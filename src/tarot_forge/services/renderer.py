"""Renderer — queues RenderJobs and writes PNGs to the output directory.

Runs on a single worker thread by default. VRAM-bound, not CPU-bound,
so a second worker only helps on multi-GPU rigs.
"""
from __future__ import annotations

import queue
import threading
from pathlib import Path

from tarot_forge.core.draw_engine import RenderJob
from tarot_forge.utils.logging_setup import get_logger

log = get_logger("tarot_forge.services.renderer")


class Renderer:
    def __init__(self, out_dir: Path, workers: int = 1) -> None:
        self._out = out_dir
        self._out.mkdir(parents=True, exist_ok=True)
        self._q: queue.Queue[RenderJob] = queue.Queue()
        self._workers = [
            threading.Thread(target=self._loop, name=f"render-{i}", daemon=True)
            for i in range(workers)
        ]
        for w in self._workers:
            w.start()

    def submit(self, job: RenderJob) -> None:
        self._q.put(job)

    def _loop(self) -> None:
        while True:
            job = self._q.get()
            try:
                target = self._out / f"{job.job_id}.png"
                log.info("rendering %s -> %s", job.job_id, target.name)
                target.write_bytes(b"")  # placeholder written by diffusion backend
            finally:
                self._q.task_done()