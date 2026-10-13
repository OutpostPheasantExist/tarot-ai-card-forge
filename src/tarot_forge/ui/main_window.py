"""Main window — question box, spread picker, render grid, history pane."""
from __future__ import annotations

from tarot_forge.config.settings import ForgeSettings
from tarot_forge.core.draw_engine import DrawEngine
from tarot_forge.handlers.deck_handler import load_deck
from tarot_forge.handlers.reading_handler import ReadingHandler
from tarot_forge.services.model_loader import ModelLoader
from tarot_forge.services.renderer import Renderer
from tarot_forge.utils.logging_setup import get_logger

log = get_logger("tarot_forge.ui.main_window")


def launch(settings: ForgeSettings, loader: ModelLoader) -> int:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        log.error("PySide6 not installed; rerun with --headless or `pip install .[gui]`")
        return 3

    from tarot_forge.ui.forge_widget import ForgeWidget

    app = QApplication.instance() or QApplication([])
    deck = load_deck(settings.checkpoint_dir.parent / "decks" / "rider-waite-ai")
    engine = DrawEngine(deck, style_suffix=settings.style_suffix)
    renderer = Renderer(settings.output_dir)
    handler = ReadingHandler(engine, renderer)

    window = ForgeWidget(handler, settings)
    window.show()
    log.info("GUI up; checkpoint=%s", loader.loaded_checkpoint)
    return app.exec()