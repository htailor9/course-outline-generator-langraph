"""Shared orchestration layer used by both the CLI and the REST API.

Everything here is transport-agnostic: no printing, no argparse, no HTTP. The CLI adds
printing/exit codes on top; the API adds job management and serialization.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Callable

from outline.graph import build_graph
from outline.prompt_guard import course_vocab_from_input, validate_user_prompt
from outline.report import make_run_dir, write

ProgressFn = Callable[[str, dict], None]


async def run_generation(
    raw: dict,
    settings,
    llm,
    runs_dir: Path,
    out: Path | None = None,
    progress: ProgressFn | None = None,
) -> tuple[Path, dict]:
    """Validate, run the full generation graph, write the run folder.

    Raises PromptRejected (a SystemExit subclass) before any model call on a bad user_prompt.
    Returns (run_dir, report).
    """
    validate_user_prompt(raw.get("user_prompt"), course_vocab_from_input(raw))
    app = build_graph(llm, settings)
    cfg = {
        "configurable": {
            "llm": llm,
            "settings": settings,
            "thread_id": f"run-{time.time_ns()}",
        },
        "max_concurrency": settings.max_concurrency,
    }
    t0 = time.perf_counter()
    async for event in app.astream(
        {"raw_input": raw}, config=cfg, stream_mode="updates"
    ):
        if progress:
            for node, update in event.items():
                progress(node, update)
    final = await app.aget_state(cfg)
    provider = getattr(llm, "provider_name", None) or settings.provider
    if out is not None:
        run_dir, run_id = Path(out), Path(out).name
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        run_dir, run_id = make_run_dir(
            Path(runs_dir),
            raw.get("course_title", "course"),
            provider,
            n_los=len(raw.get("learning_objectives", [])),
        )
    rep = write(
        run_dir,
        final.values,
        provider,
        int((time.perf_counter() - t0) * 1000),
        input_payload=raw,
        run_id=run_id,
        settings=settings,
    )
    return run_dir, rep


async def run_regeneration(
    baseline_dir: Path,
    unit: str,
    lesson: str | None,
    prompt: str | None,
    settings,
    llm,
    runs_dir: Path,
) -> tuple[Path, dict]:
    """Dispatch full / unit / lesson regeneration, write the run folder + regeneration note.

    Raises PromptRejected on a bad prompt (before any model call), SystemExit with a
    user-facing message on bad unit/lesson selection, FileNotFoundError on a bad baseline.
    Returns (run_dir, report).
    """
    from outline.regen import (
        regenerate_full,
        regenerate_lesson,
        regenerate_unit,
        write_full_regeneration_note,
        write_lesson_regeneration_note,
        write_regeneration_note,
    )

    baseline_dir = Path(baseline_dir)
    if (
        not (baseline_dir / "input.json").exists()
        or not (baseline_dir / "outline.json").exists()
    ):
        raise FileNotFoundError(
            f"baseline run folder not found or incomplete: {baseline_dir} "
            "(needs input.json + outline.json)"
        )
    baseline_input = json.loads(
        (baseline_dir / "input.json").read_text(encoding="utf-8")
    )
    validate_user_prompt(prompt, course_vocab_from_input(baseline_input))

    t0 = time.perf_counter()
    if lesson and unit.strip().lower() == "all":
        raise SystemExit("--lesson requires a specific --unit (not 'all')")
    if lesson:
        final, info, _prior = await regenerate_lesson(
            baseline_dir, unit, lesson, prompt, llm, settings
        )
        note_writer = write_lesson_regeneration_note
        slug = "lesson-" + re.sub(r"[^A-Za-z0-9]+", "-", info["lesson"]).strip("-")[:18]
    elif unit.strip().lower() == "all":
        final, info = await regenerate_full(baseline_dir, prompt, llm, settings)
        note_writer = write_full_regeneration_note
        slug = "full"
    else:
        final, info, _prior = await regenerate_unit(
            baseline_dir, unit, prompt, llm, settings
        )
        note_writer = write_regeneration_note
        slug = re.sub(r"[^A-Za-z0-9]+", "-", info["unit"]).strip("-")[:24]

    provider = getattr(llm, "provider_name", None) or settings.provider
    run_dir, run_id = make_run_dir(
        Path(runs_dir),
        f"{final['course']['course_title']}_regen-{slug}",
        provider,
        n_los=len(final["los"]),
    )
    rep = write(
        run_dir,
        final,
        provider,
        int((time.perf_counter() - t0) * 1000),
        input_payload=baseline_input,
        run_id=run_id,
        settings=settings,
    )
    note_writer(run_dir, final, info)
    return run_dir, rep
