"""Application bootstrap for the tarot forge desktop client.

Owns the process lifecycle: config load -> logging -> model warmup ->
Qt event loop. Exits non-zero on unrecoverable startup failure so the
NSIS installer's health check can detect a broken install.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from tarot_forge.bootstrap.cli import parse_args
from tarot_forge.config.settings import load_settings
from tarot_forge.services.model_loader import ModelLoader
from tarot_forge.utils.logging_setup import configure_logging

log = logging.getLogger("tarot_forge.bootstrap")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    settings = load_settings(args.config or Path.home() / ".tarot_forge" / "config.toml")
    configure_logging(settings.log_level, settings.log_dir)

    log.info("tarot-ai-card-forge v%s starting", settings.version)

    loader = ModelLoader(settings.checkpoint_dir)
    try:
        loader.warmup()
    except FileNotFoundError as exc:
        log.error("checkpoint missing: %s", exc)
        return 2

    if args.headless:
        from tarot_forge.services.headless_runner import run_headless
        return run_headless(settings, loader)

    from tarot_forge.ui.main_window import launch
    return launch(settings, loader)


if __name__ == "__main__":
    raise SystemExit(main())