# Contributing to tarot-ai-card-forge

Thanks for wanting to help the deck grow. This project ships a Windows
desktop client that draws tarot spreads and renders AI tarot art from
local diffusion checkpoints. Contributions are welcome — code, decks,
spreads, and art prompts all count.

## Ground rules

- Python 3.11+. Ruff for lint, pytest for tests. Run `ruff check src tests`
  and `pytest -q` before opening a PR.
- One PR, one concern. A new spread and a renderer refactor are two PRs.
- Deck manifests live under `decks/<deck_id>/deck.json` and must validate
  against `tarot_forge.models.deck_schema.DeckManifest`.
- Art prompts must be original or public-domain. Do not commit scraped
  card art from commercial decks.

## Adding a spread

1. Open `src/tarot_forge/core/spread.py`.
2. Add a `Spread` with `Slot` entries. Coordinates are normalized 0..1.
3. Register it in `BUILTIN_SPREADS`.
4. Add a test in `tests/` asserting `card_count` matches the slot count.

## Adding a deck

1. Create `decks/<deck_id>/deck.json` following `DeckManifest`.
2. 78 cards. Major arcana `arcana: "major"`, minor `arcana: "minor"`
   with `suit` and `rank`.
3. Provide `art_prompt` per card — this is what gets fed to the diffusion
   backend, so be specific.

## Reporting bugs

Open an issue with: Windows version, Python version, checkpoint filename,
the question you asked, the spread, and the seed. Seeds make readings
reproducible and bugs reproducible with them.

## Code style

- Type hints on public functions. `from __future__ import annotations`.
- No bare `except:`. Log and re-raise or return a typed error.
- Keep handlers free of Qt imports. Handlers are testable without a display.