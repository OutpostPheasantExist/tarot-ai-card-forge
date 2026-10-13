"""Deck abstraction: 78-card tarot deck with reversals and AI-art hooks.

A Deck is immutable once loaded. Shuffling returns a new shuffled order
rather than mutating the deck, so render jobs are reproducible from a
seed.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator


class Arcana(str, Enum):
    MAJOR = "major"
    MINOR = "minor"


class Suit(str, Enum):
    WANDS = "wands"
    CUPS = "cups"
    SWORDS = "swords"
    PENTACLES = "pentacles"


@dataclass(frozen=True)
class Card:
    card_id: str
    name: str
    arcana: Arcana
    suit: Suit | None
    rank: int | None
    keywords: tuple[str, ...]
    art_prompt: str


@dataclass
class Deck:
    deck_id: str
    name: str
    cards: list[Card] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def shuffled(self, seed: int | None = None, allow_reversed: bool = True) -> list[tuple[Card, bool]]:
        rng = random.Random(seed)
        pool = list(self.cards)
        rng.shuffle(pool)
        if not allow_reversed:
            return [(c, False) for c in pool]
        return [(c, rng.random() < 0.34) for c in pool]

    def by_id(self, card_id: str) -> Card:
        for c in self.cards:
            if c.card_id == card_id:
                return c
        raise KeyError(card_id)