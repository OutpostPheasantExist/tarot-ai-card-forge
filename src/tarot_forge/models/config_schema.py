"""Config schema — mirrors config.toml fields."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class ForgeSettings(BaseModel):
    version: str = "0.4.2"
    log_level: str = "INFO"
    log_dir: Path = Path("./logs")
    checkpoint_dir: Path = Path("./models")
    output_dir: Path = Path("./out")
    default_spread: str = "three-card"
    style_suffix: str = "ethereal oil painting, gold leaf, 4k"