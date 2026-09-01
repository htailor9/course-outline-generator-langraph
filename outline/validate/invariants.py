"""Final invariants over the assembled outline. Returns a list of failure strings (empty = valid)."""

import re
from collections import Counter

BANNED = re.compile(
    r"(?i)\b(continued|part\s*(2|3|ii|iii)|module\s*\d+|activity|practice)\b"
)


def check(outline: dict, input_urns: list[str]) -> list[str]:
    errs: list[str] = []
    parts = outline["children"]
    content = [p for p in parts if p["type"] == "understand"]

    placed = [
        m["learning_objective_urn"]
        for p in parts
        for c in p["children"]
        for m in c["children"]
        if m.get("learning_objective_urn")
    ]
    input_urns_counter = Counter(input_urns)
    if Counter(placed) != input_urns_counter:
        missing = sorted(set(input_urns) - set(placed))
        extra = sorted(set(placed) - set(input_urns))
        dup = sorted(u for u, n in Counter(placed).items() if n > input_urns_counter[u])
        errs.append(
            f"LO_COVERAGE missing={missing[:5]} extra={extra[:5]} duplicate={dup[:5]}"
        )

    for p in content:
        n = sum(1 for c in p["children"] if c["type"] == "understand")
        if n < 4 and not (
            len(content) <= 2
            and sum(
                sum(1 for c in q["children"] if c["type"] == "understand")
                for q in content
            )
            < 4
        ):
            errs.append(f"MIN4 part '{p['title']['en']}' has {n} understand chapters")

    if [p["type"] for p in parts[-2:]] != ["semester", "semester"] or parts[0][
        "type"
    ] != "overview":
        errs.append("SEMESTERS overview must be first and two semester parts last")
    if any(p["type"] != "understand" for p in parts[1:-2]):
        errs.append(
            "SEMESTERS content parts must be type understand between overview and semesters"
        )

    # NAMES (soft): no duplicate unit names in the course; no duplicate lesson names within a unit.
    # (Duplicate module names within a lesson are covered by the TITLES check below.)
    unit_counts = Counter(p["title"]["en"].strip().casefold() for p in content)
    for name, n in unit_counts.items():
        if n > 1:
            errs.append(
                f"NAMES duplicate unit name '{name}' appears {n} times in course"
            )
    for p in parts:
        lesson_counts = Counter(
            c["title"]["en"].strip().casefold() for c in p["children"]
        )
        for name, n in lesson_counts.items():
            if n > 1:
                errs.append(
                    f"NAMES duplicate lesson name '{name}' appears {n} times in unit '{p['title']['en']}'"
                )

    for p in parts:
        if [c["chapter_number"] for c in p["children"]] != list(
            range(1, len(p["children"]) + 1)
        ):
            errs.append(
                f"ORDER chapter numbers not sequential in part '{p['title']['en']}'"
            )
        for c in p["children"]:
            if [m["module_number"] for m in c["children"]] != list(
                range(1, len(c["children"]) + 1)
            ):
                errs.append(
                    f"ORDER module numbers not sequential in chapter '{c['title']['en']}'"
                )
            if c["type"] == "understand":
                w = sum(m["estimated_word_count"] or 0 for m in c["children"])
                t = sum(m["estimated_time_minutes"] or 0 for m in c["children"])
                if (
                    w != c["chapter_estimated_word_count"]
                    or t != c["chapter_estimated_time_minutes"]
                ):
                    errs.append(
                        f"SUMS chapter '{c['title']['en']}' totals do not match modules"
                    )

    overview = next((p for p in parts if p["type"] == "overview"), None)
    minutes_per_lesson = (
        overview["children"][0]["chapter_estimated_time_minutes"]
        if overview and overview["children"]
        else None
    )
    chapter_word_count_limit = outline.get("chapter_word_count_limit")
    for p in content:
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            time = c.get("chapter_estimated_time_minutes")
            words = c.get("chapter_estimated_word_count")
            if (
                minutes_per_lesson is not None
                and time is not None
                and time > minutes_per_lesson
            ):
                errs.append(
                    f"LIMITS chapter '{c['title']['en']}' exceeds minutes_per_lesson "
                    f"({time} > {minutes_per_lesson})"
                )
            if (
                chapter_word_count_limit is not None
                and words is not None
                and words > chapter_word_count_limit
            ):
                errs.append(
                    f"LIMITS chapter '{c['title']['en']}' exceeds chapter_word_count_limit "
                    f"({words} > {chapter_word_count_limit})"
                )

    expected_parts = 1 + len(content) + 2
    expected_chapters = sum(len(p["children"]) for p in parts)
    if (
        outline["total_parts"] != expected_parts
        or outline["total_chapters"] != expected_chapters
        or outline["total_chapters_in_course"] != expected_chapters
    ):
        errs.append("SUMS total_parts/total_chapters mismatch")

    for p in content:
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            titles = [m["title"]["en"].strip().casefold() for m in c["children"]]
            if len(titles) != len(set(titles)):
                errs.append(
                    f"TITLES duplicate module titles in chapter '{c['title']['en']}'"
                )
            for m in c["children"]:
                t = m["title"]["en"].strip()
                if (
                    not t
                    or t.casefold() == c["title"]["en"].strip().casefold()
                    or BANNED.search(t)
                ):
                    errs.append(
                        f"TITLES bad module title '{t}' in chapter '{c['title']['en']}'"
                    )
    return errs
