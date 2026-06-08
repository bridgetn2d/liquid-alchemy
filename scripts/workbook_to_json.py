#!/usr/bin/env python3
"""
Proof-of-concept exporter: Liquid Alchemy workbook → app-import JSON.

Reads canonical workbook tabs, filters by App_JSON_Export.export_ready = YES,
and writes { cocktails, inventory } JSON for the app Import UI.
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKBOOK = ROOT / "content/workbook/Liquid_Alchemy_Content_Database_v1_repo_ready.xlsx"
DEFAULT_OUTPUT = ROOT / "content/exports/test_workbook_export.json"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
SLIDER_KEYS = ("boozy", "sweet", "sour", "bitter", "fruity", "herbal", "smoky", "spicy", "rich")

APP_FAMILIES = {
    "Flip, Nog & Creamy",
    "Highball",
    "Julep",
    "Martini & Manhattan",
    "Negroni",
    "Old Fashioned",
    "Sour",
    "Spritz & Aperitivo",
    "Tiki & Tropical",
}
APP_SPIRITS = {
    "Gin", "Vodka", "Rum", "Cachaca", "Tequila", "Mezcal", "Whiskey", "Bourbon",
    "Scotch", "Rye", "Brandy", "Cognac", "Pisco", "Champagne/Prosecco", "Beer",
    "Wine", "Amaro", "Aperol", "Campari", "Vermouth", "Liqueur", "Non-alcoholic", "Other",
}
APP_GLASSES = {
    "Coupe", "Martini", "Rocks/Old Fashioned", "Highball", "Collins", "Nick & Nora",
    "Champagne Flute", "Wine Glass", "Tiki Mug", "Copper Mug", "Snifter", "Shot Glass",
    "Pint Glass", "Other",
}
APP_OCCASIONS = {
    "Aperitivo", "After Dinner", "Brunch", "Party/Batch", "Date Night", "Nightcap",
    "Warm Weather", "Cold Weather", "Holiday", "Anytime",
}
APP_SEASONS = {"Spring", "Summer", "Fall", "Winter", "Year-Round"}
APP_DIFFICULTIES = {"Easy", "Medium", "Advanced"}
APP_SERVE_STYLES = {"Up", "On the Rocks", "Highball", "Neat", "Frozen"}
APP_TAGS = {
    "Boozy", "Sweet", "Sour/Tart", "Fruity", "Herbal/Botanical", "Smoky", "Bitter",
    "Creamy/Rich", "Spicy", "Savory", "Light/Refreshing", "Sparkling", "Tropical", "Elegant",
}
TAG_EXPORT_RULES = {
    "normalize_on_export",
    "normalize_or_keep_future",
    "map_or_add_to_app",
    "map_or_keep_future",
    "first_class_tag",
}

ENUM_EXPORT_RULES = {
    "normalize_on_export",
    "normalize_or_app_change",
    "normalize_or_keep_future",
    "map_or_add_to_app",
    "map_or_keep_future",
}
def cell_text(cell: ET.Element) -> str:
    t = cell.get("t")
    if t == "inlineStr":
        inline = cell.find("m:is", NS)
        if inline is not None:
            return "".join((node.text or "") for node in inline.findall(".//m:t", NS))
    value = cell.find("m:v", NS)
    return (value.text or "") if value is not None else ""


def sheet_path_from_target(target: str) -> str:
    if target.startswith("/"):
        target = target[1:]
    return target if target.startswith("xl/") else f"xl/{target}"


def read_sheet_as_dicts(zf: zipfile.ZipFile, sheet_path: str) -> list[dict[str, str]]:
    root = ET.fromstring(zf.read(sheet_path))
    rows_by_num: dict[int, dict[str, str]] = {}

    for row in root.findall(".//m:sheetData/m:row", NS):
        rnum = int(row.get("r", 0))
        cells: dict[str, str] = {}
        for cell in row.findall("m:c", NS):
            ref = cell.get("r", "")
            match = re.match(r"([A-Z]+)(\d+)", ref)
            if not match:
                continue
            cells[match.group(1)] = cell_text(cell)
        if cells:
            rows_by_num[rnum] = cells

    if not rows_by_num:
        return []

    header_row = rows_by_num.get(1, rows_by_num[min(rows_by_num)])
    cols = sorted(header_row.keys(), key=lambda col: (len(col), col))
    headers = [header_row[col] for col in cols]

    records: list[dict[str, str]] = []
    for rnum in sorted(rows_by_num):
        if rnum == 1:
            continue
        row = rows_by_num[rnum]
        record = {headers[i]: row.get(cols[i], "") for i in range(len(cols)) if headers[i]}
        if any(value for value in record.values()):
            records.append(record)
    return records


def load_workbook_sheets(workbook_path: Path) -> dict[str, list[dict[str, str]]]:
    with zipfile.ZipFile(workbook_path) as zf:
        workbook_xml = ET.fromstring(zf.read("xl/workbook.xml"))
        rels_xml = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rid_to_target = {
            rel.get("Id"): rel.get("Target")
            for rel in rels_xml.findall(
                ".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"
            )
        }

        name_to_path: dict[str, str] = {}
        for sheet in workbook_xml.findall(".//m:sheet", NS):
            name = sheet.get("name")
            rid = sheet.get(REL_NS + "id")
            if name and rid:
                name_to_path[name] = sheet_path_from_target(rid_to_target[rid])

        return {
            sheet_name: read_sheet_as_dicts(zf, path)
            for sheet_name, path in name_to_path.items()
        }


def snake_to_kebab(recipe_id: str) -> str:
    return recipe_id.replace("_", "-")


def kebab_to_snake(app_id: str) -> str:
    return app_id.replace("-", "_")


def parse_tags(raw: str) -> list[str]:
    if not raw or not raw.strip():
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def load_enum_normalization(
    rows: list[dict[str, str]],
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    """Return (field -> workbook value -> app value, field -> workbook value -> rule)."""
    mappings: dict[str, dict[str, str]] = defaultdict(dict)
    rules: dict[str, dict[str, str]] = defaultdict(dict)
    for row in rows:
        field = row.get("Field", "").strip()
        workbook_value = row.get("Workbook Value", "").strip()
        app_value = row.get("Current App Value", "").strip()
        rule = row.get("Rule", "").strip()
        if not field or not workbook_value or not app_value:
            continue
        mappings[field][workbook_value] = app_value
        rules[field][workbook_value] = rule
    return dict(mappings), dict(rules)


def load_tag_normalization(
    rows: list[dict[str, str]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Return (legacy tag -> app tag, legacy tag -> rule)."""
    mappings: dict[str, str] = {}
    rules: dict[str, str] = {}
    for row in rows:
        legacy = row.get("Workbook / Legacy Tag", "").strip()
        app_value = row.get("Current App CHAR_TAGS Value", "").strip()
        rule = row.get("Rule", "").strip()
        if not legacy or rule == "reference":
            continue
        if rule not in TAG_EXPORT_RULES:
            continue
        mappings[legacy] = app_value
        rules[legacy] = rule
    return mappings, rules


