"""Draw engine contract tests."""
from __future__ import annotations

from tarot_forge.core.deck import Arcana, Card, Deck
from tarot_forge.core.draw_engine import DrawEngine
from tarot_forge.core.spread import CELTIC_CROSS, THREE_CARD


def _deck() -> Deck:
    cards = [
        Card(
            card_id=f"c{i}",
            name=f"Card {i}",
            arcana=Arcana.MAJOR,
            suit=None,
            rank=None,
            keywords=("test",),
            art_prompt="a card",
        )
        for i in range(78)
    ]
    return Deck(deck_id="t", name="Test", cards=cards)


def test_three_card_draw_is_deterministic():
    engine = DrawEngine(_deck())
    a = engine.draw("q", THREE_CARD, seed=6767)
    b = engine.draw("q", THREE_CARD, seed=6767)
    assert [d.card.card_id for d in a.draws] == [d.card.card_id for d in b.draws]
    assert [d.reversed for d in a.draws] == [d.reversed for d in b.draws]


def test_celtic_cross_uses_ten_cards():
    job = DrawEngine(_deck()).draw("q", CELTIC_CROSS, seed=1)
    assert len(job.draws) == 10
    assert {d.slot_id for d in job.draws} == {s.slot_id for s in CELTIC_CROSS.slots}