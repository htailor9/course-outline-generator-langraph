"""Human-readable analysis of one run: structure, LLM calls, quality signals, pacing."""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime


def _table(headers: list[str], rows: list[list]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join([head, sep, *body])


def _structure_rows(outline: dict) -> tuple[list[list], dict]:
    rows, totals = [], Counter()
    for p in outline["children"]:
        kinds = Counter(c["type"] for c in p["children"])
        n_mod = sum(len(c["children"]) for c in p["children"])
        n_lo = sum(
            1
            for c in p["children"]
            for m in c["children"]
            if m.get("learning_objective_urn")
        )
        mins = sum(c.get("chapter_estimated_time_minutes") or 0 for c in p["children"])
        words = sum(c.get("chapter_estimated_word_count") or 0 for c in p["children"])
        totals["chapters"] += len(p["children"])
        totals["modules"] += n_mod
        totals["los"] += n_lo
        totals["minutes"] += mins
        totals["words"] += words
        rows.append(
            [
                p["part_number"],
                p["type"],
                p["title"]["en"],
                len(p["children"]),
                kinds.get("understand", 0),
                n_mod,
                n_lo,
                words,
                mins,
            ]
        )
    return rows, totals


def _chapter_rows(
    outline: dict, minutes_per_lesson: int, word_limit: int
) -> list[list]:
    rows = []
    for p in outline["children"]:
        if p["type"] != "understand":
            continue
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            t, w = (
                c["chapter_estimated_time_minutes"],
                c["chapter_estimated_word_count"],
            )
            flag = (
                "⚠ over"
                if (t or 0) > minutes_per_lesson or (w or 0) > word_limit
                else ""
            )
            titles = "; ".join(m["title"]["en"] for m in c["children"])
            rows.append(
                [
                    p["part_number"],
                    c["chapter_number"],
                    c["title"]["en"],
                    len(c["children"]),
                    w,
                    t,
                    flag,
                    titles,
                ]
            )
    return rows


def _tier_mix(los: dict) -> Counter:
    return Counter(lo.get("tier", "?") for lo in los.values())


def _skill_stats(los: dict) -> tuple[int, list[tuple[str, int]]]:
    c = Counter(lo.get("primary_skill", "?") for lo in los.values())
    return len(c), c.most_common(10)


def _title_quality(outline: dict) -> dict:
    titles = [
        m["title"]["en"]
        for p in outline["children"]
        for c in p["children"]
        for m in c["children"]
        if m.get("learning_objective_urn")
    ]
    lens = [len(t.split()) for t in titles]
    generic = re.compile(r"(?i)\b(module|activity|practice|lesson|part)\b")
    return {
        "count": len(titles),
        "distinct": len({t.casefold() for t in titles}),
        "avg_words": round(sum(lens) / len(lens), 2) if lens else 0,
        "outside_2_5_words": sum(1 for n in lens if n < 2 or n > 5),
        "generic_word_hits": sum(1 for t in titles if generic.search(t)),
    }


def build_analysis(
    run_id: str, input_payload: dict, final: dict, report: dict, settings
) -> str:
    outline, los = final["outline"], final["los"]
    course = final["course"]
    budget = final["budget"]
    struct_rows, totals = _structure_rows(outline)
    chapter_rows = _chapter_rows(
        outline, course["minutes_per_lesson"], budget["word_limit"]
    )
    calls = [r for r in final.get("report", []) if "prompt_tokens" in r]
    call_rows = [
        [
            i + 1,
            c.get("role"),
            c.get("part", c.get("batch", "")),
            c.get("model"),
            c["prompt_tokens"],
            c["completion_tokens"],
            c.get("ms"),
            c.get("attempt"),
        ]
        for i, c in enumerate(calls)
    ]
    n_skills, top_skills = _skill_stats(los)
    tiers = _tier_mix(los)
    tq = _title_quality(outline)
    flags = report.get("fallbacks", {})
    errors = report.get("errors", [])
    merges = [
        l
        for l in report.get("enforcement_log", "").splitlines()
        if l.startswith("MERGE")
    ]
    exceptions = [
        l
        for l in report.get("enforcement_log", "").splitlines()
        if l.startswith("EXCEPTION")
    ]
    over_limit = [r for r in chapter_rows if r[6]]
    pacing = report.get("pacing", {})
    content_parts = [p for p in outline["children"] if p["type"] == "understand"]

    verdict = []
    verdict.append(
        "✅ all invariants passed"
        if not report.get("validation")
        else f"⚠ soft invariant failures: {len(report['validation'])}"
    )
    verdict.append("✅ no LLM fallbacks" if not flags else f"⚠ fallbacks used: {flags}")
    verdict.append(
        "✅ no LLM errors" if not errors else f"❌ LLM errors: {len(errors)}"
    )
    verdict.append(
        "✅ pacing within tolerance"
        if not pacing.get("pacing_overrun")
        else f"⚠ pacing overrun by {pacing.get('pacing_overrun_lesson_days')} lesson days"
    )

    md = [
        f"# Run analysis — {run_id}",
        "",
        f"Generated {datetime.now().isoformat(timespec='seconds')} · provider **{report['provider']}** · "
        f"models `{settings.models}` · wall {report['wall_ms']/1000:.1f}s",
        "",
        "## Verdict",
        "",
        *[f"- {v}" for v in verdict],
        "",
        "## 1. Input",
        "",
        _table(
            ["field", "value"],
            [
                ["course_title", course["course_title"]],
                ["grade_band", course["grade_band"]],
                ["subject_area", course["subject_area"]],
                ["progression", course["progression"]],
                ["learning objectives", len(los)],
                [
                    "calendar",
                    f"{course['lessons_per_week']}/wk × {course['course_duration_weeks']} wk = {budget['total_lesson_days']} lesson days",
                ],
                ["minutes_per_lesson", course["minutes_per_lesson"]],
                ["chapter word limit", budget["word_limit"]],
                ["user_prompt", course.get("user_prompt") or "—"],
                [
                    "batch_size / concurrency",
                    f"{settings.batch_size} / {settings.max_concurrency}",
                ],
                [
                    "planning mode",
                    (
                        "skill-level"
                        if len(los) > settings.skill_mode_threshold
                        else "id-level"
                    ),
                ],
            ],
        ),
        "",
        "## 2. Annotation (analyser stage)",
        "",
        f"- Bloom's tier mix: "
        + ", ".join(f"{k} {v}" for k, v in sorted(tiers.items())),
        f"- Unique primary skills: **{n_skills}** (top: "
        + ", ".join(f"{s} ×{n}" for s, n in top_skills)
        + ")",
        "",
        "## 3. Output structure",
        "",
        f"- Parts: **{outline['total_parts']}** (1 overview + {len(content_parts)} content + 2 semester) · "
        f"Chapters: **{outline['total_chapters']}** · Modules: {totals['modules']} · LO modules: {totals['los']}",
        f"- Content estimate: {totals['words']} words · {totals['minutes']} minutes across understand chapters",
        f"- Min-4 merges applied: {len(merges)}"
        + (f" · exception cases: {len(exceptions)}" if exceptions else ""),
        "",
        _table(
            [
                "#",
                "type",
                "part",
                "chapters",
                "understand",
                "modules",
                "LOs",
                "words",
                "minutes",
            ],
            struct_rows,
        ),
        "",
        "### Understand chapters",
        "",
        _table(
            ["part", "ch", "chapter", "LOs", "words", "min", "limit", "module titles"],
            chapter_rows,
        ),
        "",
        f"- Chapters over minute/word limit: **{len(over_limit)}**"
        + (
            " — "
            + "; ".join(
                f"P{r[0]} C{r[1]} '{r[2]}' ({r[5]} min / {r[4]} w)"
                for r in over_limit[:10]
            )
            if over_limit
            else ""
        ),
        "",
        "## 4. Pacing",
        "",
        _table(
            ["metric", "value"],
            [
                ["total_lesson_days", pacing.get("total_lesson_days")],
                ["total_chapters", pacing.get("total_chapters")],
                [
                    "fill ratio",
                    f"{(pacing.get('total_chapters') or 0) / (pacing.get('total_lesson_days') or 1):.0%}",
                ],
                ["overrun", pacing.get("pacing_overrun")],
                ["overrun days", pacing.get("pacing_overrun_lesson_days")],
            ],
        ),
        "",
        *[f"- {n}" for n in (outline.get("split_notes") or [])],
        "",
        "## 5. LLM calls",
        "",
        _table(
            ["metric", "value"],
            [
                ["calls", report["llm_calls"]],
                ["prompt tokens", report["prompt_tokens"]],
                ["completion tokens", report["completion_tokens"]],
                ["max single prompt", report["max_prompt_tokens"]],
                [
                    "tokens per LO",
                    f"{(report['prompt_tokens'] + report['completion_tokens']) / max(1, len(los)):.1f}",
                ],
            ],
        ),
        "",
        _table(
            ["node", "calls", "prompt tokens"],
            [[n, v["calls"], v["prompt_tokens"]] for n, v in report["by_node"].items()],
        ),
        "",
        _table(
            [
                "#",
                "role",
                "part/batch",
                "model",
                "prompt",
                "completion",
                "ms",
                "attempt",
            ],
            call_rows,
        ),
        "",
        "## 6. Quality signals",
        "",
        _table(
            ["signal", "value"],
            [
                ["module titles", tq["count"]],
                ["distinct titles", tq["distinct"]],
                ["avg words per title", tq["avg_words"]],
                ["titles outside 2–5 words", tq["outside_2_5_words"]],
                ["titles with generic words", tq["generic_word_hits"]],
                ["LO fallbacks by kind", flags or "none"],
                [
                    "soft invariant failures",
                    "; ".join(report.get("validation", [])) or "none",
                ],
                [
                    "LLM errors",
                    "; ".join(str(e.get("error")) for e in errors) or "none",
                ],
            ],
        ),
        "",
        "## 7. Enforcement log",
        "",
        "```",
        report.get("enforcement_log", "").strip() or "(empty)",
        "```",
        "",
        "## 8. Files",
        "",
        "- `input.json` — request as received",
        "- `outline.json` — DCIM course outline (response)",
        "- `report.json` — machine-readable metrics",
        "- `enforcement.log` — pack/merge decisions",
        "- `analysis.md` — this file",
        "",
    ]
    return "\n".join(md)
