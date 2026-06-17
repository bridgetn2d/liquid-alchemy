# CocktailCompositionDiagram — Implementation Brief

**Stage 1 scope only.** Read this fully before writing any code.

---

## What this is

A procedural SVG component that visualizes the functional structure of a cocktail. Each ingredient is rendered as a hexagonal node, sized proportionally to its volume, labeled by role. Nodes are connected by thin lines. The diagram is generated entirely from existing recipe data — no AI, no images, no new dependencies.

This is not the riff explorer. That is Stage 2. This brief covers Stage 1: a **static, read-only** composition diagram.

**The diagram lives in Create only — not in the recipe modal.** The recipe modal already has enough going on. The composition diagram is an experiment/education tool and belongs where experimentation lives. The recipe modal should remain unchanged.

---

## What it looks like

- Flat-top hexagons, sized by ingredient volume
- Base spirit is largest, positioned at center
- Supporting ingredients arranged outward at hex vertex angles
- Thin connecting lines with small open circle nodes at junctions
- Each hex labeled: ingredient name, role (all-caps), and amount
- Role-based stroke/fill color coding (see role vocabulary below)
- Monospaced or clean sans font; science-y, minimal, no decoration

Visual reference: a molecular/botanical codex diagram. Precise, annotated, elegant. Not a chart. Not a bar graph.

---

## Schema audit findings

**Current ingredient structure (consistent across all 140+ recipes):**

```js
{ name: "Blanco tequila", amount: "2", unit: "oz" }
```

- All ingredients are objects — no text strings
- `name`, `amount`, `unit` are always present
- `amount` is a numeric string (e.g., `"2"`, `"0.75"`, `"0.5"`)
- `unit` is always present: oz, ml, tsp, tbsp, dash, drop, splash, whole, each, strip, slice, etc.

**Adding `role` is safe.** Every function that touches ingredients (shopping list, inventory matching, ABV calc, import/export, search, craft item matching) uses only `name`, `amount`, `unit`. The `role` field is purely additive. No existing behavior changes.

---

## The `role` field

Add as an optional property on ingredient objects:

```js
{ name: "Blanco tequila", amount: "2", unit: "oz", role: "base" }
```

Recipes without `role` continue to render normally. The component falls back to the inference helper (see below).

### Role vocabulary

```
base          — Primary spirit (gin, rum, whiskey, tequila, mezcal)
acid          — Fresh citrus juice (lime, lemon, grapefruit, yuzu)
sweetener     — Syrups, liqueurs, honey, agave (primary sweetening role)
modifier      — Secondary spirit, fortified wine, amaro (flavoring/complexity)
bitter        — Bitters, cynar, campari (primarily aromatic/bitter function)
effervescent  — Soda, tonic, sparkling wine, ginger beer
texture       — Egg white, cream, aquafaba (mouthfeel/foam)
seasoning     — Salt, saline solution, rimming agents
garnish       — Citrus peel/wheel, herbs, cherry, edible decoration
aromatic      — Expressed oils, rinses, misting (aromatic delivery only)
```

Note: use `acid` not `citrus`. The label in the diagram node is the lesson — it should name the function.

### Role inference helper (for recipes without explicit roles)

Use this as a fallback when `ingredient.role` is undefined:

```js
function inferRole(ingredient) {
  const name = (ingredient.name || "").toLowerCase();
  const unit = (ingredient.unit || "").toLowerCase();

  if (["wheel", "slice", "peel", "twist", "strip", "sprig", "leaf", "whole", "each"].includes(unit)) {
    return "garnish";
  }
  if (name.match(/egg white|aquafaba|cream/i)) return "texture";
  if (name.match(/soda|tonic|champagne|prosecco|sparkling/i)) return "effervescent";
  if (name.match(/juice/) && name.match(/lemon|lime|grapefruit|orange|yuzu|pineapple/i)) return "acid";
  if (name.match(/bitters?|campari|aperol|cynar|fernet|suze/i)) return "bitter";
  if (name.match(/salt|saline/i) && unit !== "oz") return "seasoning";
  if (name.match(/vermouth|amaro|sherry|port|madeira/i)) return "modifier";
  if (name.match(/syrup|liqueur|honey|agave|falernum|orgeat|curaçao|triple sec/i)) return "sweetener";
  return "base"; // default assumption
}
```

