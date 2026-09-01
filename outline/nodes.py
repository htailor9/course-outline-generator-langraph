"""Graph nodes. LLM nodes: validate -> re-ask missing ids once -> deterministic fallback."""

from __future__ import annotations

from collections import Counter, defaultdict

from langgraph.types import Send

from outline.assemble.dcim import build as build_outline
from outline.llm import render
from outline.rules.blooms import tier_for
from outline.rules.estimates import word_limit
from outline.rules.naming import skill_key
from outline.rules.structure import build_structure
from outline.schemas import AnnotateOut, ChaptersOut, CourseRequest, PartsOut, TitlesOut
from outline.validate.invariants import BANNED, check

SKILL_SPLIT_MAX_LOS = 40  # design §5: skills with > 40 LOs are pre-split by tier, then
# any sub-group still > 40 is chunked into pieces of <= 40.

GUIDANCE = {
    "SKILLS_BASED_PROGRESSION": (
        "Progression style: SKILLS-BASED. A unit is a coherent skill domain; a chapter is a focused group of objectives "
        "sharing one primary skill. Order Foundational before Intermediate before Advanced, then by prerequisite "
        "dependency. Same skill normally means same chapter; split only when the instructional arc materially changes."
    ),
    "THEME_BASED_PROGRESSION": (
        "Progression style: THEME-BASED. A unit is one overarching theme or big idea; a chapter is a focused group of "
        "objectives exploring one aspect of that theme. A theme is a conceptual grouping, NOT a skill: different skills "
        "may share a theme. Order themes from foundational/context-setting to complex themes that build on them."
    ),
    "CHRONOLOGICAL_PROGRESSION": (
        "Progression style: CHRONOLOGICAL. Organise by the most authentic chronological progression in the discipline: "
        "historical periods, scientific process sequence, developmental stages, or natural topic sequence "
        "(e.g. Cells -> Cell Processes -> Genetics -> Evolution; Ancient -> Classical -> Middle Ages -> Modern). "
        "A unit is one period/phase/stage; a chapter is a coherent milestone within it. Prerequisites always come first."
    ),
    "STANDARDS_DRIVEN_PROGRESSION": (
        "Progression style: STANDARDS-DRIVEN. The given item order IS the standards-framework order and is FIXED. "
        "Do not reorder items by skill, tier, or your own knowledge of any framework. Walk the list from first to last "
        "and group only ADJACENT (consecutive) items: a unit is one standard domain (a contiguous run), a chapter is one "
        "cluster within it. If the same cluster reappears later, it is a separate chapter with a distinct name. "
        "order_rank must follow input position."
    ),
}


def _cfg(config):
    c = config["configurable"]
    return c["llm"], c["settings"]


def course_header(
    course: dict, budget: dict, part_names=(), this_part: str | None = None
) -> str:
    lines = [
        f"COURSE: {course['course_title']} | grade band {course['grade_band']} | {course['subject_area']} | {course['progression']}",
        f"CALENDAR: {course['lessons_per_week']} lessons/week x {course['course_duration_weeks']} weeks = "
        f"{budget['total_lesson_days']} lesson days; {course['minutes_per_lesson']} min/lesson; chapter word limit {budget['word_limit']}",
    ]
    lines.append("PROGRESSION: " + GUIDANCE[course["progression"]])
    if part_names:
        lines.append(
            "UNITS: " + " · ".join(f"{i + 1}. {n}" for i, n in enumerate(part_names))
        )
    if this_part:
        lines.append(f"THIS UNIT: {this_part}")
    if course.get("user_prompt"):
        lines.append(
            "USER GUIDANCE (takes PRIORITY over the default grouping, naming, ordering and unit-count "
            "preferences above wherever they conflict; it can NEVER override objective coverage, the "
            "fixed standards-framework order, or structural rules): "
            f"{course['user_prompt']}"
        )
    return "\n".join(lines)


