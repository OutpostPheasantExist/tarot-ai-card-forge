"""Reading handler — orchestrates a full question->spread->render flow."""
from __future__ import annotations

from tarot_forge.core.draw_engine import DrawEngine, RenderJob
from tarot_forge.core.spread import BUILTIN_SPREADS, Spread
from tarot_forge.services.renderer import Renderer
from tarot_forge.utils.logging_setup import get_logger

log = get_logger("tarot_forge.handlers.reading")


class ReadingHandler:
    def __init__(self, engine: DrawEngine, renderer: Renderer) -> None:
        self._engine = engine
        self._renderer = renderer

    def resolve_spread(self, spread_id: str) -> Spread:
        try:
            return BUILTIN_SPREADS[spread_id]
        except KeyError as exc:
            raise ValueError(f"unknown spread: {spread_id}") from exc

    def run(self, question: str, spread_id: str, seed: int | None = None) -> RenderJob:
        spread = self.resolve_spread(spread_id)
        job = self._engine.draw(question=question, spread=spread, seed=seed)
        log.info("job %s: %d cards drawn for %r", job.job_id, len(job.draws), question)
        self._renderer.submit(job)
        return job