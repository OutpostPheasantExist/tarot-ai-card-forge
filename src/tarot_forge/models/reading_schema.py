"""Pydantic schemas for persisted readings (history.json)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DrawnCard(BaseModel):
    slot_id: str
    card_id: str
    reversed: bool
    prompt: str


class ReadingRecord(BaseModel):
    job_id: str
    question: str
    spread_id: str
    seed: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    draws: list[DrawnCard]