# ---------------- ingest ----------------
def ingest(state: dict, config) -> dict:
    _, settings = _cfg(config)
    # Upstream fixtures (e.g. sample-input-123.json) send course_outline_progression in
    # lowercase snake_case; CourseRequest's Literal is case-sensitive uppercase. Normalize
    # casing here (mirrors outline.rules.grade_band.normalize's tolerance for raw input)
    # rather than weakening the schema's Literal contract.
    raw = state["raw_input"]
    prog = raw.get("course_outline_progression")
    if isinstance(prog, str) and prog.upper() != prog:
        raw = {**raw, "course_outline_progression": prog.upper()}
    req = CourseRequest.model_validate(raw)
    los = {
        f"L{i + 1}": {
            "id": f"L{i + 1}",
            "urn": lo.learning_objective_urn,
            "text": lo.objective,
            "idx": i,
            "flags": [],
        }
        for i, lo in enumerate(req.learning_objectives)
    }
    course = {
        "course_title": req.course_title,
        "grade_band": req.grade_band,
        "subject_area": req.subject_area,
        "minutes_per_lesson": req.minutes_per_lesson,
        "lessons_per_week": req.lessons_per_week,
        "course_duration_weeks": req.course_duration_weeks,
        "progression": req.course_outline_progression,
        "user_prompt": req.user_prompt,
    }
    budget = {
        "total_lesson_days": req.lessons_per_week * req.course_duration_weeks,
        "word_limit": word_limit(req.grade_band),
    }
    ids = list(los)
    batches = [
        ids[i : i + settings.batch_size]
        for i in range(0, len(ids), settings.batch_size)
    ]
    return {
        "course": course,
        "budget": budget,
        "los": los,
        "batches": batches,
        "parts": [],
        "titles": {},
        "report": [],
    }


# ---------------- annotate ----------------
def fan_out_annotate(state: dict) -> list[Send]:
    return [
        Send(
            "annotate",
            {
                "batch": ids,
                "los": {i: state["los"][i] for i in ids},
                "course": state["course"],
                "budget": state["budget"],
            },
        )
        for ids in state["batches"]
    ]


def _fallback_annotation(text: str) -> dict:
    words = [w.strip(".,;:()") for w in text.split()]
    verb = words[0].lower() if words else "identify"
    content = [w for w in words[1:] if len(w) > 3][:3]
    return {
        "verb": verb,
        "primary_skill": " ".join(w.title() for w in content) or "General Skill",
    }


async def annotate(payload: dict, config) -> dict:
    llm, _ = _cfg(config)
    los, batch = payload["los"], payload["batch"]
    header = course_header(payload["course"], payload["budget"])
    got: dict[str, dict] = {}
    report = []
    pending = list(batch)
    for _attempt in range(2):
        rows = "\n".join(f"{i} | {los[i]['text']}" for i in pending)
        system, user = render("annotate", header=header, rows=rows)
        try:
            out, metric = await llm.call("annotate", system, user, AnnotateOut)
            report.append({"node": "annotate", **metric})
        except Exception as exc:  # transport/schema failure → fallback below
            report.append({"node": "annotate", "error": str(exc)[:200]})
            break
        for it in out.items:
            if it.id in los and it.id not in got:
                got[it.id] = {
                    "verb": it.verb.strip().lower(),
                    "primary_skill": it.primary_skill.strip(),
                }
        pending = [i for i in batch if i not in got]
        if not pending:
            break
    patches = {}
    for i in batch:
        base = got.get(i)
        flags = []
        if base is None:
            base = _fallback_annotation(los[i]["text"])
            flags = ["annotate_fallback"]
        patches[i] = {**base, "tier": tier_for(base["verb"]), "flags": flags}
    return {"los": patches, "report": report}


# ---------------- plan_parts ----------------
SKILL_COLUMNS = "skill_id | skill | count | tiers | example"
ID_COLUMNS = "id | skill | tier"


