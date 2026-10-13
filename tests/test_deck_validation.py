"""Deck validation tests — catches malformed manifests before render."""
from __future__ import annotations

from tarot_forge.core.deck import Arcana, Card, Deck
from tarot_forge.handlers.deck_handler import validate_deck


def test_duplicate_card_id_flagged():
    card = Card(
        card_id="dup",
        name="Dup",
        arcana=Arcana.MAJOR,
        suit=None,
        rank=None,
        keywords=(),
        art_prompt="x",
    )
    deck = Deck(deck_id="d", name="D", cards=[card] * 78)
    problems = validate_deck(deck)
    assert any("duplicate" in p for p in problems)
    assert any("78" in p for p in problems) is False