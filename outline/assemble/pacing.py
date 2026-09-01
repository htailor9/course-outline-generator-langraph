"""Lesson-day pacing check (+/- tolerance)."""


def pacing_fields(
    total_chapters: int, total_lesson_days: int, tolerance: float = 0.05
) -> dict:
    tol = round(total_lesson_days * tolerance)
    lower, upper = total_lesson_days - tol, total_lesson_days + tol
    if total_chapters > upper:
        return {
            "pacing_overrun": True,
            "pacing_overrun_lesson_days": total_chapters - total_lesson_days,
            "split_notes": [
                f"Pacing overrun: total_chapters_in_course={total_chapters} exceeds "
                f"total_lesson_days={total_lesson_days} (+{tol} tolerance)."
            ],
        }
    if total_chapters < lower:
        note = (
            f"Pacing check: total_chapters_in_course={total_chapters} is below the lesson-day target range "
            f"({lower}-{upper}) for total_lesson_days={total_lesson_days}. Course is under-filled."
        )
    else:
        note = f"Pacing check passed: total_chapters_in_course={total_chapters} within {lower}-{upper}."
    return {
        "pacing_overrun": False,
        "pacing_overrun_lesson_days": None,
        "split_notes": [note],
    }