def _skill_rows(los: dict) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Group ids by skill, then pre-split any skill with > 40 LOs per design §5:
    split into per-tier sub-groups (Foundational/Intermediate/Advanced, input order), and
    any sub-group still > 40 into chunks of <= 40 (also input order). Returns per-key row
    text (so re-asks can regenerate rows for pending keys instead of string-filtering) and
    the key -> lo-ids mapping.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    label: dict[str, str] = {}
    for lo in sorted(los.values(), key=lambda x: x["idx"]):
        k = skill_key(lo["primary_skill"])
        groups[k].append(lo["id"])
        label.setdefault(k, lo["primary_skill"])

    sub_groups: list[tuple[str, list[str]]] = (
        []
    )  # (label, ids), input order preserved throughout
    for k, ids in groups.items():
        if len(ids) <= SKILL_SPLIT_MAX_LOS:
            sub_groups.append((label[k], ids))
            continue
        by_tier: dict[str, list[str]] = defaultdict(list)
        for i in ids:
            by_tier[los[i]["tier"]].append(i)
        for tier in ("Foundational", "Intermediate", "Advanced"):
            tier_ids = by_tier.get(tier)
            if not tier_ids:
                continue
            tier_label = f"{label[k]} ({tier})"
            if len(tier_ids) <= SKILL_SPLIT_MAX_LOS:
                sub_groups.append((tier_label, tier_ids))
            else:
                for c in range(0, len(tier_ids), SKILL_SPLIT_MAX_LOS):
                    sub_groups.append(
                        (tier_label, tier_ids[c : c + SKILL_SPLIT_MAX_LOS])
                    )

    row_text: dict[str, str] = {}
    mapping: dict[str, list[str]] = {}
    for n, (lbl, ids) in enumerate(sub_groups, start=1):
        sid = f"S{n}"
        mapping[sid] = ids
        tiers = Counter(los[i]["tier"] for i in ids)
        tier_txt = "/".join(f"{t[:3]}{c}" for t, c in tiers.items())
        example = los[ids[0]]["text"][:80]
        row_text[sid] = f"{sid} | {lbl} | {len(ids)} | {tier_txt} | {example}"
    return row_text, mapping


async def plan_parts(state: dict, config) -> dict:
    llm, settings = _cfg(config)
    los, course, budget = state["los"], state["course"], state["budget"]
    header = course_header(course, budget)
    guidance = GUIDANCE[course["progression"]]
    skill_mode = len(los) > settings.skill_mode_threshold
    report = []
    if skill_mode:
        row_text, mapping = _skill_rows(los)
        all_keys = list(mapping)
        columns = SKILL_COLUMNS
    else:
        mapping = {i: [i] for i in los}
        all_keys = sorted(los, key=lambda i: los[i]["idx"])
        row_text = {
            i: f"{i} | {los[i]['primary_skill']} | {los[i]['tier']}" for i in all_keys
        }
        columns = ID_COLUMNS
    parts: list[dict] = []
    assigned: set[str] = set()
    pending = list(all_keys)
    for _attempt in range(2):
        rows = "\n".join(row_text[k] for k in pending)
        system, user = render(
            "plan_parts",
            header=header,
            guidance=guidance,
            rows=rows,
            count=str(len(pending)),
            columns=columns,
        )
        if parts:
            user += (
                "\n\nExisting units: "
                + "; ".join(p["part_name"] for p in parts)
                + "\nPlace ONLY the ids below into existing units (reuse the exact part_name) or a new unit."
            )
        try:
            out, metric = await llm.call("plan_parts", system, user, PartsOut)
            report.append({"node": "plan_parts", **metric})
        except Exception as exc:
            report.append({"node": "plan_parts", "error": str(exc)[:200]})
            break
        for item in out.parts:
            keys = [k for k in item.ids if k in mapping and k not in assigned]
            if not keys:
                continue
            existing = next(
                (p for p in parts if p["part_name"] == item.part_name), None
            )
            if existing:
                existing["keys"].extend(keys)
            else:
                parts.append({"part_name": item.part_name, "keys": keys})
            assigned.update(keys)
        pending = [k for k in all_keys if k not in assigned]
        if not pending:
            break
    fallback_flags: set[str] = set()
    if pending:
        if not parts:
            parts.append(
                {"part_name": f"{course['course_title']} Core Concepts", "keys": []}
            )
        for k in pending:
            lo_ids = mapping[k]
            sk = skill_key(los[lo_ids[0]].get("primary_skill", ""))
            target = next(
                (
                    p
                    for p in parts
                    if any(
                        skill_key(los[j].get("primary_skill", "")) == sk
                        for kk in p["keys"]
                        for j in mapping[kk]
                    )
                ),
                parts[-1],
            )
            target["keys"].append(k)
            fallback_flags.update(lo_ids)
    if course["progression"] == "STANDARDS_DRIVEN_PROGRESSION":
        # STUDIOPE-243: framework order is FIXED. Unit order = input position of each unit's
        # earliest LO, enforced in code regardless of what the model returned.
        parts.sort(
            key=lambda p: min(los[i]["idx"] for k in p["keys"] for i in mapping[k])
        )
    result_parts, patches = [], {}
    for n, p in enumerate(parts, start=1):
        pid = f"P{n}"
        ids = [i for k in p["keys"] for i in mapping[k]]
        ids.sort(key=lambda i: los[i]["idx"])
        result_parts.append({"part_id": pid, "part_name": p["part_name"], "ids": ids})
        for i in ids:
            patches[i] = {
                "part_id": pid,
                "flags": (["plan_parts_fallback"] if i in fallback_flags else []),
            }
    return {"parts": result_parts, "los": patches, "report": report}


