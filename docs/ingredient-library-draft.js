// LIQUID ALCHEMY — INGREDIENT LIBRARY DRAFT
// Editorial work in progress. Do not wire into app.jsx until all target roles are complete and approved.
// Format mirrors the Stage 4 schema agreed in the Riff Lab implementation brief.
//
// Role vocabulary: base · acid · sweetener · modifier · bitter · effervescent · texture · seasoning · garnish · aromatic

const INGREDIENT_LIBRARY = [

  // ── ACID ──────────────────────────────────────────────────────────────────

  {
    id: "fresh-lime-juice",
    name: "Fresh lime juice",
    role: "acid",
    substituteFor: ["fresh-lemon-juice", "grapefruit-juice", "yuzu-juice"],
    intensityNotes: "High acid, sharp and tropical. The default acid in sours and daiquiri-family drinks. More aggressive than lemon — sweetener may need to rise slightly when swapping lemon for lime."
  },
  {
    id: "fresh-lemon-juice",
    name: "Fresh lemon juice",
    role: "acid",
    substituteFor: ["fresh-lime-juice", "grapefruit-juice", "yuzu-juice", "verjus-white"],
    intensityNotes: "High acid, softer and more floral than lime. More versatile — works across sours, fizzes, and egg white drinks. Sweetness perception stays similar when swapping lime for lemon."
  },
  {
    id: "grapefruit-juice",
    name: "Fresh grapefruit juice",
    role: "acid",
    substituteFor: ["fresh-lime-juice", "fresh-lemon-juice"],
    intensityNotes: "Moderate acid with significant bitterness. Lower juice yield means you typically need more volume — ¾ oz lime becomes 1–1¼ oz grapefruit. Bitterness rises; sweetener may need to drop or shift to something drier."
  },
  {
    id: "yuzu-juice",
    name: "Yuzu juice",
    role: "acid",
    substituteFor: ["fresh-lemon-juice", "fresh-lime-juice"],
    intensityNotes: "High acid, intensely aromatic — floral, tart, faintly piney. Use less than the original spec calls for; its aromatic intensity can dominate. Start at half the called-for volume and adjust."
  },
  {
    id: "verjus-white",
    name: "Verjus (white)",
    role: "acid",
    substituteFor: ["fresh-lemon-juice"],
    intensityNotes: "Low-moderate acid, no citrus character. Made from unfermented grape juice — wine-adjacent, soft, slightly tart. Works in spirit-forward or wine-based drinks where citrus would be too aggressive. Typically needs more volume than lemon."
  },
  {
    id: "pineapple-juice",
    name: "Fresh pineapple juice",
    role: "acid",
    substituteFor: ["fresh-lime-juice"],
    intensityNotes: "Moderate acid, high natural sweetness and tropical character. Contains bromelain, which softens texture over time. Sweetener often needs to drop when pineapple replaces lime — it brings its own sugar. Works especially well in rum and tequila contexts."
  },
  {
    id: "passion-fruit-puree",
    name: "Passion fruit purée",
    role: "acid",
    substituteFor: ["fresh-lime-juice"],
    intensityNotes: "Moderate acid with intense tropical flavor. Sweet-tart balance means it functions as both acid and partial sweetener — reduce the sweetener when adding. Aromatic intensity is high; a little goes a long way."
  },
  {
    id: "tamarind-concentrate",
    name: "Tamarind concentrate",
    role: "acid",
    substituteFor: ["fresh-lime-juice"],
    intensityNotes: "Moderate-high acid, earthy, dark, sweet-sour. Completely changes the flavor profile of a drink — not a neutral swap. Best used in tequila, mezcal, and rum contexts. Needs thinning with water before use; concentration varies by brand."
  },
  {
    id: "fresh-orange-juice",
    name: "Fresh orange juice",
    role: "acid",
    substituteFor: ["fresh-lemon-juice", "fresh-lime-juice"],
    intensityNotes: "Low acid, high natural sweetness. Functions as both acid and partial sweetener — reduce or eliminate added sweetener when swapping in. Softens a drink considerably; the sour edge largely disappears. Works best in low-ABV and wine-based contexts, or when that softness is the point."
  },
  {
    id: "fresh-tangerine-juice",
    name: "Fresh tangerine juice",
    role: "acid",
    substituteFor: ["fresh-orange-juice", "fresh-lemon-juice"],
    intensityNotes: "Low acid, sweeter and more floral than orange. Similar swap logic to OJ — treat it as acid plus sweetener in one. Seasonal; peak flavor is winter. Pairs particularly well with aged spirits and light rum."
  },

  // ── SWEETENER ─────────────────────────────────────────────────────────────

  // TO DO

  // ── MODIFIER ──────────────────────────────────────────────────────────────

  // TO DO

  // ── BASE SPIRIT ───────────────────────────────────────────────────────────

  // TO DO

  // ── BITTER ────────────────────────────────────────────────────────────────

  // TO DO

  // ── EFFERVESCENT ──────────────────────────────────────────────────────────

  // TO DO

  // ── TEXTURE ───────────────────────────────────────────────────────────────

  // TO DO

  // ── SEASONING ─────────────────────────────────────────────────────────────

  // TO DO

  // ── AROMATIC ──────────────────────────────────────────────────────────────

  // TO DO

];
