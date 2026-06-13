# Data contributing — canonical cocktails

How to add or update **permanent** recipes baked into the app. This describes the current pre-recipe-extraction workflow, where canonical recipes still live primarily in `app.jsx`.

## Overview

Canonical recipes are **not** only in user storage. They ship as JavaScript constants and are **merged on every app load**:

- If `alchemy_cocktails` has no entry with the same `id`, the recipe is injected.
- If the user already has that `id` in storage, the stored version is kept (user data wins).

Illustrations are **not** stored inside the cocktail JSON in `alchemy_cocktails`. They use separate keys: `alchemy_img_{id}`, `alchemy_myphoto_{id}`, `alchemy_thumb_{id}`.

## Where to edit

| Step | Location |
|------|----------|
| Define the recipe object | **My Recipes** block in `app.jsx` (individual `const` recipe constants) |
| Register for merge | `MY_RECIPES_LIST` array in `app.jsx` |
| Comment marker | “Add new recipes above this line” in the My Recipes section |

Follow an existing recipe (e.g. `CLASSIC_MARGARITA`, `NEGRONI`) as a template.

For a section-level map of `app.jsx`, see [project-map.md](project-map.md).

## Recipe object checklist

### Required for a good entry

| Field | Notes |
|-------|--------|
| `id` | Unique, kebab-case slug (e.g. `classic-negroni`). **Never change** after users may have storage under this id. |
| `name` | Display name |
| `family` | Primary family (align with Families tab / `TEMPLATES_DATA`) |
| `subFamily` | Subfamily label (can be `""`) |
| `baseSpirit` | One of `SPIRIT_OPTIONS` |
| `glass` | One of `GLASS_OPTIONS` |
| `occasion` | One of `OCCASION_OPTIONS` |
| `season` | One of `SEASON_OPTIONS` |
| `difficulty` | `Easy`, `Medium`, or `Advanced` |
| `serveStyle` | One of `SERVE_STYLES` |
| `tags` | Array from `CHAR_TAGS` |
| `sliders` | Object with keys: `boozy`, `sweet`, `sour`, `bitter`, `fruity`, `herbal`, `smoky`, `spicy`, `rich` (0–10) |
| `ingredients` | `[{ name, amount, unit }]` — `unit` typically `oz`, `ml`, `dash`, `whole`, etc. |
| `instructions` | Prose |
| `addedAt` | `Date.now()` or offset (used for “Recent” sort) |

### Recommended prose

| Field | Purpose |
|-------|---------|
| `notes` | Technique, brands, ratios |
| `lore` | History, family context, creator attribution |
| `riffs` | Variations (keep distinct from `notes`) |
| `tastingNotes` | Personal tasting log placeholder (`""` in canon) |

### Optional flags / links

| Field | Purpose |
|-------|---------|
| `obscura` | `true` — surfaces under Obscura filter (“best cocktails you’ve never heard of”) |
| `rating` | Usually `0` in canon; users set in app |
| `craftLinks` | Array of craft item `id`s from `alchemy_craft` |
| `sourceUrl` | External reference — where the recipe spec itself originated |
| `citations` | Optional. Sources supporting lore, history, provenance, creator context, or educational claims. Distinct from recipe `sourceUrl`. Preserved in export when populated; not shown in app UI yet. |
| `imageUrl` | `""` in source — seed may set; runtime uses `alchemy_img_{id}` |
| `myPhoto` | Always `""` in canon |

### Workbook provenance fields (`Lore` tab)

For workbook-driven content, provenance-related fields live on the `Lore` tab in the canonical workbook (`content/workbook/`). Column order near provenance content:

| Workbook field | App field (when exported) | Notes |
|----------------|---------------------------|--------|
| `creator_id` | — | Join key to `Creators` tab; not exported to app JSON today |
| `source_urls` | `sourceUrl` (first URL) | Recipe / spec source URLs |
| `citations` | `citations` | Optional. Sources supporting lore, history, provenance, creator context, or educational claims. Distinct from recipe `sourceUrl`. Preserved in export when populated; not shown in app UI yet. |
| `why_it_works` | — | Editorial framing; workbook-only |
| `story` | `lore` | Historical narrative |

Do not auto-populate `citations`. Leave blank until editorially sourced.

Workbook → app export is handled by `scripts/workbook_to_json.py`. See [architecture.md](architecture.md) for the export pipeline.

### Slider defaults

If unsure, start from `DEFAULT_SLIDERS` (all zeros) and adjust to match `tags`, or copy a similar drink.

## Ingredient names and ABV

- `calcABV` uses `ABV_TABLE` / `SUGAR_TABLE` in `app.jsx`. Unknown ingredients are skipped in ABV math but still show in the recipe.
- Prefer names that match table keys or common variants (lowercase substring matching).
- For inventory **Can Make**, naming should be close to cabinet item names (fuzzy word match).

## Registration in `MY_RECIPES_LIST`

After defining `const MY_DRINK = { ... }`:

1. Add `MY_DRINK` (the constant name) to the `MY_RECIPES_LIST` array.
2. Order in the list is not critical for merge; it only affects inject order when multiple are new at once.

```javascript
const MY_RECIPES_LIST = [
  // ...
  MY_NEW_DRINK,
];
```

Missing this step = recipe **never** ships to users who already have other data in storage.

## Images

- **Do not** commit huge base64 strings on the recipe object for normal canon work.
- For **beta/first-run** seed, `BETA_SEED_DATA` may include `imageUrl`; those are copied to `alchemy_img_{id}` on first load.
- For My Recipes merge, illustrations are usually added via the in-app editor (stored per id) or a one-time seed path — not required in the constant for the recipe to appear (placeholder/family image used).

## Families and templates

- Set `family` / `subFamily` to match [Families tab](architecture.md) curriculum (`TEMPLATES_DATA` in `app.jsx`).
- Optional: add cocktail `id` to a subfamily’s `appIds` in `TEMPLATES_DATA` so it appears in family navigation links.

## Load-time patches

Some ids receive extra fields in `App`’s load `useEffect` (e.g. `family`, `lore` backfill). Prefer setting correct `family` / `lore` on the constant instead of relying on a new patch.

Search `app.jsx` for `x.id === "your-id"` before adding duplicate patches.

## What not to edit for a simple new recipe

- `BETA_SEED_DATA` — first-run only when storage is empty
- `DEFAULT_INVENTORY` / `DEFAULT_CRAFT_ITEMS` — unless the drink depends on new defaults
- Unrelated recipes in the My Recipes block

## Checklist before merge

- [ ] Unique `id` (grep the repo for collisions)
- [ ] Constant added to `MY_RECIPES_LIST`
- [ ] `tags` values exist in `CHAR_TAGS`
- [ ] `sliders` keys complete (nine keys)
- [ ] At least one ingredient with `name` and `amount`
- [ ] `family` / `subFamily` consistent with taxonomy
- [ ] Optional: `obscura`, `craftLinks`, `appIds` in templates

## Future extraction

[refactor-plan.md](refactor-plan.md) describes moving recipes out of `app.jsx` into structured data files. Until that migration lands, use the workflow above.

## Related docs

- [architecture.md](architecture.md) — persistence, merge pipeline, and workbook export
- [project-map.md](project-map.md) — section map for `app.jsx` (line numbers may drift)
- [AGENTS.md](../AGENTS.md) — AI task routing