# ---------------- plan_chapters ----------------
def fan_out_chapters(state: dict) -> list[Send]:
    names = [p["part_name"] for p in state["parts"]]
    return [
        Send(
            "plan_chapters",
            {
                "part": p,
                "los": {i: state["los"][i] for i in p["ids"]},
                "course": state["course"],
                "budget": state["budget"],
                "part_names": names,
            },
        )
        for p in state["parts"]
    ]


async def plan_chapters(payload: dict, config) -> dict:
    llm, _ = _cfg(config)
    part, los = payload["part"], payload["los"]
    header = course_header(
        payload["course"],
        payload["budget"],
        payload["part_names"],
        this_part=part["part_name"],
    )
    got: dict[str, dict] = {}
    report = []
    pending = list(part["ids"])
    for _attempt in range(2):
        rows = "\n".join(
            f"{i} | {los[i]['text']} | {los[i]['primary_skill']} | {los[i]['tier']}"
            for i in pending
        )
        system, user = render("plan_chapters", header=header, rows=rows)
        if got:
            existing = sorted({v["chapter"] for v in got.values()})
            user += (
                "\n\nExisting chapters: "
                + "; ".join(existing)
                + "\nPlace ONLY the ids below into existing chapters (reuse the exact chapter_name) or a new chapter."
            )
        try:
            out, metric = await llm.call("plan_chapters", system, user, ChaptersOut)
            report.append({"node": "plan_chapters", "part": part["part_id"], **metric})
        except Exception as exc:
            report.append(
                {
                    "node": "plan_chapters",
                    "part": part["part_id"],
                    "error": str(exc)[:200],
                }
            )
            break
        for a in out.assignments:
            if a.id in los and a.id not in got:
                got[a.id] = {"chapter": a.chapter_name.strip(), "rank": a.order_rank}
        pending = [i for i in part["ids"] if i not in got]
        if not pending:
            break
    patches = {}
    tier_rank = {"Foundational": 1, "Intermediate": 2, "Advanced": 3}
    max_rank = max((v["rank"] for v in got.values()), default=0)
    for i in part["ids"]:
        if i in got:
            patches[i] = {**got[i], "flags": []}
        else:
            lo = los[i]
            patches[i] = {
                "chapter": lo["primary_skill"],
                "rank": max_rank + tier_rank.get(lo["tier"], 1),
                "flags": ["plan_chapters_fallback"],
            }
    if payload["course"]["progression"] == "STANDARDS_DRIVEN_PROGRESSION":
        # STUDIOPE-243: zero intra-unit reordering. Ignore model ranks: rank = input position, so the
        # downstream (rank, chapter, idx) sort yields strict input order, and a chapter whose LOs are
        # non-adjacent in the input splits into adjacent-only buckets automatically.
        for i in patches:
            patches[i]["rank"] = los[i]["idx"] + 1
    return {"los": patches, "report": report}


# ---------------- pack_and_merge ----------------
class PipelineBug(RuntimeError):
    """A structural invariant produced by code was violated — a bug, never retried."""


