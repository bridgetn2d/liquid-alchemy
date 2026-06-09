/* Creator, bar, and venue terms for the main recipe search bar. */
export function normalizeSearchText(s) {
  return (s || '')
    .replace(/[\u2018\u2019']/g, '')
    .normalize('NFD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9 ]/gi, ' ')
    .replace(/ +/g, ' ')
    .trim();
}

/** @deprecated Use normalizeSearchText — kept for internal call sites in this module. */
export const searchNorm = normalizeSearchText;

export const COCKTAIL_SEARCH_INDEX = 
{
  "classic-daiquiri": {
    "creators": [
      "Jennings Cox"
    ],
    "venues": [
      "El Floridita"
    ]
  },
  "classic-negroni": {
    "creators": [
      "Fosco Scarselli"
    ],
    "venues": []
  },
  "classic-cosmopolitan": {
    "creators": [
      "Toby Cecchini"
    ],
    "venues": [
      "The Odeon"
    ]
  },
  "french-75": {
    "creators": [],
    "venues": [
      "Harry's New York Bar"
    ]
  },
  "paper-plane": {
    "creators": [
      "Sam Ross"
    ],
    "venues": [
      "Attaboy",
      "Milk & Honey",
      "Violet Hour"
    ]
  },
  "classic-sidecar": {
    "creators": [],
    "venues": [
      "Harry's New York Bar"
    ]
  },
  "pisco-sour": {
    "creators": [
      "Victor Vaughen Morris"
    ],
    "venues": []
  },
  "clover-club": {
    "creators": [
      "Julie Reiner"
    ],
    "venues": [
      "Bellevue-Stratford",
      "Clover Club"
    ]
  },
  "vieux-carre": {
    "creators": [
      "Walter Bergeron"
    ],
    "venues": [
      "Carousel Bar",
      "Hotel Monteleone"
    ]
  },
  "paloma": {
    "creators": [
      "Don Javier Delgado Corona"
    ],
    "venues": [
      "La Capilla"
    ]
  },
  "bellini": {
    "creators": [
      "Giuseppe Cipriani"
    ],
    "venues": []
  },
  "jungle-bird": {
    "creators": [
      "Jeff Berry"
    ],
    "venues": [
      "Aviary Bar"
    ]
  },
  "mai-tai": {
    "creators": [
      "Jeff Berry"
    ],
    "venues": [
      "Trader Vic"
    ]
  },
  "morgenthaler-amaretto-sour": {
    "creators": [
      "Jeffrey Morgenthaler",
      "Morgenthaler"
    ],
    "venues": []
  },
  "six-seeds": {
    "creators": [],
    "venues": [
      "The Up and Up"
    ]
  },
  "zuzus-petals": {
    "creators": [
      "Matt Piacentini"
    ],
    "venues": [
      "The Up and Up"
    ]
  },
  "ramble-on": {
    "creators": [
      "Phil Ward"
    ],
    "venues": []
  },
  "ramble": {
    "creators": [
      "Phil Ward"
    ],
    "venues": [
      "Death & Co"
    ]
  },
  "naked-and-famous": {
    "creators": [
      "Phil Ward"
    ],
    "venues": []
  },
  "gargoyle": {
    "creators": [
      "George White"
    ],
    "venues": []
  },
  "cold-fashioned": {
    "creators": [
      "Reid Nelson",
      "Reidbetweenthelimes"
    ],
    "venues": [
      "Still Austin"
    ]
  },
  "thou-shall-not-be-named": {
    "creators": [
      "Erick Castro"
    ],
    "venues": [
      "Polite Provisions"
    ]
  },
  "bourbon-renewal": {
    "creators": [
      "Dick Bradsell",
      "Jeffrey Morgenthaler",
      "Morgenthaler"
    ],
    "venues": [
      "Bel Ami Lounge",
      "Clyde Common",
      "Death & Co",
      "PDT",
      "Pdt"
    ]
  },
  "tia-mia": {
    "creators": [
      "Ivy Mix",
      "Jeff Berry"
    ],
    "venues": [
      "Lani Kai",
      "Leyenda",
      "Trader Vic"
    ]
  },
  "sonambula": {
    "creators": [
      "Ivy Mix"
    ],
    "venues": [
      "Clover Club",
      "Fort Defiance",
      "Leyenda"
    ]
  },
  "oaxacan-old-fashioned": {
    "creators": [
      "Phil Ward"
    ],
    "venues": [
      "Death & Co",
      "Mayahuel"
    ]
  },
  "gin-basil-smash": {
    "creators": [
      "Jorg Meyer"
    ],
    "venues": [
      "Bar de Paris",
      "Death & Co",
      "Le Lion"
    ]
  },
  "infante": {
    "creators": [
      "Erick Castro",
      "Sam Ross"
    ],
    "venues": []
  },
  "irish-maid": {
    "creators": [
      "Sam Ross"
    ],
    "venues": []
  },
  "guardian-angel": {
    "creators": [
      "Erick Castro"
    ],
    "venues": [
      "Polite Provisions",
      "Raised By Wolves",
      "Raised by Wolves"
    ]
  },
  "springs-first-bloom": {
    "creators": [
      "Charlotte Voisey"
    ],
    "venues": []
  },
  "genovese-smash": {
    "creators": [
      "Jorg Meyer"
    ],
    "venues": []
  },
  "morgenthaler-sbagliato": {
    "creators": [
      "Jeffrey Morgenthaler",
      "Morgenthaler"
    ],
    "venues": []
  },
  "french-blonde": {
    "creators": [
      "Jorg Meyer"
    ],
    "venues": [
      "Le Lion"
    ]
  },
  "rosemary-gin-smash": {
    "creators": [
      "Jorg Meyer"
    ],
    "venues": [
      "Le Lion"
    ]
  },
  "pineapple-makrut-buck": {
    "creators": [
      "Camila Chaparro"
    ],
    "venues": []
  },
  "sicilian-sojourn": {
    "creators": [
      "Camila Chaparro"
    ],
    "venues": []
  },
  "citrus-peel-sculpture": {
    "creators": [
      "Reid Nelson"
    ],
    "venues": []
  },
  "mosquito": {
    "creators": [
      "Brandon Bramhall",
      "Jojo Colona",
      "Mike McCollum",
      "Sam Ross"
    ],
    "venues": [
      "Attaboy"
    ]
  },
  "praying-mantis": {
    "creators": [
      "Brandon Bramhall",
      "Jojo Colona",
      "Mike McCollum",
      "Sam Ross"
    ],
    "venues": [
      "Attaboy"
    ]
  },
  "maverick": {
    "creators": [
      "Brandon Bramhall",
      "Jojo Colona",
      "Mike McCollum",
      "Mike Mccollum",
      "Sam Ross"
    ],
    "venues": [
      "Attaboy"
    ]
  },
  "lantern-fly": {
    "creators": [
      "Brandon Bramhall",
      "Jojo Colona",
      "Mike McCollum",
      "Sam Ross"
    ],
    "venues": [
      "Attaboy"
    ]
  }
};

export const SEARCH_ALIAS_TO_IDS = 
{
  "jeffrey morgenthaler": [
    "bourbon-renewal",
    "morgenthaler-amaretto-sour",
    "morgenthaler-sbagliato"
  ],
  "morgenthaler": [
    "bourbon-renewal",
    "morgenthaler-amaretto-sour",
    "morgenthaler-sbagliato"
  ],
  "ivy mix": [
    "sonambula",
    "tia-mia"
  ],
  "sam ross": [
    "infante",
    "irish-maid",
    "lantern-fly",
    "maverick",
    "mosquito",
    "paper-plane",
    "praying-mantis"
  ],
  "jorg meyer": [
    "french-blonde",
    "genovese-smash",
    "gin-basil-smash",
    "rosemary-gin-smash"
  ],
  "julie reiner": [
    "clover-club"
  ],
  "phil ward": [
    "naked-and-famous",
    "oaxacan-old-fashioned",
    "ramble",
    "ramble-on"
  ],
  "matt piacentini": [
    "zuzus-petals"
  ],
  "erick castro": [
    "guardian-angel",
    "infante",
    "thou-shall-not-be-named"
  ],
  "toby cecchini": [
    "classic-cosmopolitan"
  ],
  "jeff berry": [
    "jungle-bird",
    "mai-tai",
    "tia-mia"
  ],
  "reid nelson": [
    "citrus-peel-sculpture",
    "cold-fashioned"
  ],
  "reidbetweenthelimes": [
    "cold-fashioned"
  ],
  "brandon bramhall": [
    "praying-mantis"
  ],
  "mike mccollum": [
    "maverick"
  ],
  "jojo colona": [
    "lantern-fly"
  ],
  "camila chaparro": [
    "pineapple-makrut-buck",
    "sicilian-sojourn"
  ],
  "charlotte voisey": [
    "springs-first-bloom"
  ],
  "attaboy": [
    "lantern-fly",
    "maverick",
    "mosquito",
    "paper-plane",
    "praying-mantis"
  ],
  "milk and honey": [
    "paper-plane"
  ],
  "milk honey": [
    "paper-plane"
  ],
  "death and co": [
    "bourbon-renewal",
    "gin-basil-smash",
    "oaxacan-old-fashioned",
    "ramble"
  ],
  "death co": [
    "bourbon-renewal",
    "oaxacan-old-fashioned",
    "ramble"
  ],
  "leyenda": [
    "sonambula",
    "tia-mia"
  ],
  "clover club": [
    "clover-club",
    "sonambula"
  ],
  "pdt": [
    "bourbon-renewal"
  ],
  "clyde common": [
    "bourbon-renewal"
  ],
  "hotel monteleone": [
    "vieux-carre"
  ],
  "carousel bar": [
    "vieux-carre"
  ],
  "harrys new york bar": [
    "classic-sidecar",
    "french-75"
  ],
  "the odeon": [
    "classic-cosmopolitan"
  ],
  "fort defiance": [
    "sonambula"
  ],
  "le lion": [
    "french-blonde",
    "gin-basil-smash",
    "rosemary-gin-smash"
  ],
  "violet hour": [
    "paper-plane"
  ],
  "mayahuel": [
    "oaxacan-old-fashioned"
  ],
  "the up and up": [
    "six-seeds",
    "zuzus-petals"
  ],
  "polite provisions": [
    "guardian-angel",
    "thou-shall-not-be-named"
  ],
  "raised by wolves": [
    "guardian-angel"
  ],
  "still austin": [
    "cold-fashioned"
  ],
  "lani kai": [
    "tia-mia"
  ],
  "bel ami lounge": [
    "bourbon-renewal"
  ],
  "el floridita": [
    "classic-daiquiri"
  ],
  "la capilla": [
    "paloma"
  ],
  "aviary bar": [
    "jungle-bird"
  ],
  "trader vic": [
    "mai-tai",
    "tia-mia"
  ]
};

function aliasMatchesQuery(alias, q) {
  if (!q) return false;
  const na = searchNorm(alias);
  if (na.includes(q) || q.includes(na)) return true;
  const words = q.split(' ').filter(w => w.length > 1);
  return words.length > 1 && words.every(w => na.includes(w));
}

export function cocktailSearchText(c) {
  const idx = COCKTAIL_SEARCH_INDEX[c.id];
  const extra = c.searchTerms || [];
  return searchNorm([
    c.name, c.aka, c.baseSpirit, c.family, c.subFamily,
    c.lore, c.notes, c.riffs, c.instructions, c.source, c.sourceUrl,
    ...(c.ingredients || []).map(i => i.name),
    ...(c.tags || []),
    ...(idx?.creators || []),
    ...(idx?.venues || []),
    ...extra,
  ].filter(Boolean).join(' '));
}

export function cocktailMatchesSearch(c, q) {
  if (!q) return true;
  const blob = cocktailSearchText(c);
  if (blob.includes(q)) return true;
  const words = q.split(' ').filter(w => w.length > 1);
  if (words.length > 1 && words.every(w => blob.includes(w))) return true;
  for (const [alias, ids] of Object.entries(SEARCH_ALIAS_TO_IDS)) {
    if (ids.includes(c.id) && aliasMatchesQuery(alias, q)) return true;
  }
  return false;
}

