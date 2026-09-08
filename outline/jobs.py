"""In-memory async job registry for the REST API.

Jobs run on a dedicated background event-loop THREAD owned by the registry, so they are
independent of the server's request lifecycle (request-scoped task groups can cancel tasks
created on the request loop — observed as CancelledError under the ASGI test transport).

A job id equals the run-folder name where possible, so completed work survives server
restarts: status() serves live jobs from memory; resolve() falls back to folder-exists=done.
MVP limits (documented): single-process registry — run uvicorn with one worker.
"""

from __future__ import annotations

import asyncio
import threading
from pathlib import Path
from typing import Coroutine


class JobRegistry:
    def __init__(self) -> None:
        self._jobs: dict[str, dict] = {}
        self._loop: asyncio.AbstractEventLoop | None = None
        self._lock = threading.Lock()

    def _ensure_loop(self) -> asyncio.AbstractEventLoop:
        with self._lock:
            if self._loop is None or self._loop.is_closed():
                loop = asyncio.new_event_loop()
                threading.Thread(
                    target=loop.run_forever, name="outline-jobs", daemon=True
                ).start()
                self._loop = loop
            return self._loop

    def submit(self, run_id: str, coro: Coroutine) -> str:
        """Run the coroutine on the registry's own loop; it must return (run_dir, report)."""
        entry: dict = {"status": "queued"}
        self._jobs[run_id] = entry

        async def _wrap():
            entry["status"] = "running"
            try:
                run_dir, report = await coro
                entry.update(
                    {"status": "done", "run_dir": str(run_dir), "report": report}
                )
            except (
                BaseException
            ) as exc:  # SystemExit (guard/selection) carries the message too
                entry.update(
                    {"status": "failed", "error": str(exc) or type(exc).__name__}
                )

        asyncio.run_coroutine_threadsafe(_wrap(), self._ensure_loop())
        return run_id

    def status(self, job_id: str) -> dict:
        entry = self._jobs.get(job_id)
        if entry is None:
            return {"status": "unknown"}
        out = {"status": entry["status"]}
        for k in ("run_dir", "report", "error"):
            if k in entry:
                out[k] = entry[k]
        return out

    def resolve(self, run_id: str, runs_dir: Path) -> dict:
        """Status for any id, including runs from before this process started."""
        st = self.status(run_id)
        if st["status"] != "unknown":
            return st
        folder = Path(runs_dir) / run_id
        if (folder / "report.json").exists():
            return {"status": "done", "run_dir": str(folder)}
        return {"status": "unknown"}


registry = JobRegistry()
