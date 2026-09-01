"""Context-based unit regeneration (STUDIOPE-94).

Regenerates ONE unit of a previously generated outline, using the prior run as the baseline:
- non-target units are locked (placements, lesson names, module titles reused verbatim);
- the target unit's lessons and titles are re-planned by the LLM, with the previous version
  supplied as context and `--prompt` given user-priority;
- the whole course then re-flows through pack_and_merge -> assemble -> validate, so every
  structural guarantee (coverage, min-4, unique names, numbering) holds on the result;
- output is a NEW run folder; the baseline folder is untouched (that is the undo).
"""

from __future__ import annotations

import json
from pathlib import Path

from outline.assemble.dcim import build as build_outline
from outline.nodes import plan_chapters, titles
from outline.rules.estimates import word_limit
from outline.rules.structure import build_structure
from outline.validate.invariants import check


def load_run(run_dir: Path) -> tuple[dict, dict]:
    inp = json.loads((run_dir / "input.json").read_text(encoding="utf-8"))
    outline = json.loads((run_dir / "outline.json").read_text(encoding="utf-8"))
    return inp, outline


def state_from_outline(inp: dict, outline: dict) -> tuple[dict, dict, list, dict]:
    """Deterministically rebuild pipeline state from a prior run. No LLM involved.

    Returns (course, budget, parts, los) where parts/los carry the prior placements
    (chapter name + rank) and los[id]['title'] the prior module title.
    """
    course = {
        "course_title": inp["course_title"],
        "grade_band": inp["grade_band"],
        "subject_area": inp["subject_area"],
        "minutes_per_lesson": inp["minutes_per_lesson"],
        "lessons_per_week": inp["lessons_per_week"],
        "course_duration_weeks": inp["course_duration_weeks"],
        "progression": inp["course_outline_progression"].upper(),
        "user_prompt": None,
    }
    budget = {
        "total_lesson_days": inp["lessons_per_week"] * inp["course_duration_weeks"],
        "word_limit": word_limit(inp["grade_band"]),
    }
    los: dict[str, dict] = {}
    id_of: dict[str, str] = {}
    for i, lo in enumerate(inp["learning_objectives"]):
        lid = f"L{i + 1}"
        id_of[lo["learning_objective_urn"]] = lid
        los[lid] = {
            "id": lid,
            "urn": lo["learning_objective_urn"],
            "text": lo["objective"],
            "idx": i,
            "verb": "apply",
            "flags": [],
        }
    parts: list[dict] = []
    content = [p for p in outline["children"] if p["type"] == "understand"]
    for k, p in enumerate(content, start=1):
        pid = f"P{k}"
        ids: list[str] = []
        rank = 0
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            rank += 1
            for m in c["children"]:
                urn = m.get("learning_objective_urn")
                if not urn or urn not in id_of:
                    continue
                lid = id_of[urn]
                ids.append(lid)
                los[lid].update(
                    {
                        "primary_skill": m.get("primary_skill") or "General",
                        "tier": m.get("blooms_level") or "Foundational",
                        "part_id": pid,
                        "chapter": c["title"]["en"],
                        "rank": rank,
                        "title": m["title"]["en"],
                    }
                )
        parts.append({"part_id": pid, "part_name": p["title"]["en"], "ids": ids})
    return course, budget, parts, los


def select_unit(parts: list[dict], unit_sel: str) -> dict:
    if unit_sel.isdigit():
        i = int(unit_sel)
        if not 1 <= i <= len(parts):
            raise SystemExit(
                f"--unit {i} out of range; course has {len(parts)} content units: "
                + "; ".join(f"{n + 1}. {p['part_name']}" for n, p in enumerate(parts))
            )
        return parts[i - 1]
    match = [
        p
        for p in parts
        if p["part_name"].strip().casefold() == unit_sel.strip().casefold()
    ]
    if not match:
        raise SystemExit(
            f"--unit '{unit_sel}' not found. Units: "
            + "; ".join(f"{n + 1}. {p['part_name']}" for n, p in enumerate(parts))
        )
    return match[0]


def _regen_context(target: dict, los: dict) -> str:
    lessons = list(dict.fromkeys(los[i].get("chapter", "") for i in target["ids"]))
    mods = [los[i].get("title", "") for i in target["ids"]]
    return (
        "REGENERATION: this unit is being regenerated. Its PREVIOUS version is given below for "
        "context — produce an improved version per the user guidance; do not simply repeat it, and "
        "do not reuse a previous name unless it is clearly still the best choice.\n"
        f"PREVIOUS LESSONS: {'; '.join(n for n in lessons if n)}\n"
        f"PREVIOUS MODULE TITLES: {'; '.join(t for t in mods if t)}"
    )


