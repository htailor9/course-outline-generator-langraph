"""Graph state: one ID-keyed copy of LO data + small aggregates. Nodes return partial dicts."""

import operator
from typing import Annotated, TypedDict


class LO(TypedDict, total=False):
    id: str
    urn: str
    text: str
    idx: int
    verb: str
    primary_skill: str
    tier: str
    part_id: str
    chapter: str
    rank: int
    title: str
    flags: list[str]


def merge_los(a: dict[str, LO], b: dict[str, LO]) -> dict[str, LO]:
    out = {k: dict(v) for k, v in a.items()}
    for k, patch in b.items():
        cur = out.get(k, {})
        merged = {**cur, **patch}
        flags = list(cur.get("flags", [])) + [
            f for f in patch.get("flags", []) if f not in cur.get("flags", [])
        ]
        if flags:
            merged["flags"] = flags
        out[k] = merged
    return out


def merge_dict(a: dict, b: dict) -> dict:
    return {**a, **b}


class State(TypedDict, total=False):
    raw_input: dict
    course: dict  # course_title, grade_band, subject_area, minutes_per_lesson, lessons_per_week, course_duration_weeks, progression, user_prompt
    budget: dict  # total_lesson_days, word_limit
    batches: list[list[str]]
    los: Annotated[dict[str, LO], merge_los]
    parts: list[dict]  # [{"part_id", "part_name", "ids"}]
    packed: dict
    titles: Annotated[dict[str, str], merge_dict]
    outline: dict
    validation: list[str]
    report: Annotated[list[dict], operator.add]
