"""Pydantic schemas for on-disk deck manifests."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CardEntry(BaseModel):
    id: str
    name: str
    arcana: str = Field(pattern="^(major|minor)$")
    suit: str | None = None
    rank: int | None = None
    keywords: list[str] = Field(default_factory=list)
    art_prompt: str


class DeckManifest(BaseModel):
    deck_id: str
    name: str
    author: str = "unknown"
    cards: list[CardEntry]