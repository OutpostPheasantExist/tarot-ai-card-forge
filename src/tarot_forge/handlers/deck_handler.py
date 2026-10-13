"""Deck handler — load, list, and validate user decks."""
from __future__ import annotations

from pathlib import Path

from tarot_forge.core.deck import Arcana, Card, Deck, Suit
from tarot_forge.models.deck_schema import DeckManifest
from tarot_forge.utils.json_io import read_json


def load_deck(deck_dir: Path) -> Deck:
    manifest = DeckManifest.model_validate(read_json(deck_dir / "deck.json"))
    cards: list[Card] = []
    for entry in manifest.cards:
        cards.append(
            Card(
                card_id=entry.id,
                name=entry.name,
                arcana=Arcana(entry.arcana),
                suit=Suit(entry.suit) if entry.suit else None,
                rank=entry.rank,
                keywords=tuple(entry.keywords),
                art_prompt=entry.art_prompt,
            )
        )
    return Deck(deck_id=manifest.deck_id, name=manifest.name, cards=cards)


def validate_deck(deck: Deck) -> list[str]:
    problems: list[str] = []
    if len(deck) != 78:
        problems.append(f"expected 78 cards, got {len(deck)}")
    seen: set[str] = set()
    for c in deck:
        if c.card_id in seen:
            problems.append(f"duplicate card_id: {c.card_id}")
        seen.add(c.card_id)
    return problems