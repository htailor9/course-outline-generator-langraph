"""Run report: tokens, calls, fallbacks, invariants, pacing."""

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


def build_report(final: dict, provider: str, wall_ms: int) -> dict:
    calls = [r for r in final.get("report", []) if "prompt_tokens" in r]
    flags = Counter(f for lo in final["los"].values() for f in lo.get("flags", []))
    enforcement = next(
        (
            r["enforcement_log"]
            for r in final.get("report", [])
            if "enforcement_log" in r
        ),
        "",
    )
    out = final.get("outline", {})
    return {
        "provider": provider,
        "n_los": len(final["los"]),
        "llm_calls": len(calls),
        "errors": [r for r in final.get("report", []) if "error" in r],
        "prompt_tokens": sum(c["prompt_tokens"] for c in calls),
        "completion_tokens": sum(c["completion_tokens"] for c in calls),
        "max_prompt_tokens": max((c["prompt_tokens"] for c in calls), default=0),
        "by_node": {
            n: {
                "calls": sum(1 for c in calls if c["role"] == n),
                "prompt_tokens": sum(
                    c["prompt_tokens"] for c in calls if c["role"] == n
                ),
            }
            for n in sorted({c["role"] for c in calls})
        },
        "fallbacks": dict(flags),
        "validation": final.get("validation", []),
        "enforcement_log": enforcement,
        "pacing": {
            k: out.get(k)
            for k in (
                "total_lesson_days",
                "total_chapters",
                "pacing_overrun",
                "pacing_overrun_lesson_days",
            )
        },
        "wall_ms": wall_ms,
    }


def make_run_dir(
    root: Path,
    course_title: str,
    provider: str,
    n_los: int | None = None,
    started: datetime | None = None,
) -> tuple[Path, str]:
    """runs/<YYYYMMDD-HHMMSS>_<N>LOs_<course-slug>_<provider>/ — one folder per run."""
    started = started or datetime.now()
    slug = re.sub(r"[^A-Za-z0-9]+", "-", course_title).strip("-")[:40] or "course"
    count = f"{n_los}LOs_" if n_los is not None else ""
    run_id = f"{started.strftime('%Y%m%d-%H%M%S')}_{count}{slug}_{provider}"
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir, run_id


def write(
    out_dir: Path,
    final: dict,
    provider: str,
    wall_ms: int,
    input_payload: dict | None = None,
    run_id: str | None = None,
    settings=None,
) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    if input_payload is not None:
        (out_dir / "input.json").write_text(
            json.dumps(input_payload, indent=2), encoding="utf-8"
        )
    (out_dir / "outline.json").write_text(
        json.dumps(final["outline"], indent=2), encoding="utf-8"
    )
    rep = build_report(final, provider, wall_ms)
    rep["run_id"] = run_id or out_dir.name
    rep["started_at"] = datetime.now().isoformat(timespec="seconds")
    (out_dir / "report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    (out_dir / "enforcement.log").write_text(rep["enforcement_log"], encoding="utf-8")
    if settings is not None:
        from outline.analysis import build_analysis

        (out_dir / "analysis.md").write_text(
            build_analysis(rep["run_id"], input_payload or {}, final, rep, settings),
            encoding="utf-8",
        )
    return rep
