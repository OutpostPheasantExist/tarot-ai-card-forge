"""Logging setup — rotating file + stderr, one call per process."""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path


def configure_logging(level: str, log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(level.upper())
    fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

    fh = logging.handlers.RotatingFileHandler(
        log_dir / "tarot_forge.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    root.handlers[:] = [fh, sh]


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)