async def regenerate_unit(
    run_dir: Path, unit_sel: str, prompt: str | None, llm, settings
) -> tuple[dict, dict, dict]:
    """Returns (final_state, regen_info, prior_snapshot_of_target)."""
    inp, prior = load_run(run_dir)
    course, budget, parts, los = state_from_outline(inp, prior)
    course["user_prompt"] = prompt
    target = select_unit(parts, unit_sel)
    part_names = [p["part_name"] for p in parts]
    config = {"configurable": {"llm": llm, "settings": settings}}
    context = _regen_context(target, los)
    prior_target = {
        "part_name": target["part_name"],
        "lessons": list(
            dict.fromkeys(los[i].get("chapter", "") for i in target["ids"])
        ),
        "module_titles": {i: los[i].get("title", "") for i in target["ids"]},
    }
    report: list[dict] = []

    # 1. Re-plan the target unit's lessons (other units untouched).
    ch = await plan_chapters(
        {
            "part": {k: target[k] for k in ("part_id", "part_name", "ids")},
            "los": {i: los[i] for i in target["ids"]},
            "course": course,
            "budget": budget,
            "part_names": part_names,
            "regen_context": context,
        },
        config,
    )
    report += ch["report"]
    for i, patch in ch["los"].items():
        los[i].update(patch)

    # 2. Deterministic re-flow of the WHOLE course (locked units keep prior chapter/rank).
    packed = build_structure(
        course,
        budget,
        los,
        [{"part_name": p["part_name"], "ids": p["ids"]} for p in parts],
    )

    # 3. Titles: reuse prior titles everywhere; regenerate only for packed parts containing target LOs.
    titles_map = {i: lo["title"] for i, lo in los.items() if lo.get("title")}
    target_ids = set(target["ids"])
    for p in packed["parts"]:
        p_ids = {lo["id"] for c in p["chapters"] for lo in c["learning_objectives"]}
        if not (p_ids & target_ids):
            continue
        t = await titles(
            {
                "part": p,
                "los": {i: los[i] for i in p_ids},
                "course": course,
                "budget": budget,
                "part_names": [q["part_name"] for q in packed["parts"]],
                "regen_context": context,
            },
            config,
        )
        report += t["report"]
        titles_map.update(t["titles"])
        for i, patch in t["los"].items():
            los[i].update(patch)

    outline = build_outline(course, budget, packed, titles_map)
    validation = check(outline, [lo["urn"] for lo in los.values()])
    structural = [
        e for e in validation if not e.startswith(("TITLES", "LIMITS", "NAMES"))
    ]
    if structural:
        raise RuntimeError(f"regeneration produced structural failures: {structural}")
    report.append(
        {"node": "pack_and_merge", "enforcement_log": packed["enforcement_log"]}
    )
    final = {
        "course": course,
        "budget": budget,
        "los": los,
        "packed": packed,
        "titles": titles_map,
        "outline": outline,
        "validation": validation,
        "report": report,
    }
    info = {
        "baseline": str(run_dir),
        "unit": target["part_name"],
        "prompt": prompt,
        "prior": prior_target,
    }
    return final, info, prior_target


def write_regeneration_note(out_dir: Path, final: dict, info: dict) -> None:
    prior = info["prior"]
    new_lessons: list[str] = []
    new_titles: dict[str, str] = {}
    prior_ids = set(prior["module_titles"])
    for p in final["packed"]["parts"]:
        for c in p["chapters"]:
            for lo in c["learning_objectives"]:
                if lo["id"] in prior_ids:
                    if c["chapter_name"] not in new_lessons:
                        new_lessons.append(c["chapter_name"])
                    new_titles[lo["id"]] = final["titles"].get(lo["id"], "")
    changed = sum(
        1
        for i in prior_ids
        if new_titles.get(i, "") != prior["module_titles"].get(i, "")
    )
    lines = [
        f"# Regeneration — unit '{info['unit']}'",
        "",
        f"- Baseline run: `{info['baseline']}` (untouched — restore by using it instead of this run)",
        f"- User prompt: {info['prompt'] or '—'}",
        f"- Validation: {final['validation'] or 'clean'}",
        "",
        "## Target unit — before vs after",
        "",
        f"- Lessons before ({len(prior['lessons'])}): " + "; ".join(prior["lessons"]),
        f"- Lessons after  ({len(new_lessons)}): " + "; ".join(new_lessons),
        f"- Module titles changed: {changed}/{len(prior_ids)}",
        "",
        "| id | before | after |",
        "| --- | --- | --- |",
    ]
    for i in sorted(prior_ids, key=lambda x: int(x[1:])):
        lines.append(f"| {i} | {prior['module_titles'][i]} | {new_titles.get(i, '')} |")
    lines += [
        "",
        "All other units are locked: placements, lesson names and module titles are reused from the baseline.",
    ]
    (out_dir / "regeneration.md").write_text("\n".join(lines), encoding="utf-8")