def normalize_enum_value(
    field: str,
    value: str,
    enum_maps: dict[str, dict[str, str]],
    enum_rules: dict[str, dict[str, str]],
) -> str:
    value = (value or "").strip()
    if not value:
        return value
    field_map = enum_maps.get(field, {})
    if value not in field_map:
        return value
    rule = enum_rules.get(field, {}).get(value, "")
    if rule in ENUM_EXPORT_RULES or rule == "future_or_display_only":
        return field_map[value]
    return value


def normalize_tags(tags: list[str], tag_map: dict[str, str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        mapped = tag_map.get(tag, tag)
        if mapped not in seen:
            seen.add(mapped)
            normalized.append(mapped)
    return normalized


def parse_sliders(recipe: dict[str, str]) -> dict[str, int]:
    sliders: dict[str, int] = {}
    for key in SLIDER_KEYS:
        raw = recipe.get(key, "").strip()
        sliders[key] = int(float(raw)) if raw else 0
    return sliders


def parse_optional_int(raw: str, default: int = 0) -> int:
    raw = (raw or "").strip()
    if not raw:
        return default
    return int(float(raw))


def parse_obscura(raw: str) -> bool:
    return str(raw).strip().upper() in {"TRUE", "YES", "1"}


def parse_craft_links(raw: str):
    raw = (raw or "").strip()
    if not raw:
        return []
    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def build_ingredients(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    sorted_rows = sorted(rows, key=lambda row: int(row.get("sort_order") or 0))
    ingredients: list[dict[str, str]] = []
    for row in sorted_rows:
        name = row.get("ingredient_name_source", "").strip()
        if not name:
            continue
        ingredients.append(
            {
                "name": name,
                "amount": row.get("amount", "").strip(),
                "unit": row.get("unit", "").strip(),
            }
        )
    return ingredients


def build_instructions(rows: list[dict[str, str]]) -> str:
    sorted_rows = sorted(rows, key=lambda row: int(row.get("step_number") or 0))
    parts = [row.get("instruction", "").strip() for row in sorted_rows if row.get("instruction", "").strip()]
    return " ".join(parts)


def build_cocktail(
    recipe: dict[str, str],
    ingredients: list[dict[str, str]],
    steps: list[dict[str, str]],
    lore: dict[str, str] | None,
    *,
    enum_maps: dict[str, dict[str, str]],
    enum_rules: dict[str, dict[str, str]],
    tag_map: dict[str, str],
) -> dict:
    raw_tags = parse_tags(recipe.get("tags", ""))
    cocktail: dict = {
        "id": snake_to_kebab(recipe["recipe_id"]),
        "name": recipe.get("name", "").strip(),
        "family": normalize_enum_value("family", recipe.get("family", ""), enum_maps, enum_rules),
        "subFamily": normalize_enum_value("subFamily", recipe.get("subfamily", ""), enum_maps, enum_rules),
        "baseSpirit": normalize_enum_value("baseSpirit", recipe.get("base_spirit", ""), enum_maps, enum_rules),
        "glass": normalize_enum_value("glass", recipe.get("glass", ""), enum_maps, enum_rules),
        "occasion": normalize_enum_value("occasion", recipe.get("occasion", ""), enum_maps, enum_rules),
        "season": normalize_enum_value("season", recipe.get("season", ""), enum_maps, enum_rules),
        "difficulty": normalize_enum_value("difficulty", recipe.get("difficulty", ""), enum_maps, enum_rules),
        "serveStyle": recipe.get("serve_style", "").strip(),
        "tags": normalize_tags(raw_tags, tag_map),
        "sliders": parse_sliders(recipe),
        "ingredients": ingredients,
        "instructions": build_instructions(steps),
        "rating": parse_optional_int(recipe.get("rating", ""), 0),
        "addedAt": parse_optional_int(recipe.get("source_added_at", ""), 0),
        "imageUrl": "",
        "myPhoto": "",
    }

    if lore:
        notes = lore.get("notes", "").strip()
        story = lore.get("story", "").strip()
        riffs = lore.get("riffs", "").strip()
        tasting = lore.get("tasting_notes", "").strip()
        if notes:
            cocktail["notes"] = notes
        if story:
            cocktail["lore"] = story
        if riffs:
            cocktail["riffs"] = riffs
        if tasting:
            cocktail["tastingNotes"] = tasting

    aka = recipe.get("aka", "").strip()
    if aka:
        cocktail["aka"] = aka

    source_url = recipe.get("sourceUrl", "").strip()
    if not source_url and lore:
        source_url = lore.get("source_urls", "").strip().split("\n")[0].strip()
    if source_url:
        cocktail["sourceUrl"] = source_url

    obscura_raw = recipe.get("obscura", "").strip()
    if obscura_raw:
        cocktail["obscura"] = parse_obscura(obscura_raw)

    craft_links = parse_craft_links(recipe.get("craftLinks", ""))
    if craft_links:
        cocktail["craftLinks"] = craft_links

    return cocktail


def collect_mapping_uncertainties(
    cocktails: list[dict],
    recipes_by_id: dict[str, dict[str, str]],
    *,
    enum_rules: dict[str, dict[str, str]],
    tag_map: dict[str, str],
) -> list[str]:
    """Validate post-normalization export values against app enums."""
    uncertainties: list[str] = []

    for cocktail in cocktails:
        cid = cocktail["id"]
        recipe_id = kebab_to_snake(cid)
        recipe = recipes_by_id.get(recipe_id, {})

        checks = (
            ("family", cocktail.get("family", ""), APP_FAMILIES),
            ("baseSpirit", cocktail.get("baseSpirit", ""), APP_SPIRITS),
            ("glass", cocktail.get("glass", ""), APP_GLASSES),
            ("occasion", cocktail.get("occasion", ""), APP_OCCASIONS),
            ("season", cocktail.get("season", ""), APP_SEASONS),
            ("difficulty", cocktail.get("difficulty", ""), APP_DIFFICULTIES),
            ("serveStyle", cocktail.get("serveStyle", ""), APP_SERVE_STYLES),
        )
        for field, value, allowed in checks:
            if value and value not in allowed:
                raw = recipe.get(
                    "family" if field == "family" else
                    "base_spirit" if field == "baseSpirit" else
                    "glass" if field == "glass" else
                    "occasion" if field == "occasion" else
                    "season" if field == "season" else
                    "difficulty" if field == "difficulty" else
                    "serve_style",
                    value,
                )
                if raw != value:
                    uncertainties.append(
                        f"{recipe_id}: {field} '{raw}' normalized to '{value}' but still not in app options"
                    )
                else:
                    uncertainties.append(
                        f"{recipe_id}: {field} '{value}' not in app options and has no Enum_Normalization rule"
                    )

        subfamily = cocktail.get("subFamily", "")
        if subfamily:
            rule = enum_rules.get("subFamily", {}).get(subfamily, "")
            if rule == "future_or_display_only":
                uncertainties.append(
                    f"{recipe_id}: subFamily '{subfamily}' is display-only and may not resolve in Families tab"
                )

        raw_tags = parse_tags(recipe.get("tags", ""))
        for raw_tag in raw_tags:
            if raw_tag in tag_map:
                continue
            if raw_tag not in APP_TAGS:
                uncertainties.append(
                    f"{recipe_id}: tag '{raw_tag}' has no Tag_Normalization rule and is not in app CHAR_TAGS"
                )

        for tag in cocktail.get("tags", []):
            if tag not in APP_TAGS:
                uncertainties.append(f"{recipe_id}: exported tag '{tag}' not in app CHAR_TAGS")

        if not cocktail.get("instructions"):
            uncertainties.append(f"{cid}: exported cocktail has empty instructions")
        if not cocktail.get("ingredients"):
            uncertainties.append(f"{cid}: exported cocktail has no ingredients")

    return uncertainties


def export_workbook(
    workbook_path: Path = DEFAULT_WORKBOOK,
    output_path: Path = DEFAULT_OUTPUT,
    *,
    export_ready_only: bool = True,
) -> dict:
    sheets = load_workbook_sheets(workbook_path)

    recipes = sheets.get("Recipes", [])
    export_rows = sheets.get("App_JSON_Export", [])
    ingredients_all = sheets.get("Recipe_Ingredients", [])
    steps_all = sheets.get("Steps", [])
    lore_all = sheets.get("Lore", [])
    enum_maps, enum_rules = load_enum_normalization(sheets.get("Enum_Normalization", []))
    tag_map, _tag_rules = load_tag_normalization(sheets.get("Tag_Normalization", []))

    export_ready_by_snake: dict[str, str] = {}
    export_notes_by_snake: dict[str, str] = {}
    for row in export_rows:
        snake_id = kebab_to_snake(row.get("id", "").strip())
        if snake_id:
            export_ready_by_snake[snake_id] = row.get("export_ready", "").strip().upper()
            export_notes_by_snake[snake_id] = row.get("export_notes", "").strip()

    ingredients_by_recipe: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ingredients_all:
        ingredients_by_recipe[row.get("recipe_id", "")].append(row)

    steps_by_recipe: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in steps_all:
        steps_by_recipe[row.get("recipe_id", "")].append(row)

    lore_by_recipe = {row.get("recipe_id", ""): row for row in lore_all if row.get("recipe_id")}

    exported: list[dict] = []
    skipped: list[dict[str, str]] = []

    for recipe in recipes:
        recipe_id = recipe.get("recipe_id", "").strip()
        if not recipe_id:
            skipped.append({"recipe_id": "", "name": recipe.get("name", ""), "reason": "missing recipe_id"})
            continue

        export_ready = export_ready_by_snake.get(recipe_id, "")
        if export_ready_only and export_ready != "YES":
            reason = "export_ready is not YES"
            notes = export_notes_by_snake.get(recipe_id, "")
            if notes:
                reason = f"{reason} ({notes})"
            elif recipe_id not in export_ready_by_snake:
                reason = "missing App_JSON_Export row"
            skipped.append(
                {
                    "recipe_id": recipe_id,
                    "name": recipe.get("name", ""),
                    "reason": reason,
                }
            )
            continue

        cocktail = build_cocktail(
            recipe,
            build_ingredients(ingredients_by_recipe.get(recipe_id, [])),
            steps_by_recipe.get(recipe_id, []),
            lore_by_recipe.get(recipe_id),
            enum_maps=enum_maps,
            enum_rules=enum_rules,
            tag_map=tag_map,
        )
        exported.append(cocktail)

    exported.sort(key=lambda item: item["name"].lower())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"cocktails": exported, "inventory": []}
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    recipes_by_id = {r["recipe_id"]: r for r in recipes if r.get("recipe_id")}
    uncertainties = collect_mapping_uncertainties(
        exported,
        recipes_by_id,
        enum_rules=enum_rules,
        tag_map=tag_map,
    )

    return {
        "workbook": str(workbook_path),
        "output": str(output_path),
        "exported_count": len(exported),
        "skipped_count": len(skipped),
        "total_recipes": len(recipes),
        "skipped": skipped,
        "uncertainties": uncertainties,
        "normalization": {
            "enum_rules_loaded": sum(len(v) for v in enum_maps.values()),
            "tag_rules_loaded": len(tag_map),
        },
    }


def print_report(report: dict) -> None:
    print("Workbook export report")
    print("======================")
    print(f"Workbook: {report['workbook']}")
    print(f"Output:   {report['output']}")
    print(f"Total recipes in workbook: {report['total_recipes']}")
    print(f"Exported: {report['exported_count']}")
    print(f"Skipped:  {report['skipped_count']}")
    norm = report.get("normalization", {})
    if norm:
        print(f"Normalization rules loaded: {norm.get('enum_rules_loaded', 0)} enum, {norm.get('tag_rules_loaded', 0)} tag")
    print()

    if report["skipped"]:
        print("Skipped recipes:")
        for item in report["skipped"]:
            print(f"  - {item['recipe_id']} | {item['name']} | {item['reason']}")
        print()

    if report["uncertainties"]:
        print(f"Mapping uncertainties ({len(report['uncertainties'])}):")
        for note in report["uncertainties"]:
            print(f"  - {note}")
    else:
        print("Mapping uncertainties: none flagged")


def main(argv: list[str]) -> int:
    workbook = Path(argv[1]) if len(argv) > 1 else DEFAULT_WORKBOOK
    output = Path(argv[2]) if len(argv) > 2 else DEFAULT_OUTPUT

    if not workbook.exists():
        print(f"Workbook not found: {workbook}", file=sys.stderr)
        return 1

    report = export_workbook(workbook, output)
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