def pack_and_merge(state: dict, config) -> dict:
    packed = build_structure(
        state["course"], state["budget"], state["los"], state["parts"]
    )
    if not packed["validation"]["valid"]:
        raise PipelineBug(f"pack_and_merge coverage failure: {packed['validation']}")
    return {
        "packed": packed,
        "report": [
            {"node": "pack_and_merge", "enforcement_log": packed["enforcement_log"]}
        ],
    }


# ---------------- titles ----------------
def fan_out_titles(state: dict) -> list[Send]:
    names = [p["part_name"] for p in state["packed"]["parts"]]
    return [
        Send(
            "titles",
            {
                "part": p,
                "los": {
                    lo["id"]: state["los"][lo["id"]]
                    for c in p["chapters"]
                    for lo in c["learning_objectives"]
                },
                "course": state["course"],
                "budget": state["budget"],
                "part_names": names,
            },
        )
        for p in state["packed"]["parts"]
    ]


def _fallback_title(lo: dict) -> str:
    skill = lo.get("primary_skill", "Concept")
    title = f"{skill}: {lo.get('verb', 'apply').title()}"
    if BANNED.search(title):
        title = f"{skill} Skills"
    if BANNED.search(title):
        title = f"{skill} Concept {lo.get('id', '')}"
    return title


async def titles(payload: dict, config) -> dict:
    llm, _ = _cfg(config)
    part, los = payload["part"], payload["los"]
    header = course_header(
        payload["course"],
        payload["budget"],
        payload["part_names"],
        this_part=part["part_name"],
    )
    chapter_of = {
        lo["id"]: c["chapter_name"]
        for c in part["chapters"]
        for lo in c["learning_objectives"]
    }
    ids = list(chapter_of)
    got: dict[str, str] = {}
    report = []
    pending = ids
    for _attempt in range(2):
        rows = "\n".join(
            f"{chapter_of[i]} | {i} | {los[i]['text']} | {los[i]['primary_skill']}"
            for i in pending
        )
        system, user = render("titles", header=header, rows=rows)
        try:
            out, metric = await llm.call("titles", system, user, TitlesOut)
            report.append({"node": "titles", "part": part["part_number"], **metric})
        except Exception as exc:
            report.append(
                {"node": "titles", "part": part["part_number"], "error": str(exc)[:200]}
            )
            break
        for t in out.modules:
            if t.id in chapter_of and t.id not in got:
                got[t.id] = t.title.strip()
        # reject duplicates within a chapter and titles equal to the chapter name
        seen: dict[str, set[str]] = defaultdict(set)
        for i in ids:
            if i in got:
                key = got[i].casefold()
                if (
                    key == chapter_of[i].casefold()
                    or key in seen[chapter_of[i]]
                    or BANNED.search(got[i])
                ):
                    del got[i]
                else:
                    seen[chapter_of[i]].add(key)
        pending = [i for i in ids if i not in got]
        if not pending:
            break
    result, patches = {}, {}
    used: dict[str, set[str]] = defaultdict(set)
    for i in ids:
        title = got.get(i)
        flags = []
        if title is None:
            title = _fallback_title(los[i])
            flags = ["titles_fallback"]
        base, n = title, 2
        while (
            title.casefold() in used[chapter_of[i]]
            or title.casefold() == chapter_of[i].casefold()
        ):
            title = f"{base} ({los[i]['id']})" if n == 2 else f"{base} {n}"
            n += 1
        used[chapter_of[i]].add(title.casefold())
        result[i] = title
        patches[i] = {"title": title, "flags": flags}
    return {"titles": result, "los": patches, "report": report}


# ---------------- assemble / validate ----------------
def assemble(state: dict, config) -> dict:
    return {
        "outline": build_outline(
            state["course"], state["budget"], state["packed"], state["titles"]
        )
    }


SOFT_INVARIANT_PREFIXES = ("TITLES", "LIMITS", "NAMES")


def validate(state: dict, config) -> dict:
    errs = check(state["outline"], [lo["urn"] for lo in state["los"].values()])
    structural = [e for e in errs if not e.startswith(SOFT_INVARIANT_PREFIXES)]
    if structural:
        raise PipelineBug("; ".join(structural))
    return {"validation": errs}
