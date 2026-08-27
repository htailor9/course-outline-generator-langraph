"""All Pydantic contracts: input request, LLM structured outputs, DCIM output."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Progression = Literal[
    "SKILLS_BASED_PROGRESSION",
    "THEME_BASED_PROGRESSION",
    "CHRONOLOGICAL_PROGRESSION",
    "STANDARDS_DRIVEN_PROGRESSION",
]
Tier = Literal["Foundational", "Intermediate", "Advanced"]


# ---------- input ----------
class LearningObjectiveIn(BaseModel):
    learning_objective_urn: str = Field(min_length=1)
    objective: str = Field(min_length=1)


class CourseRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    course_title: str = Field(min_length=1)
    grade_band: str = Field(min_length=1)
    subject_area: str = Field(min_length=1)
    minutes_per_lesson: int = Field(gt=0)
    lessons_per_week: int = Field(gt=0, le=7)
    course_duration_weeks: int = Field(gt=0)
    course_outline_progression: Progression
    learning_objectives: list[LearningObjectiveIn] = Field(min_length=1)
    user_prompt: str | None = None


# ---------- LLM outputs (ID-keyed deltas only) ----------
class AnnotateItem(BaseModel):
    id: str
    verb: str = Field(min_length=1)
    primary_skill: str = Field(min_length=2, max_length=60)


class AnnotateOut(BaseModel):
    items: list[AnnotateItem]


class PartItem(BaseModel):
    part_name: str = Field(min_length=2, max_length=80)
    ids: list[str] = Field(min_length=1)


class PartsOut(BaseModel):
    parts: list[PartItem] = Field(min_length=1)


class ChapterItem(BaseModel):
    id: str
    chapter_name: str = Field(min_length=2, max_length=80)
    order_rank: int = Field(ge=1)


class ChaptersOut(BaseModel):
    assignments: list[ChapterItem]


class TitleItem(BaseModel):
    id: str
    title: str = Field(min_length=3, max_length=80)


class TitlesOut(BaseModel):
    modules: list[TitleItem]


# ---------- DCIM output ----------
class Title(BaseModel):
    en: str


class Module(BaseModel):
    model_config = ConfigDict(extra="allow")
    label: Literal["module"]
    type: str
    module_number: int
    title: Title
    learning_objective_urn: str | None = None
    estimated_word_count: int | None = None
    estimated_time_minutes: int | None = None
    primary_skill: str | None = None
    blooms_level: str | None = None


class Chapter(BaseModel):
    model_config = ConfigDict(extra="allow")
    label: Literal["chapter"]
    type: str
    chapter_number: int
    title: Title
    chapter_estimated_word_count: int | None = None
    chapter_estimated_time_minutes: int | None = None
    children: list[Module]


class Part(BaseModel):
    model_config = ConfigDict(extra="allow")
    label: Literal["part"]
    type: Literal["overview", "understand", "semester"]
    part_number: int
    title: Title
    children: list[Chapter]


class Outline(BaseModel):
    model_config = ConfigDict(extra="allow")
    course_title: str
    grade_band: str
    subject_area: str
    chapter_word_count_limit: int
    total_parts: int
    total_chapters: int
    title: Title
    label: Literal["project"]
    children: list[Part]
    total_lesson_days: int
    total_chapters_in_course: int
    pacing_overrun: bool
    pacing_overrun_lesson_days: int | None
    split_notes: list[str] | str | None
    unassigned_objective_urns: list[str]
