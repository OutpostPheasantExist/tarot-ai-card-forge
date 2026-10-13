"""Draw engine — turns a question + spread into cards + AI art prompts.

This is the seam where the tarot domain meets the diffusion backend.
The engine never touches the GPU directly; it emits RenderJob objects
that services/renderer.py consumes.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from tarot_forge.core.deck import Card, Deck
from tarot_forge.core.spread import Spread


@dataclass(frozen=True)
class DrawResult:
    card: Card
    reversed: bool
    slot_id: str
    prompt: str


@dataclass(frozen=True)
class RenderJob:
    job_id: str
    question: str
    spread: Spread
    draws: tuple[DrawResult, ...]
    seed: int


class DrawEngine:
    def __init__(self, deck: Deck, style_suffix: str = "ethereal oil painting, gold leaf, 4k") -> None:
        self._deck = deck
        self._style_suffix = style_suffix

    def draw(self, question: str, spread: Spread, seed: int | None = None) -> RenderJob:
        if spread.card_count > len(self._deck):
            raise ValueError(
                f"spread {spread.spread_id} needs {spread.card_count} cards; deck has {len(self._deck)}"
            )
        shuffled = self._deck.shuffled(seed=seed, allow_reversed=True)
        draws: list[DrawResult] = []
        for slot, (card, is_rev) in zip(spread.slots, shuffled):
            draws.append(
                DrawResult(
                    card=card,
                    reversed=is_rev,
                    slot_id=slot.slot_id,
                    prompt=self._build_prompt(card, is_rev, slot.label),
                )
            )
        job_seed = seed if seed is not None else int(hashlib.sha1(question.encode()).hexdigest()[:8], 16)
        job_id = hashlib.sha1(f"{question}|{spread.spread_id}|{job_seed}".encode()).hexdigest()[:12]
        return RenderJob(
            job_id=job_id,
            question=question,
            spread=spread,
            draws=tuple(draws),
            seed=job_seed,
        )

    def _build_prompt(self, card: Card, reversed_: bool, slot_label: str) -> str:
        orientation = "reversed, inverted composition" if reversed_ else "upright"
        return (
            f"{card.art_prompt}, {orientation}, placed as '{slot_label}' in a tarot spread, "
            f"{self._style_suffix}"
        )