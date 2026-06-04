# liquid-alchemy

A cocktail compendium — curated recipes, liquor-cabinet inventory, craft preparations, and cocktail-family education.

The application is a single-file React SPA (`app.jsx`) intended for a host environment that provides persistent **`window.storage`** (e.g. Claude Artifact).

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/architecture.md](docs/architecture.md) | System design, data model, persistence |
| [docs/project-map.md](docs/project-map.md) | Internal map of `app.jsx` (sections, components, lines) |
| [docs/refactor-plan.md](docs/refactor-plan.md) | Phased plan for maintainability and modularization |
| [docs/DATA-CONTRIBUTING.md](docs/DATA-CONTRIBUTING.md) | How to add canonical recipes in source |
| [AGENTS.md](AGENTS.md) | Guide for contributors and AI assistants (task routing) |

An older overview also exists at [ARCHITECTURE.md](ARCHITECTURE.md) in the repo root; **prefer `docs/architecture.md`** for up-to-date structure.

## Contributing recipes

See **[docs/DATA-CONTRIBUTING.md](docs/DATA-CONTRIBUTING.md)**. Summary: define a constant in the My Recipes section of `app.jsx`, then register it in `MY_RECIPES_LIST`.

## Status

Phase 0 (docs and indexing) is in place. Refactor work that splits `app.jsx` is described in [docs/refactor-plan.md](docs/refactor-plan.md) and not required to run the app today.