---

## Component spec

```jsx
<CocktailCompositionDiagram cocktail={viewCocktail} />
```

**Props:**
- `cocktail` — the full cocktail object from state (same object used by the rest of the modal)

**Component behavior:**
1. Read `cocktail.ingredients`
2. For each ingredient, resolve role: use `ingredient.role` if present, otherwise call `inferRole(ingredient)`
3. Identify the base spirit (role === "base") — this becomes the center node
4. Parse `ingredient.amount` to float for sizing
5. Scale hex radius: base spirit = largest, others relative to it (use softened scale — see sizing below)
6. Arrange non-base ingredients at the 6 hex vertex angles from center, closest fit to avoid overlap
7. Render SVG: hexagons, connector lines, open circle junction nodes, text labels
8. Garnishes and seasonings: small fixed accent size (no proportional scaling — they're not volumetric)

**Hex sizing:**
```js
const MAX_R = 68;
const MIN_R = 28;
const GARNISH_R = 30; // fixed for non-volumetric roles

function hexRadius(oz, maxOz) {
  if (!oz || oz <= 0) return GARNISH_R;
  return Math.round(MIN_R + (oz / maxOz) * (MAX_R - MIN_R));
}
```

Do not use raw proportion (0.75/2 = 37.5% of base size). That makes modifier hexes unreadably small. Scale relative to the largest measured ingredient instead.

**Role-based colors (stroke / light fill):**
```js
const ROLE_STYLES = {
  base:         { stroke: "#2A2A28", fill: "#F4F3EF" },
  acid:         { stroke: "#5C7034", fill: "#EFF4E6" },
  sweetener:    { stroke: "#A85820", fill: "#FAF0E6" },
  modifier:     { stroke: "#4A5A7A", fill: "#E8EEF8" },
  bitter:       { stroke: "#7A2E50", fill: "#F5E8EF" },
  effervescent: { stroke: "#2E6678", fill: "#E8F2F4" },
  texture:      { stroke: "#5A6878", fill: "#E8F0F4" },
  seasoning:    { stroke: "#9A9A92", fill: "#F4F4F2" },
  garnish:      { stroke: "#9A9A92", fill: "#F4F4F2", dashed: true },
  aromatic:     { stroke: "#6B5A7A", fill: "#F0ECF4" },
};
```

---

## Where to render

**Create section only.** Do not add to the recipe modal.

When a user selects a drink or template in Create, the composition diagram is the first thing they see — it IS the Create section's primary UI. The recipe modal stays exactly as it is.

---

## What NOT to build in Stage 1

- No tappable/clickable nodes
- No substitution panel
- No swap logic
- No "riff this" interaction
- No saving mutations
- No Create section integration

The diagram is static and read-only. Interaction lives in Stage 2, which belongs only in the Create section and requires a separate brief.

---

## Proof-of-concept recipe set

Before tagging the full database, add explicit `role` fields to two recipes only:

- **Classic Margarita** (tequila/lime/orange liqueur/salt — clean 4-role example)
- **Whiskey Sour** (whiskey/lemon/simple syrup/egg white — introduces texture role)

Verify the diagram renders correctly with explicit roles and also correctly via inference for an untagged recipe. Then report before touching more data.

---

## Success criteria for Stage 1

- Diagram renders in recipe modal without breaking any existing display behavior
- Shopping list, inventory matching, ABV calc, search all unaffected
- Recipes without `role` fields render correctly via inference
- Explicitly tagged recipes render correctly with their assigned roles
- Component is self-contained — no changes to modal state, shopping logic, or recipe data flow required
- Diagram is visually clean, legible, and fits the existing modal layout

---

*Liquid Alchemy · June 2026 · Stage 1 of 2*
