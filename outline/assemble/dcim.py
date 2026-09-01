"""Build the DCIM course outline JSON from packed structure + titles. Pure, deterministic."""

from outline.assemble.assessments import for_chapter_type
from outline.assemble.pacing import pacing_fields


def _module(
    mtype: str,
    number: int,
    title: str,
    urn=None,
    words=None,
    mins=None,
    skill=None,
    tier=None,
) -> dict:
    return {
        "label": "module",
        "type": mtype,
        "module_number": number,
        "title": {"en": title},
        "learning_objective_urn": urn,
        "estimated_word_count": words,
        "estimated_time_minutes": mins,
        "primary_skill": skill,
        "blooms_level": tier,
    }


def _chapter(
    ctype: str, number: int, title: str, words, mins: int, children: list[dict]
) -> dict:
    ch = {
        "label": "chapter",
        "type": ctype,
        "chapter_number": number,
        "title": {"en": title},
        "chapter_estimated_word_count": words,
        "chapter_estimated_time_minutes": mins,
        "children": children,
    }
    assessment = for_chapter_type(ctype)
    if assessment is not None:
        ch["assessment"] = assessment
    return ch


def _part(ptype: str, number: int, title: str, chapters: list[dict]) -> dict:
    return {
        "label": "part",
        "type": ptype,
        "part_number": number,
        "title": {"en": title},
        "children": chapters,
    }


def _overview(course: dict, mpl: int) -> dict:
    t = course["course_title"]
    return _part(
        "overview",
        1,
        f"{t} Course Overview",
        [
            _chapter(
                "overview",
                1,
                f"{t} Course Overview",
                None,
                mpl,
                [
                    _module("course_guide", 1, "Course Guide"),
                    _module("overview_introduction", 2, "Course Introduction"),
                ],
            )
        ],
    )


def _content_part(p: dict, titles: dict[str, str], mpl: int) -> dict:
    name = p["part_name"]
    chapters = [
        _chapter(
            "introduction",
            1,
            f"{name} Introduction",
            None,
            mpl,
            [_module("introduction", 1, f"{name} Introduction")],
        )
    ]
    n = 1
    for c in p["chapters"]:
        n += 1
        mods = [
            _module(
                "understand",
                lo["module_number"],
                titles.get(lo["id"], lo.get("lo_text") or lo["urn"]),
                urn=lo["urn"],
                words=lo["estimated_word_count"],
                mins=lo["estimated_time_minutes"],
                skill=lo["primary_skill"],
                tier=lo["blooms_level"],
            )
            for lo in c["learning_objectives"]
        ]
        chapters.append(
            _chapter(
                "understand",
                n,
                c["chapter_name"],
                c["chapter_estimated_word_count"],
                c["chapter_estimated_time_minutes"],
                mods,
            )
        )
    chapters.append(
        _chapter(
            "apply", n + 1, f"{name} Apply", None, mpl, [_module("apply", 1, "Apply")]
        )
    )
    chapters.append(
        _chapter(
            "review",
            n + 2,
            f"{name} Review",
            None,
            mpl,
            [_module("review", 1, "Review")],
        )
    )
    chapters.append(_chapter("test", n + 3, f"{name} Part Test", None, mpl, []))
    return _part("understand", p["part_number"], name, chapters)


def _semester(course: dict, letter: str, number: int, mpl: int) -> dict:
    t = course["course_title"]
    return _part(
        "semester",
        number,
        f"{t} Semester {letter} Reflect & Review",
        [
            _chapter(
                "semester_review",
                1,
                f"Semester {letter} Review",
                None,
                mpl,
                [_module("semester_review", 1, f"Semester {letter} Review & Reflect")],
            ),
            _chapter("semester_exam", 2, f"Semester {letter} Exam", None, mpl, []),
        ],
    )


def build(course: dict, budget: dict, packed: dict, titles: dict[str, str]) -> dict:
    mpl = course["minutes_per_lesson"]
    parts = [_overview(course, mpl)]
    parts += [_content_part(p, titles, mpl) for p in packed["parts"]]
    n_content = len(packed["parts"])
    parts.append(_semester(course, "A", n_content + 2, mpl))
    parts.append(_semester(course, "B", n_content + 3, mpl))
    total_chapters = sum(len(p["children"]) for p in parts)
    pacing = pacing_fields(total_chapters, budget["total_lesson_days"])

    validation = packed.get("validation", {})
    notes = list(pacing["split_notes"])
    notes.append(
        f"Structure check: {n_content} content parts; all parts >= 4 understand chapters: "
        f"{validation.get('all_parts_gte_4_chapters', True)}."
    )
    enforcement_log = packed.get("enforcement_log") or ""
    merge_count = sum(
        1 for line in enforcement_log.splitlines() if line.startswith("MERGE:")
    )
    if merge_count:
        notes.append(f"Merges applied: {merge_count} (see enforcement_log).")

    return {
        "course_title": course["course_title"],
        "grade_band": course["grade_band"],
        "subject_area": course["subject_area"],
        "chapter_word_count_limit": budget["word_limit"],
        "total_parts": len(parts),
        "total_chapters": total_chapters,
        "title": {"en": course["course_title"]},
        "label": "project",
        "children": parts,
        "total_lesson_days": budget["total_lesson_days"],
        "total_chapters_in_course": total_chapters,
        "pacing_overrun": pacing["pacing_overrun"],
        "pacing_overrun_lesson_days": pacing["pacing_overrun_lesson_days"],
        "split_notes": notes,
        "unassigned_objective_urns": list(validation.get("missing_urns", [])),
    }
