"""Deterministic structure: estimates -> pack -> merge -> number -> validate."""

from collections import Counter

from outline.rules.estimates import estimate_minutes, estimate_words
from outline.rules.merging import MINIMUM_UNDERSTAND_CHAPTERS, enforce_min_4
from outline.rules.naming import uniquify_chapter_names, uniquify_part_names
from outline.rules.packing import pack_chapters


def _stub(lo: dict, grade_band: str) -> dict:
    return {
        "id": lo["id"],
        "urn": lo["urn"],
        "lo_text": lo["text"],
        "primary_skill": lo.get("primary_skill") or "General",
        "blooms_level": lo.get("tier") or "Foundational",
        "source_chapter_name": lo.get("chapter")
        or (lo.get("primary_skill") or "General"),
        "estimated_word_count": estimate_words(
            grade_band, lo.get("tier") or "Foundational"
        ),
        "estimated_time_minutes": estimate_minutes(lo.get("tier") or "Foundational"),
    }


def _initial_parts(
    course: dict, budget: dict, los: dict[str, dict], parts: list[dict]
) -> list[dict]:
    out: list[dict] = []
    for part in parts:
        ordered = sorted(
            (los[i] for i in part["ids"] if i in los),
            key=lambda lo: (
                lo.get("rank") or 10**6,
                lo.get("chapter") or "",
                lo["idx"],
            ),
        )
        chapters: list[dict] = []
        bucket: list[dict] = []
        current: tuple | None = None
        for lo in ordered:
            key = (lo.get("chapter"), lo.get("rank"))
            if current is not None and key != current and bucket:
                chapters.extend(
                    pack_chapters(
                        bucket, budget["word_limit"], course["minutes_per_lesson"]
                    )
                )
                bucket = []
            current = key
            bucket.append(_stub(lo, course["grade_band"]))
        if bucket:
            chapters.extend(
                pack_chapters(
                    bucket, budget["word_limit"], course["minutes_per_lesson"]
                )
            )
        if chapters:
            # Uniquify across the WHOLE unit, not per packing bucket — buckets sharing a base name
            # (e.g. standards mode splitting a topic by input position) must not yield duplicate
            # lesson names within the unit.
            out.append(
                {
                    "part_name": part["part_name"],
                    "chapters": uniquify_chapter_names(chapters),
                }
            )
    return out


def _number(parts: list[dict]) -> list[dict]:
    for pi, p in enumerate(parts, start=2):
        p["part_number"] = pi
        p["understand_chapter_count"] = len(p["chapters"])
        for ci, c in enumerate(p["chapters"], start=2):
            c["chapter_number"] = ci
            c["chapter_type"] = "understand"
            for mi, lo in enumerate(c["learning_objectives"], start=1):
                lo["module_number"] = mi
    return parts


def _validate(input_urns: list[str], parts: list[dict]) -> dict:
    placed = [
        lo["urn"]
        for p in parts
        for c in p["chapters"]
        for lo in c["learning_objectives"]
    ]
    in_counts, out_counts = Counter(input_urns), Counter(placed)
    known_dupes = {u for u, n in in_counts.items() if n > 1}
    missing = sorted(set(input_urns) - set(placed))
    extra = sorted(set(placed) - set(input_urns))
    dupes = sorted(u for u, n in out_counts.items() if n > 1 and u not in known_dupes)
    return {
        "total_input_los": len(input_urns),
        "total_placed_los": len(placed),
        "all_parts_gte_4_chapters": all(
            len(p["chapters"]) >= MINIMUM_UNDERSTAND_CHAPTERS for p in parts
        ),
        "duplicate_urns": dupes,
        "missing_urns": missing,
        "extra_urns": extra,
        "valid": not dupes and not missing and not extra,
    }


def build_structure(
    course: dict, budget: dict, los: dict[str, dict], parts: list[dict]
) -> dict:
    initial = _initial_parts(course, budget, los, parts)
    merged, log = enforce_min_4(initial)
    merged = uniquify_part_names(merged)  # no duplicate unit names within the course
    numbered = _number(merged)
    validation = _validate([lo["urn"] for lo in los.values()], numbered)
    content_chapters = sum(len(p["chapters"]) for p in numbered)
    n_parts = len(numbered)
    return {
        "parts": numbered,
        "enforcement_log": "\n".join(log),
        "validation": validation,
        "content_chapter_count": content_chapters,
        "num_content_parts": n_parts,
        "total_chapter_count": 1 + content_chapters + n_parts * 4 + 4,
    }
