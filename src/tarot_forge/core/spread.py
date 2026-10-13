"""Spread geometry — named layouts that place drawn cards on a canvas."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Slot:
    slot_id: str
    label: str
    x: float
    y: float
    rotation: float = 0.0


@dataclass(frozen=True)
class Spread:
    spread_id: str
    name: str
    slots: tuple[Slot, ...]

    @property
    def card_count(self) -> int:
        return len(self.slots)


CELTIC_CROSS = Spread(
    spread_id="celtic-cross",
    name="Celtic Cross",
    slots=(
        Slot("present", "Present", 0.50, 0.50),
        Slot("challenge", "Challenge", 0.50, 0.50, rotation=90.0),
        Slot("foundation", "Foundation", 0.50, 0.72),
        Slot("past", "Recent Past", 0.28, 0.50),
        Slot("crown", "Crown", 0.50, 0.28),
        Slot("future", "Near Future", 0.72, 0.50),
        Slot("self", "Self", 0.86, 0.72),
        Slot("environment", "Environment", 0.86, 0.58),
        Slot("hopes", "Hopes & Fears", 0.86, 0.44),
        Slot("outcome", "Outcome", 0.86, 0.30),
    ),
)

THREE_CARD = Spread(
    spread_id="three-card",
    name="Past / Present / Future",
    slots=(
        Slot("past", "Past", 0.25, 0.50),
        Slot("present", "Present", 0.50, 0.50),
        Slot("future", "Future", 0.75, 0.50),
    ),
)

BUILTIN_SPREADS: dict[str, Spread] = {
    s.spread_id: s for s in (CELTIC_CROSS, THREE_CARD)
}