def _full_context(outline: dict) -> str:
    """Compact summary of the previous outline for full-course regeneration prompts."""
    lines = [
        "REGENERATION: the whole course outline is being regenerated. The PREVIOUS outline is "
        "summarised below for context — produce an improved outline per the user guidance; keep "
        "what was good, do not simply repeat it, and do not reuse previous names unless they are "
        "clearly still the best choice."
    ]
    for p in outline["children"]:
        if p["type"] != "understand":
            continue
        lessons = [c["title"]["en"] for c in p["children"] if c["type"] == "understand"]
        lines.append(f"PREVIOUS UNIT '{p['title']['en']}': " + "; ".join(lessons))
    return "\n".join(lines)


async def regenerate_full(
    run_dir: Path, prompt: str | None, llm, settings
) -> tuple[dict, dict]:
    """Full-course regeneration with the previous outline passed as context to every prompt.

    Runs the normal generation graph on the baseline input, with `_regen_context` injected so
    course_header carries the previous unit/lesson structure into annotate/plan_parts/
    plan_chapters/titles. Returns (final_state, info).
    """
    from outline.graph import build_graph

    inp, prior = load_run(run_dir)
    raw = dict(inp)
    raw["user_prompt"] = prompt
    raw["_regen_context"] = _full_context(prior)
    app = build_graph(llm, settings)
    config = {
        "configurable": {
            "llm": llm,
            "settings": settings,
            "thread_id": f"regen-full-{run_dir.name}",
        },
        "max_concurrency": settings.max_concurrency,
    }
    final = await app.ainvoke({"raw_input": raw}, config=config)
    prior_units = [
        p["title"]["en"] for p in prior["children"] if p["type"] == "understand"
    ]
    new_units = [
        p["title"]["en"]
        for p in final["outline"]["children"]
        if p["type"] == "understand"
    ]
    info = {
        "baseline": str(run_dir),
        "unit": "ALL (full course)",
        "prompt": prompt,
        "prior_units": prior_units,
        "new_units": new_units,
    }
    return final, info


def write_full_regeneration_note(out_dir: Path, final: dict, info: dict) -> None:
    lines = [
        "# Full-course regeneration",
        "",
        f"- Baseline run: `{info['baseline']}` (untouched — restore by using it instead of this run)",
        f"- User prompt: {info['prompt'] or '—'}",
        f"- Validation: {final['validation'] or 'clean'}",
        "- The previous outline's unit/lesson structure was passed as context to every planning prompt.",
        "",
        "## Units — before vs after",
        "",
        f"- Before ({len(info['prior_units'])}): " + "; ".join(info["prior_units"]),
        f"- After  ({len(info['new_units'])}): " + "; ".join(info["new_units"]),
    ]
    (out_dir / "regeneration.md").write_text("\n".join(lines), encoding="utf-8")


NON_REGENERABLE_LESSON_TYPES = {
    "introduction",
    "overview",
    "apply",
    "review",
    "test",
    "semester_review",
    "semester_exam",
}


def select_lesson(packed_part: dict, lesson_sel: str) -> dict:
    """Pick one understand lesson of a packed unit by 1-based number or exact name.

    Structural lessons (Introduction, Apply, Review, Test, Semester ...) are not regenerable
    (STUDIOPE-94 exclusions) and are not offered.
    """
    lessons = packed_part["chapters"]  # packed parts hold understand lessons only
    if lesson_sel.isdigit():
        i = int(lesson_sel)
        if not 1 <= i <= len(lessons):
            raise SystemExit(
                f"--lesson {i} out of range; unit '{packed_part['part_name']}' has {len(lessons)} "
                "regenerable (understand) lessons: "
                + "; ".join(
                    f"{n + 1}. {c['chapter_name']}" for n, c in enumerate(lessons)
                )
            )
        return lessons[i - 1]
    match = [
        c
        for c in lessons
        if c["chapter_name"].strip().casefold() == lesson_sel.strip().casefold()
    ]
    if not match:
        raise SystemExit(
            f"--lesson '{lesson_sel}' not found in unit '{packed_part['part_name']}'. "
            "Regenerable lessons: "
            + "; ".join(f"{n + 1}. {c['chapter_name']}" for n, c in enumerate(lessons))
            + ". Introduction/Apply/Review/Test/Semester lessons cannot be regenerated."
        )
    return match[0]


