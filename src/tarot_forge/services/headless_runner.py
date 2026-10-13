"""Headless batch runner — used by `--headless` and CI smoke tests."""
from __future__ import annotations

from tarot_forge.config.settings import ForgeSettings
from tarot_forge.core.draw_engine import DrawEngine
from tarot_forge.handlers.deck_handler import load_deck
from tarot_forge.handlers.reading_handler import ReadingHandler
from tarot_forge.services.model_loader import ModelLoader
from tarot_forge.services.renderer import Renderer


def run_headless(settings: ForgeSettings, loader: ModelLoader) -> int:
    deck = load_deck(settings.checkpoint_dir.parent / "decks" / "rider-waite-ai")
    engine = DrawEngine(deck, style_suffix=settings.style_suffix)
    renderer = Renderer(settings.output_dir)
    handler = ReadingHandler(engine, renderer)
    job = handler.run(question="headless smoke", spread_id=settings.default_spread, seed=6767)
    print(f"job={job.job_id} cards={len(job.draws)} checkpoint={loader.loaded_checkpoint}")
    return 0