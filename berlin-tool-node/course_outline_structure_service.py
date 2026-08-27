"""Deterministic course-outline structure enforcement services.

This module moves arithmetic-heavy structure decisions out of Berlin prompts.
It derives deterministic estimates from analyzer output, packs learning
objectives into lesson-sized chapters, merges undersized parts, and emits a
stable structure for the downstream DCIM node.
"""

from __future__ import annotations

import copy
from collections import Counter, OrderedDict

from api.models.course_outline_structure.course_outline_structure_models import (
    AnnotatedObjective,
    PackMergeRequest,
    PackMergeResponse,
    StructureValidationSummary,
    StructuredChapter,
    StructuredLearningObjective,
    StructuredPart,
)

MINIMUM_UNDERSTAND_CHAPTERS = 4
MAX_LOS_PER_CHAPTER = 4
MAX_PART_NAME_WORDS = 6

GRADE_WORD_LIMITS = {
    "K-2": 400,
    "3-5": 600,
    "MS": 2000,
    "HS": 2250,
}

GRADE_WORD_RANGES = {
    "K-2": (50, 200),
    "3-5": (50, 300),
    "MS": (200, 750),
    "HS": (300, 1000),
}

BLOOMS_TIME_RANGES = {
    "Foundational": (12, 18),
    "Intermediate": (15, 22),
    "Advanced": (20, 28),
}

STOP_WORDS = {
    "a", "an", "the", "of", "in", "for", "to", "by", "on", "with", "from",
    "that", "this", "their", "its", "and", "or", "is", "are", "be", "been",
    "being", "was", "were", "will", "can", "could", "should", "would", "may",
    "might", "has", "have", "had", "do", "does", "did", "using", "use", "related",
    "concept", "concepts"
}


def _normalize_grade_band(grade_band: str) -> str:
    """Normalize raw or unnormalized grade band strings (e.g., 'grade6', 'k6-8', 'Grade 3-5') into standard keys."""
    if not grade_band:
        return "3-5"
    raw = grade_band.strip().lower()

    if raw in ("k-2", "3-5", "ms", "hs"):
        return "MS" if raw == "ms" else ("HS" if raw == "hs" else ("K-2" if raw == "k-2" else "3-5"))

    if any(k in raw for k in ["k-2", "k_2", "k2", "kindergarten", "grade 1", "grade 2", "grade1", "grade2"]):
        return "K-2"
    if any(k in raw for k in ["3-5", "3_5", "grade 3", "grade 4", "grade 5", "grade3", "grade4", "grade5", "elem"]):
        return "3-5"
    if any(k in raw for k in ["ms", "middle", "6-8", "6_8", "k6-8", "grade 6", "grade 7", "grade 8", "grade6", "grade7", "grade8"]):
        return "MS"
    if any(k in raw for k in ["hs", "high", "9-12", "9_12", "grade 9", "grade 10", "grade 11", "grade 12", "grade9", "grade10", "grade11", "grade12"]):
        return "HS"

    return "3-5"


def _estimate_time_minutes(blooms_level: str) -> int:
    """Return a deterministic lesson-time estimate for one learning objective."""
    low, high = BLOOMS_TIME_RANGES.get(blooms_level, BLOOMS_TIME_RANGES["Foundational"])
    if blooms_level == "Foundational":
        return low + 2
    if blooms_level == "Intermediate":
        return (low + high) // 2
    return max(low, high - 2)


