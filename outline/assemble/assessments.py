"""Default assessment per DCIM chapter type."""

_TABLE = {
    "understand": {
        "type": "Quick Check",
        "scoring": "auto",
        "delivery": "multiple_choice",
    },
    "apply": {"type": "Sample Work", "scoring": "teacher", "delivery": "dropbox"},
    "review": {
        "type": "Unit Online Practice",
        "scoring": "auto",
        "delivery": "multiple_choice",
    },
    "test": {"type": "Unit Test", "scoring": "auto_and_teacher", "delivery": "test"},
    "semester_review": {
        "type": "Semester Online Practice",
        "scoring": "auto",
        "delivery": "multiple_choice",
    },
    "semester_exam": {
        "type": "Semester Exam",
        "scoring": "auto_and_teacher",
        "delivery": "exam",
    },
}


def for_chapter_type(chapter_type: str) -> dict | None:
    return dict(_TABLE[chapter_type]) if chapter_type in _TABLE else None
