#!/usr/bin/env python3
"""
Generate LIVE_COCKTAILS.md — the canonical, searchable index of every cocktail
currently live in the app.

Source of truth: app.jsx -> MY_RECIPES_LIST (the array the app actually ships).
It contains individual const cocktail objects, single-object consts (e.g.
SIX_SEEDS), and spreads of pack arrays (...TIKI_PACK_003, ...CLASSICS_PACK_004).

Re-run this whenever cocktails or packs are added:
    python3 scripts/list_live_cocktails.py

It reads app.jsx fresh each time, so the output always matches what's live.
"""
import re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "app.jsx"
OUT = ROOT / "LIVE_COCKTAILS.md"

txt = APP.read_text()

# --- 1. Pull the live registry block: const MY_RECIPES_LIST = [ ... ]; ---
m = re.search(r'const MY_RECIPES_LIST\s*=\s*\[(.*?)\n\];', txt, re.S)
if not m:
    sys.exit("ERROR: could not locate MY_RECIPES_LIST in app.jsx")
block = m.group(1)

const_idents, spread_idents = [], []
for raw in block.splitlines():
    line = raw.split("//")[0].strip().rstrip(",").strip()
    if not line:
        continue
    if line.startswith("..."):
        spread_idents.append(line[3:].strip())
    elif re.fullmatch(r"[A-Z0-9_]+", line):
        const_idents.append(line)

def fields_from_window(win):
    idm = re.search(r'\bid:\s*"([^"]+)"', win)
    nm  = re.search(r'\bname:\s*"([^"]+)"', win)
    fm  = re.search(r'\bfamily:\s*"([^"]+)"', win)
    sf  = re.search(r'\bsubFamily:\s*"([^"]+)"', win)
    ak  = re.search(r'\baka:\s*"([^"]+)"', win)
    return {
        "id": idm.group(1) if idm else "",
        "name": nm.group(1) if nm else "",
        "family": fm.group(1) if fm else "",
        "subFamily": sf.group(1) if sf else "",
        "aka": ak.group(1) if ak else "",
    }

rows, missing = [], []

# --- 2. Resolve each single-object const ---
for ident in const_idents:
    cm = re.search(r'const\s+' + re.escape(ident) + r'\s*=\s*\{', txt)
    if not cm:
        missing.append(ident)
        continue
    f = fields_from_window(txt[cm.end(): cm.end() + 1800])
    f["source"] = "core"
    rows.append(f)

# --- 3. Resolve each spread pack array ---
for arr in spread_idents:
    am = re.search(r'const\s+' + re.escape(arr) + r'\s*=\s*\[', txt)
    if not am:
        missing.append(arr + " (array)")
        continue
    seg = txt[am.end():]
    seg = seg[: seg.find("\n];")]
    for om in re.finditer(r'\bid:\s*"([^"]+)"', seg):
        f = fields_from_window(seg[om.start(): om.start() + 600])
        f["source"] = arr
        rows.append(f)

# --- 4. Dedupe by id (preserve first), sort by name ---
seen, uniq = set(), []
for r in rows:
    key = r["id"] or r["name"]
    if key in seen:
        continue
    seen.add(key)
    uniq.append(r)
uniq.sort(key=lambda r: r["name"].lower())

# --- 5. Write the searchable markdown ---
today = datetime.date.today().isoformat()
lines = []
lines.append("# Live Cocktails — master index")
lines.append("")
lines.append(f"Auto-generated from `app.jsx` (`MY_RECIPES_LIST`) on {today}. "
             f"**{len(uniq)} cocktails live.**")
lines.append("")
lines.append("Regenerate after adding any cocktail or pack: "
             "`python3 scripts/list_live_cocktails.py`")
lines.append("")
lines.append("Search this file (Cmd/Ctrl-F) by name, alias, id, or family before "
             "adding a new find — if it's here, it's already in the app.")
lines.append("")
lines.append("| # | Cocktail | Also known as | Family / Sub-family | id | source |")
lines.append("|---|----------|---------------|---------------------|----|--------|")
for i, r in enumerate(uniq, 1):
    fam = r["family"] + (" / " + r["subFamily"] if r["subFamily"] else "")
    lines.append(f"| {i} | {r['name']} | {r['aka']} | {fam} | `{r['id']}` | {r['source']} |")
lines.append("")
lines.append("## Plain name list (quick scan / paste)")
lines.append("")
lines.append(", ".join(r["name"] for r in uniq))
lines.append("")
if missing:
    lines.append("## ⚠ Unresolved entries (in MY_RECIPES_LIST but object not found)")
    lines.append("")
    for x in missing:
        lines.append(f"- {x}")
    lines.append("")

OUT.write_text("\n".join(lines))
print(f"Wrote {OUT} — {len(uniq)} live cocktails"
      + (f", {len(missing)} unresolved: {missing}" if missing else ""))
