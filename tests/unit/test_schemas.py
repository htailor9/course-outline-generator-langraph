import pytest
from pydantic import ValidationError
from outline.schemas import CourseRequest, AnnotateOut, PartsOut, ChaptersOut, TitlesOut, Outline


def test_course_request_accepts_sample(input43):
    req = CourseRequest.model_validate(input43)
    assert req.course_outline_progression == "SKILLS_BASED_PROGRESSION"
    assert len(req.learning_objectives) == 43
    assert req.minutes_per_lesson == 60


def test_course_request_rejects_empty_los(input43):
    bad = {**input43, "learning_objectives": []}
    with pytest.raises(ValidationError):
        CourseRequest.model_validate(bad)


def test_llm_schemas_roundtrip():
    a = AnnotateOut.model_validate({"items": [{"id": "L1", "verb": "identify", "primary_skill": "Main Idea"}]})
    assert a.items[0].id == "L1"
    p = PartsOut.model_validate({"parts": [{"part_name": "Logic", "ids": ["L1", "L2"]}]})
    assert p.parts[0].ids == ["L1", "L2"]
    c = ChaptersOut.model_validate({"assignments": [{"id": "L1", "chapter_name": "Fallacies", "order_rank": 1}]})
    assert c.assignments[0].order_rank == 1
    t = TitlesOut.model_validate({"modules": [{"id": "L1", "title": "Logical Fallacy Identification"}]})
    assert t.modules[0].title.startswith("Logical")


def test_outline_accepts_golden(golden43):
    o = Outline.model_validate(golden43)
    assert o.total_parts == 10
    assert o.children[0].type == "overview"
    assert o.children[1].children[1].children[0].learning_objective_urn.startswith("urn:")
