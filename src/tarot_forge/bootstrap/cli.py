"""CLI surface. Subcommands mirror the GUI tabs so power users can script."""
from __future__ import annotations

import argparse
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="tarot-forge", description="AI tarot card generator")
    p.add_argument("--config", type=Path, default=None, help="path to config.toml")
    p.add_argument("--headless", action="store_true", help="run without GUI (batch render)")
    p.add_argument("--deck", default=None, help="deck preset id, e.g. rider-waite-ai")
    p.add_argument("--spread", default=None, help="spread id, e.g. celtic-cross")
    p.add_argument("--out", type=Path, default=Path("./out"), help="output directory")
    p.add_argument("--seed", type=int, default=None, help="deterministic shuffle seed")
    return p.parse_args(argv)