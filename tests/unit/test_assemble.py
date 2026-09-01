import copy
from outline.assemble.dcim import build
from outline.assemble.pacing import pacing_fields
from outline.assemble.assessments import for_chapter_type


def packed_from_golden(golden: dict) -> tuple[dict, dict]:
    """Rebuild `packed` + `titles` from the golden outline so assemble can be round-tripped."""
    parts, titles = [], {}
    for p in golden["children"]:
        if p["type"] != "understand":
            continue
        chapters = []
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            los = []
            for m in c["children"]:
                lo_id = m["learning_objective_urn"]
                titles[lo_id] = m["title"]["en"]
                los.append(
                    {
                        "id": lo_id,
                        "urn": lo_id,
                        "module_number": m["module_number"],
                        "lo_text": "",
                        "primary_skill": m["primary_skill"],
                        "blooms_level": m["blooms_level"],
                        "source_chapter_name": c["title"]["en"],
                        "estimated_word_count": m["estimated_word_count"],
                        "estimated_time_minutes": m["estimated_time_minutes"],
                    }
                )
            chapters.append(
                {
                    "chapter_name": c["title"]["en"],
                    "chapter_number": c["chapter_number"],
                    "chapter_type": "understand",
                    "chapter_estimated_word_count": c["chapter_estimated_word_count"],
                    "chapter_estimated_time_minutes": c[
                        "chapter_estimated_time_minutes"
                    ],
                    "learning_objectives": los,
                }
            )
        parts.append(
            {
                "part_name": p["title"]["en"],
                "part_number": p["part_number"],
                "understand_chapter_count": len(chapters),
                "chapters": chapters,
            }
        )
    n_ch = sum(len(p["chapters"]) for p in parts)
    packed = {
        "parts": parts,
        "enforcement_log": "",
        "validation": {"valid": True},
        "content_chapter_count": n_ch,
        "num_content_parts": len(parts),
        "total_chapter_count": 1 + n_ch + 4 * len(parts) + 4,
    }
    return packed, titles


def strip(o: dict) -> dict:
    o = copy.deepcopy(o)
    o.pop("split_notes", None)
    for p in o["children"]:
        for c in p["children"]:
            c.pop("assessment", None)
    return o


def test_assemble_reproduces_golden(golden43, input43):
    packed, titles = packed_from_golden(golden43)
    course = {
        k: input43[k]
        for k in ("course_title", "grade_band", "subject_area", "minutes_per_lesson")
    }
    budget = {"word_limit": 2000, "total_lesson_days": 180}
    out = build(course, budget, packed, titles)
    assert strip(out) == strip(golden43)
    assert isinstance(out["split_notes"], list) and out["split_notes"]


def test_pacing_overrun():
    f = pacing_fields(total_chapters=200, total_lesson_days=180)
    assert f["pacing_overrun"] is True and f["pacing_overrun_lesson_days"] == 20
    ok = pacing_fields(total_chapters=76, total_lesson_days=180)
    assert ok["pacing_overrun"] is False and ok["pacing_overrun_lesson_days"] is None


def test_assessment_mapping():
    assert for_chapter_type("understand")["type"] == "Quick Check"
    assert for_chapter_type("test")["type"] == "Unit Test"
    assert for_chapter_type("semester_exam")["type"] == "Semester Exam"
    assert for_chapter_type("apply")["type"] == "Sample Work"
    assert for_chapter_type("review")["type"] == "Unit Online Practice"
    assert for_chapter_type("semester_review")["type"] == "Semester Online Practice"
    assert for_chapter_type("introduction") is None


_COURSE = {
    "course_title": "Test Course",
    "grade_band": "6-8",
    "subject_area": "Science",
    "minutes_per_lesson": 60,
}
_BUDGET = {"word_limit": 2000, "total_lesson_days": 180}


def test_zero_content_parts():
    packed = {"parts": [], "validation": {"valid": True}}
    out = build(_COURSE, _BUDGET, packed, {})
    assert out["total_parts"] == 3
    assert out["total_chapters"] == 5
    assert [p["type"] for p in out["children"]] == ["overview", "semester", "semester"]


def test_missing_title_falls_back_to_lo_text():
    stub = {
        "id": "L1",
        "urn": "urn:L1",
        "module_number": 1,
        "lo_text": "Identify main idea",
        "primary_skill": "Reading",
        "blooms_level": "Foundational",
        "source_chapter_name": "Chapter One",
        "estimated_word_count": 100,
        "estimated_time_minutes": 10,
    }
    chapter = {
        "chapter_name": "Chapter One",
        "chapter_number": 2,
        "chapter_type": "understand",
        "chapter_estimated_word_count": 100,
        "chapter_estimated_time_minutes": 10,
        "learning_objectives": [stub],
    }
    packed = {
        "parts": [
            {
                "part_name": "Part One",
                "part_number": 2,
                "understand_chapter_count": 1,
                "chapters": [chapter],
            }
        ],
        "validation": {"valid": True},
    }
    out = build(_COURSE, _BUDGET, packed, {})
    content_part = out["children"][1]
    understand_chapter = content_part["children"][1]
    module = understand_chapter["children"][0]
    assert module["title"]["en"] == "Identify main idea"


def test_unassigned_and_notes_from_validation():
    packed = {
        "parts": [],
        "validation": {
            "valid": False,
            "missing_urns": ["urn:x"],
            "all_parts_gte_4_chapters": False,
        },
        "enforcement_log": "MERGE: a\nRESULT: b\nMERGE: c",
    }
    out = build(_COURSE, _BUDGET, packed, {})
    assert out["unassigned_objective_urns"] == ["urn:x"]
    assert any("Merges applied: 2" in n for n in out["split_notes"])
    assert any(
        "all parts >= 4 understand chapters: False" in n for n in out["split_notes"]
    )
