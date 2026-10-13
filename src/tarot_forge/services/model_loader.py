"""Model loader — locates and warms the diffusion checkpoint on disk.

Default backend is a local SDXL-turbo derivative fine-tuned on public
domain tarot plates. On CPU-only boxes we fall back to a 512px LCM
checkpoint; warmup is lazy so the GUI can paint first.
"""
from __future__ import annotations

from pathlib import Path

from tarot_forge.utils.logging_setup import get_logger

log = get_logger("tarot_forge.services.model_loader")

DEFAULT_CHECKPOINT = "tarot-forge-sdxl-turbo.safetensors"
FALLBACK_CHECKPOINT = "tarot-forge-lcm-512.safetensors"


class ModelLoader:
    def __init__(self, checkpoint_dir: Path) -> None:
        self._dir = checkpoint_dir
        self._loaded: str | None = None

    def resolve(self) -> Path:
        primary = self._dir / DEFAULT_CHECKPOINT
        if primary.exists():
            return primary
        fallback = self._dir / FALLBACK_CHECKPOINT
        if fallback.exists():
            return fallback
        raise FileNotFoundError(f"no checkpoint in {self._dir}")

    def warmup(self) -> None:
        path = self.resolve()
        log.info("warming checkpoint %s", path.name)
        self._loaded = path.name

    @property
    def loaded_checkpoint(self) -> str | None:
        return self._loaded