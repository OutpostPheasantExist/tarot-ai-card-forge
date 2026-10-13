"""Deterministic RNG helpers so readings reproduce from a seed."""
from __future__ import annotations

import hashlib
import random


def seed_from_text(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def rng_for(text: str) -> random.Random:
    return random.Random(seed_from_text(text))