async def regenerate_lesson(
    run_dir: Path, unit_sel: str, lesson_sel: str, prompt: str | None, llm, settings
) -> tuple[dict, dict, dict]:
    """Lesson-level regeneration (STUDIOPE-94): re-title the modules of ONE lesson.

    LG alignment, placements, lesson/unit names and every other title are locked; only the
    selected lesson's module titles are regenerated (previous titles passed as context).
    """
    from outline.nodes import titles as titles_node

    inp, prior = load_run(run_dir)
    course, budget, parts, los = state_from_outline(inp, prior)
    course["user_prompt"] = prompt
    target_unit = select_unit(parts, unit_sel)
    config = {"configurable": {"llm": llm, "settings": settings}}

    # Deterministic re-flow with EVERYTHING locked (prior chapter/rank reused for all units).
    packed = build_structure(
        course,
        budget,
        los,
        [{"part_name": p["part_name"], "ids": p["ids"]} for p in parts],
    )
    packed_part = next(
        p for p in packed["parts"] if p["part_name"] == target_unit["part_name"]
    )
    lesson = select_lesson(packed_part, lesson_sel)
    lesson_ids = [lo["id"] for lo in lesson["learning_objectives"]]
    prior_titles = {i: los[i].get("title", "") for i in lesson_ids}

    context = (
        "REGENERATION: ONLY the module titles of this one lesson are being regenerated — "
        "produce improved titles per the user guidance; do not simply repeat the previous ones.\n"
        f"TARGET LESSON: {lesson['chapter_name']}\n"
        f"PREVIOUS MODULE TITLES: {'; '.join(t for t in prior_titles.values() if t)}"
    )
    mini_part = {
        "part_name": packed_part["part_name"],
        "part_number": packed_part["part_number"],
        "chapters": [lesson],
    }
    t = await titles_node(
        {
            "part": mini_part,
            "los": {i: los[i] for i in lesson_ids},
            "course": course,
            "budget": budget,
            "part_names": [p["part_name"] for p in packed["parts"]],
            "regen_context": context,
        },
        config,
    )
    titles_map = {i: lo["title"] for i, lo in los.items() if lo.get("title")}
    titles_map.update(t["titles"])
    for i, patch in t["los"].items():
        los[i].update(patch)

    outline = build_outline(course, budget, packed, titles_map)
    validation = check(outline, [lo["urn"] for lo in los.values()])
    structural = [
        e for e in validation if not e.startswith(("TITLES", "LIMITS", "NAMES"))
    ]
    if structural:
        raise RuntimeError(
            f"lesson regeneration produced structural failures: {structural}"
        )
    final = {
        "course": course,
        "budget": budget,
        "los": los,
        "packed": packed,
        "titles": titles_map,
        "outline": outline,
        "validation": validation,
        "report": t["report"]
        + [{"node": "pack_and_merge", "enforcement_log": packed["enforcement_log"]}],
    }
    info = {
        "baseline": str(run_dir),
        "unit": target_unit["part_name"],
        "lesson": lesson["chapter_name"],
        "prompt": prompt,
        "prior_titles": prior_titles,
    }
    return final, info, {"module_titles": prior_titles}


def write_lesson_regeneration_note(out_dir: Path, final: dict, info: dict) -> None:
    lines = [
        f"# Lesson regeneration — '{info['lesson']}' (unit '{info['unit']}')",
        "",
        f"- Baseline run: `{info['baseline']}` (untouched — restore by using it instead of this run)",
        f"- User prompt: {info['prompt'] or '—'}",
        f"- Validation: {final['validation'] or 'clean'}",
        "- Scope: module titles of this one lesson only; placements, lesson/unit names and all",
        "  other titles are locked to the baseline.",
        "",
        "| id | before | after |",
        "| --- | --- | --- |",
    ]
    for i in sorted(info["prior_titles"], key=lambda x: int(x[1:])):
        lines.append(
            f"| {i} | {info['prior_titles'][i]} | {final['titles'].get(i, '')} |"
        )
    (out_dir / "regeneration.md").write_text("\n".join(lines), encoding="utf-8")