def _estimate_word_count(grade_band: str, blooms_level: str) -> int:
    """Return a deterministic word-count estimate for one learning objective."""
    norm_band = _normalize_grade_band(grade_band)
    low, high = GRADE_WORD_RANGES.get(norm_band, GRADE_WORD_RANGES["3-5"])
    span = high - low
    if blooms_level == "Foundational":
        return low + max(1, span // 6)
    if blooms_level == "Intermediate":
        return low + (span // 2)
    return high - max(1, span // 6)


def _get_total_lo_count(request: PackMergeRequest) -> int:
    """Return the authoritative total LO count for this request.

    Prefers total_input_lo_count from the analyser payload if provided;
    otherwise falls back to len(objectives) from the input objectives list.
    """
    explicit_count = request.annotated_objectives.total_input_lo_count
    if explicit_count is not None and explicit_count > 0:
        return explicit_count
    return len(request.annotated_objectives.objectives)


def _get_input_duplicate_urns(request: PackMergeRequest) -> list[str]:
    """Return known input duplicate URNs.

    Uses input_duplicate_urns from payload if provided; otherwise automatically
    derives duplicate URNs from the list of objectives in annotated_objectives.
    """
    explicit_duplicates = request.annotated_objectives.input_duplicate_urns
    if explicit_duplicates:
        return list(explicit_duplicates)
    
    urn_counts = Counter(
        o.learning_objective_urn for o in request.annotated_objectives.objectives
    )
    return [urn for urn, count in urn_counts.items() if count > 1]


def _build_lo_record(
    objective: AnnotatedObjective,
    *,
    source_chapter_name: str,
    grade_band: str,
) -> dict:
    """Convert analyzer output into the deterministic working LO shape.

    Each record is a PRE-POPULATED MODULE STUB. The `module_title` field is
    intentionally set to None so the DCIM knows exactly which field to fill --
    it cannot skip or reorder stubs because the slots already exist.
    """
    return {
        "urn": objective.learning_objective_urn,
        "lo_text": objective.objective,
        "objective": objective.objective,
        "primary_skill": objective.primary_skill,
        "blooms_level": objective.blooms_level,
        "source_chapter_name": source_chapter_name,
        "estimated_word_count": _estimate_word_count(grade_band, objective.blooms_level),
        "estimated_time_minutes": _estimate_time_minutes(objective.blooms_level),
        "module_title": None,
    }


def _chapter_base_name(bucket: list[dict]) -> str:
    """Derive a chapter name from the source chapter names present in a bucket."""
    source_names = list(OrderedDict.fromkeys(lo["source_chapter_name"] for lo in bucket))
    if len(source_names) == 1:
        return source_names[0]
    if len(source_names) == 2:
        return f"{source_names[0]} and {source_names[1]}"
    return f"{source_names[0]} and Related Concepts"


def _merge_part_names(first_name: str, second_name: str) -> str:
    """Deterministically combines part names without calling LLM."""
    CONJUNCTIONS = {"and", "or", "the", "of", "in", "for", "to", "a"}

    # -- 1. Identity / containment
    if first_name == second_name:
        return first_name
    if second_name.lower() in first_name.lower():
        return first_name
    if first_name.lower() in second_name.lower():
        return second_name

    # -- 2. Strip trailing conjunctions
    words_a = first_name.split()
    words_b = second_name.split()
    while words_a and words_a[-1].lower() in CONJUNCTIONS:
        words_a.pop()
    while words_b and words_b[-1].lower() in CONJUNCTIONS:
        words_b.pop()

    clean_a = " ".join(words_a)
    clean_b = " ".join(words_b)

    combined = f"{clean_a} & {clean_b}"
    if len(combined.split()) <= MAX_PART_NAME_WORDS:
        return combined

    short_a = " ".join([w for w in words_a if w.lower() not in CONJUNCTIONS][:2])
    short_b = " ".join([w for w in words_b if w.lower() not in CONJUNCTIONS][:2])
    return f"{short_a} & {short_b}"


def _build_chapter_differentiator(chapter_los: list[dict], base_name: str = "") -> str:
    if not chapter_los:
        return ""

    base_words = set(w.lower() for w in base_name.split())
    novel_skill_words: list[str] = []

    for lo in chapter_los:
        skill = lo.get("primary_skill", "")
        if skill:
            for word in skill.split():
                clean_word = word.strip(".,;:()").title()
                if word.lower() not in base_words and word.lower() not in STOP_WORDS:
                    if clean_word not in novel_skill_words:
                        novel_skill_words.append(clean_word)

    if novel_skill_words:
        return " ".join(novel_skill_words[:2])
    return ""


def _uniquify_chapter_names(chapters: list[dict]) -> list[dict]:
    """Make duplicate chapter names unique inside a part using meaningful differentiators.

    Instead of appending " 2", " 3" (which produces banned title patterns),
    this function uses LO content to differentiate chapters with the same base name.
    """
    name_counts: dict[str, int] = {}
    for chapter in chapters:
        name = chapter["chapter_name"]
        name_counts[name] = name_counts.get(name, 0) + 1

    seen: dict[str, int] = {}
    used_names: set[str] = set()

    for chapter in chapters:
        name = chapter["chapter_name"]

        if name_counts[name] <= 1:
            used_names.add(name)
            continue

        occurrence = seen.get(name, 0) + 1
        seen[name] = occurrence

        if occurrence == 1:
            used_names.add(name)
            continue

        differentiator = _build_chapter_differentiator(chapter.get("learning_objectives", []), base_name=name)
        new_name = f"{name} - {differentiator}" if differentiator else f"{name} ({occurrence})"

        if new_name in used_names:
            new_name = f"{name} ({occurrence})"

        chapter["chapter_name"] = new_name
        used_names.add(new_name)

    return chapters


def _assign_module_numbers(los: list[dict]) -> list[dict]:
    for index, lo in enumerate(los, start=1):
        lo["module_number"] = index
    return los


def _pack_los_into_chapters(los: list[dict], word_limit: int, time_limit: int) -> list[dict]:
    """Pack ordered learning objectives into lesson-sized understand chapters."""
    chapters: list[dict] = []
    bucket: list[dict] = []
    bucket_words = 0
    bucket_time = 0

    for lo in los:
        would_exceed_words = bucket_words + lo["estimated_word_count"] > word_limit
        would_exceed_time = bucket_time + lo["estimated_time_minutes"] > time_limit
        would_exceed_density = len(bucket) >= MAX_LOS_PER_CHAPTER

        if bucket and (would_exceed_words or would_exceed_time or would_exceed_density):
            chapters.append(
                {
                    "chapter_name": _chapter_base_name(bucket),
                    "chapter_estimated_word_count": bucket_words,
                    "chapter_estimated_time_minutes": bucket_time,
                    "learning_objectives": _assign_module_numbers(copy.deepcopy(bucket)),
                }
            )
            bucket = []
            bucket_words = 0
            bucket_time = 0

        bucket.append(copy.deepcopy(lo))
        bucket_words += lo["estimated_word_count"]
        bucket_time += lo["estimated_time_minutes"]

    if bucket:
        chapters.append(
            {
                "chapter_name": _chapter_base_name(bucket),
                "chapter_estimated_word_count": bucket_words,
                "chapter_estimated_time_minutes": bucket_time,
                "learning_objectives": _assign_module_numbers(copy.deepcopy(bucket)),
            }
        )

    return _uniquify_chapter_names(chapters)


def _build_initial_parts(request: PackMergeRequest, word_limit: int, time_limit: int) -> list[dict]:
    objective_by_urn = {
        objective.learning_objective_urn: objective
        for objective in request.annotated_objectives.objectives
    }
    objective_order = {
        objective.learning_objective_urn: index
        for index, objective in enumerate(request.annotated_objectives.objectives)
    }
    part_order: dict[str, int] = {}
    for assignment in request.grouping_plan.assignments:
        part_order.setdefault(assignment.part_name, len(part_order))

    ordered_assignments = sorted(
        request.grouping_plan.assignments,
        key=lambda assignment: (
            part_order[assignment.part_name],
            assignment.order_rank,
            objective_order.get(assignment.learning_objective_urn, 10**9),
        ),
    )

    planned_parts: list[dict] = []
    current_part_name: str | None = None
    current_part_chapters: list[dict] = []
    current_chapter_name: str | None = None
    current_chapter_order_rank: int | None = None
    current_chapter_los: list[dict] = []

    def flush_current_chapter() -> None:
        nonlocal current_chapter_los, current_part_chapters
        if not current_chapter_los:
            return
        current_part_chapters.extend(
            _pack_los_into_chapters(current_chapter_los, word_limit, time_limit)
        )
        current_chapter_los = []

    def flush_current_part() -> None:
        nonlocal current_part_name, current_part_chapters, planned_parts
        if current_part_name is None:
            return
        flush_current_chapter()
        planned_parts.append(
            {
                "part_name": current_part_name,
                "chapters": copy.deepcopy(current_part_chapters),
            }
        )
        current_part_chapters = []

    for assignment in ordered_assignments:
        objective = objective_by_urn.get(assignment.learning_objective_urn)
        if objective is None:
            continue

        if current_part_name is None:
            current_part_name = assignment.part_name

        if assignment.part_name != current_part_name:
            flush_current_part()
            current_part_name = assignment.part_name
            current_chapter_name = None
            current_chapter_order_rank = None

        if (
            current_chapter_name is None
            or assignment.chapter_name != current_chapter_name
            or assignment.order_rank != current_chapter_order_rank
        ):
            flush_current_chapter()
            current_chapter_name = assignment.chapter_name
            current_chapter_order_rank = assignment.order_rank

        current_chapter_los.append(
            _build_lo_record(
                objective,
                source_chapter_name=assignment.chapter_name,
                grade_band=request.annotated_objectives.grade_band,
            )
        )

    if current_part_name is not None:
        flush_current_part()

    return planned_parts


def _get_best_adjacent(parts: list[dict], index: int) -> int | None:
    """Return the best adjacent part index for a merge."""
    candidates: list[tuple[int, int]] = []
    if index > 0:
        candidates.append((index - 1, len(parts[index - 1]["chapters"])))
    if index < len(parts) - 1:
        candidates.append((index + 1, len(parts[index + 1]["chapters"])))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[1], -item[0]))
    return candidates[0][0]


def _merge_parts(
    parts: list[dict],
    source_idx: int,
    target_idx: int,
    word_limit: int,
    time_limit: int,
) -> list[dict]:
    """Merge two adjacent parts, preserving the earlier positional slot."""
    source = parts[source_idx]
    target = parts[target_idx]
    if source_idx < target_idx:
        combined_chapters = copy.deepcopy(source["chapters"]) + copy.deepcopy(target["chapters"])
        merged_name = _merge_part_names(source["part_name"], target["part_name"])
    else:
        combined_chapters = copy.deepcopy(target["chapters"]) + copy.deepcopy(source["chapters"])
        merged_name = _merge_part_names(target["part_name"], source["part_name"])

    merged_part = {
        "part_name": merged_name,
        "chapters": _uniquify_chapter_names(combined_chapters),
    }

    first, second = sorted([source_idx, target_idx])
    merged_parts: list[dict] = []
    for index, part in enumerate(parts):
        if index == first:
            merged_parts.append(merged_part)
            continue
        if index == second:
            continue
        merged_parts.append(copy.deepcopy(part))
    return merged_parts


def _enforce_minimum_4(
    parts: list[dict],
    word_limit: int,
    time_limit: int,
) -> tuple[list[dict], str]:
    """Merge undersized parts until all parts satisfy the minimum or the exception applies."""
    log: list[str] = []
    changed = True

    while changed:
        changed = False
        for index, part in enumerate(parts):
            chapter_count = len(part["chapters"])
            if chapter_count >= MINIMUM_UNDERSTAND_CHAPTERS:
                continue

            best_adjacent = _get_best_adjacent(parts, index)
            if best_adjacent is None:
                log.append(f"WARNING: Part '{part['part_name']}' has {chapter_count} chapters and no adjacent part.")
                continue

            if len(parts) == 2:
                combined_count = len(parts[index]["chapters"]) + len(parts[best_adjacent]["chapters"])
                if combined_count < MINIMUM_UNDERSTAND_CHAPTERS:
                    log.append(
                        f"EXCEPTION: Part '{part['part_name']}' has {chapter_count} chapters; "
                        f"combined pair would still have {combined_count} chapters (< 4). Accepted as-is."
                    )
                    continue

            target_name = parts[best_adjacent]["part_name"]
            target_count = len(parts[best_adjacent]["chapters"])
            log.append(
                f"MERGE: Part '{part['part_name']}' ({chapter_count} chapters) merged with '{target_name}' ({target_count} chapters)"
            )
            parts = _merge_parts(parts, index, best_adjacent, word_limit, time_limit)
            merged_index = min(index, best_adjacent)
            log.append(f"RESULT: Part '{parts[merged_index]['part_name']}' now has {len(parts[merged_index]['chapters'])} chapters")
            changed = True
            break

    for part in parts:
        chapter_count = len(part["chapters"])
        suffix = "OK" if chapter_count >= MINIMUM_UNDERSTAND_CHAPTERS else "WARNING"
        log.append(f"FINAL: Part '{part['part_name']}' - {chapter_count} understand chapters {suffix}")

    return parts, "\n".join(log)


def _compute_total_chapters(num_content_parts: int, content_chapter_count: int) -> int:
    return 1 + content_chapter_count + (num_content_parts * 4) + 4


def _validate_output(
    input_urns: set[str],
    parts: list[dict],
    total_input_lo_count: int | None = None,
    input_duplicate_urns: list[str] | None = None,
) -> StructureValidationSummary:
    """Validate deterministic output before returning it to Berlin."""
    output_urns: list[str] = []
    for part in parts:
        for chapter in part["chapters"]:
            for lo in chapter["learning_objectives"]:
                output_urns.append(lo["urn"])

    authoritative_total = total_input_lo_count if (total_input_lo_count is not None and total_input_lo_count > 0) else len(input_urns)
    known_duplicates: set[str] = set(input_duplicate_urns or [])

    output_urn_counts = Counter(output_urns)
    output_urn_set = set(output_urns)

    missing = sorted(input_urns - output_urn_set)
    extra = sorted(output_urn_set - input_urns)

    unexpected_duplicates = sorted(
        urn
        for urn, count in output_urn_counts.items()
        if count > 1 and urn not in known_duplicates
    )

    return StructureValidationSummary(
        total_input_los=authoritative_total,
        total_placed_los=len(output_urns),
        all_parts_gte_4_chapters=all(
            len(part["chapters"]) >= MINIMUM_UNDERSTAND_CHAPTERS for part in parts
        ),
        duplicate_urns=unexpected_duplicates,
        missing_urns=missing,
        extra_urns=extra,
        valid=not unexpected_duplicates and not missing and not extra,
    )


def _number_parts(parts: list[dict]) -> list[StructuredPart]:
    """Assign part, chapter, and module numbers and build response models."""
    structured_parts: list[StructuredPart] = []
    for part_index, part in enumerate(parts, start=2):
        structured_chapters: list[StructuredChapter] = []
        for chapter_index, chapter in enumerate(part["chapters"], start=2):
            structured_los: list[StructuredLearningObjective] = []
            for module_index, lo in enumerate(chapter["learning_objectives"], start=1):
                structured_los.append(
                    StructuredLearningObjective(
                        urn=lo["urn"],
                        module_number=module_index,
                        lo_text=lo.get("lo_text", lo.get("objective", "")),
                        objective=lo["objective"],
                        primary_skill=lo["primary_skill"],
                        blooms_level=lo["blooms_level"],
                        source_chapter_name=lo["source_chapter_name"],
                        estimated_word_count=lo["estimated_word_count"],
                        estimated_time_minutes=lo["estimated_time_minutes"],
                        module_title=None,
                    )
                )
            structured_chapters.append(
                StructuredChapter(
                    chapter_name=chapter["chapter_name"],
                    chapter_number=chapter_index,
                    chapter_type="understand",
                    chapter_estimated_word_count=chapter["chapter_estimated_word_count"],
                    chapter_estimated_time_minutes=chapter["chapter_estimated_time_minutes"],
                    learning_objectives=structured_los,
                )
            )

        structured_parts.append(
            StructuredPart(
                part_name=part["part_name"],
                part_number=part_index,
                understand_chapter_count=len(structured_chapters),
                chapters=structured_chapters,
            )
        )
    return structured_parts


def pack_and_merge_course_outline_structure(request: PackMergeRequest) -> PackMergeResponse:
    """Enforce deterministic course-outline structure rules for Berlin Tool Nodes."""
    norm_grade_band = _normalize_grade_band(request.annotated_objectives.grade_band)
    word_limit = request.chapter_word_count_limit or GRADE_WORD_LIMITS.get(norm_grade_band, 600)
    time_limit = request.annotated_objectives.minutes_per_lesson
    total_lesson_days = (
        request.annotated_objectives.lessons_per_week
        * request.annotated_objectives.course_duration_weeks
    )

    initial_parts = _build_initial_parts(request, word_limit, time_limit)
    enforced_parts, enforcement_log = _enforce_minimum_4(initial_parts, word_limit, time_limit)

    input_urns = {
        objective.learning_objective_urn
        for objective in request.annotated_objectives.objectives
    }

    total_input_lo_count = _get_total_lo_count(request)
    input_duplicate_urns = _get_input_duplicate_urns(request)

    validation = _validate_output(
        input_urns,
        enforced_parts,
        total_input_lo_count=total_input_lo_count,
        input_duplicate_urns=input_duplicate_urns,
    )
    numbered_parts = _number_parts(enforced_parts)

    content_chapter_count = sum(len(part["chapters"]) for part in enforced_parts)
    num_content_parts = len(enforced_parts)
    total_chapter_count = _compute_total_chapters(num_content_parts, content_chapter_count)

    return PackMergeResponse(
        course_title=request.annotated_objectives.course_title,
        grade_band=request.annotated_objectives.grade_band,
        subject_area=request.annotated_objectives.subject_area,
        chapter_word_count_limit=word_limit,
        minutes_per_lesson_day=time_limit,
        total_lesson_days=total_lesson_days,
        progression_type=request.grouping_plan.progression_type,
        annotated_objectives=request.annotated_objectives,
        enforcement_log=enforcement_log,
        parts=numbered_parts,
        validation=validation,
        content_chapter_count=content_chapter_count,
        num_content_parts=num_content_parts,
        total_chapter_count=total_chapter_count,
    )
