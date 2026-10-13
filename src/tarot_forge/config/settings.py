"""Load config.toml into ForgeSettings, falling back to defaults."""
from __future__ import annotations

import tomllib
from pathlib import Path

from tarot_forge.models.config_schema import ForgeSettings


def load_settings(path: Path) -> ForgeSettings:
    if not path.exists():
        return ForgeSettings()
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    return ForgeSettings.model_validate(raw.get("forge", {}))