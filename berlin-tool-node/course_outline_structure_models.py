"""Request and response models for course outline structure endpoints."""

from __future__ import annotations

import json
from typing import Literal
from pydantic import BaseModel, Field, model_validator


class GroupingAssignment(BaseModel):
    """Single planner assignment for one learning objective."""

    learning_objective_urn: str = Field(..., alias="learning_objective_urn", min_length=1)
    chapter_name: str = Field(..., min_length=1)
    part_name: str = Field(..., min_length=1)
    order_rank: int = Field(..., ge=1)

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class GroupingPlan(BaseModel):
    """Planner output forwarded to the deterministic pack-and-merge step."""

    progression_type: str = Field(..., min_length=1)
    assignments: list[GroupingAssignment] = Field(..., min_length=1)
    parts_metadata: list[dict] | None = Field(default=None, alias="parts_metadata")
    merge_notes: str | None = Field(default=None, alias="merge_notes")
    split_notes: str | None = Field(default=None, alias="split_notes")
    unassigned_objective_urns: list[str] = Field(
        default_factory=list,
        alias="unassigned_objective_urns",
    )
    planning_notes: str | None = Field(default=None, alias="planning_notes")

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class AnnotatedObjective(BaseModel):
    """Learning objective enriched by the analyzer node."""

    learning_objective_urn: str = Field(..., alias="learning_objective_urn", min_length=1)
    objective: str = Field(..., min_length=1)
    verb: str = Field(..., min_length=1)
    primary_skill: str = Field(..., alias="primary_skill", min_length=1)
    blooms_level: Literal["Foundational", "Intermediate", "Advanced"] = Field(
        ...,
        alias="blooms_level",
    )

    @model_validator(mode="before")
    @classmethod
    def preprocess_objective_fields(cls, data: dict | str) -> dict | str:
        """Handle stringified JSON, field alias fallback (lo_text -> objective), and casing."""
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return data
        if isinstance(data, dict):
            # Fallback lo_text -> objective if objective is missing
            if not data.get("objective") and data.get("lo_text"):
                data["objective"] = data["lo_text"]
            # Normalize blooms_level string casing
            blooms = data.get("blooms_level")
            if isinstance(blooms, str):
                blooms_clean = blooms.strip().capitalize()
                if blooms_clean in ("Foundational", "Intermediate", "Advanced"):
                    data["blooms_level"] = blooms_clean
        return data

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class AnnotatedObjectivesPayload(BaseModel):
    """Analyzer payload forwarded through the planner."""

    objectives: list[AnnotatedObjective] = Field(..., min_length=1)
    course_title: str = Field(..., alias="course_title", min_length=1)
    grade_band: str = Field(..., alias="grade_band", min_length=1)
    subject_area: str = Field(..., alias="subject_area", min_length=1)
    minutes_per_lesson: int = Field(..., alias="minutes_per_lesson", gt=0)
    lessons_per_week: int = Field(..., alias="lessons_per_week", gt=0)
    course_duration_weeks: int = Field(..., alias="course_duration_weeks", gt=0)
    user_prompt: str | None = Field(default=None, alias="user_prompt")
    PearsonExtSSOSession: str | None = Field(default=None, alias="PearsonExtSSOSession")
    total_input_lo_count: int | None = Field(
        default=None,
        alias="total_input_lo_count",
        ge=1,
    )
    input_duplicate_urns: list[str] = Field(
        default_factory=list,
        alias="input_duplicate_urns",
    )

    @model_validator(mode="before")
    @classmethod
    def preprocess_payload(cls, data: dict | str) -> dict | str:
        """Parse stringified objectives array or nested JSON strings."""
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return data
        if isinstance(data, dict):
            if isinstance(data.get("objectives"), str):
                try:
                    data["objectives"] = json.loads(data["objectives"])
                except Exception:
                    pass
        return data

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class PackMergeRequest(BaseModel):
    """Request body for deterministic course-outline structure enforcement."""

    grouping_plan: GroupingPlan = Field(..., alias="grouping_plan")
    annotated_objectives: AnnotatedObjectivesPayload = Field(
        ...,
        alias="annotated_objectives",
    )
    chapter_word_count_limit: int | None = Field(
        default=None,
        alias="chapter_word_count_limit",
        gt=0,
    )

    @model_validator(mode="before")
    @classmethod
    def parse_stringified_json_fields(cls, data: dict | str) -> dict | str:
        """Parse stringified JSON strings if Berlin Studio passes them wrapped in quotes."""
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return data
        if isinstance(data, dict):
            # Recursively unwrap stringified grouping_plan
            gp = data.get("grouping_plan")
            while isinstance(gp, str):
                try:
                    gp = json.loads(gp)
                except Exception:
                    break
            data["grouping_plan"] = gp

            # Recursively unwrap stringified annotated_objectives
            ao = data.get("annotated_objectives")
            while isinstance(ao, str):
                try:
                    ao = json.loads(ao)
                except Exception:
                    break
            data["annotated_objectives"] = ao

        return data

    model_config = {"populate_by_name": True}


class StructuredLearningObjective(BaseModel):
    """Learning objective module stub."""

    urn: str = Field(..., min_length=1)
    module_number: int = Field(..., alias="module_number", ge=1)
    objective: str = Field(..., min_length=1)
    lo_text: str = Field(default="", alias="lo_text")
    primary_skill: str = Field(..., alias="primary_skill", min_length=1)
    blooms_level: str = Field(default="", alias="blooms_level")
    source_chapter_name: str = Field(..., alias="source_chapter_name", min_length=1)
    estimated_word_count: int = Field(..., alias="estimated_word_count", ge=1)
    estimated_time_minutes: int = Field(..., alias="estimated_time_minutes", ge=1)
    module_title: str | None = Field(default=None, alias="module_title")

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class StructuredChapter(BaseModel):
    """One enforced understand chapter consumed by the DCIM node."""

    chapter_name: str = Field(..., alias="chapter_name", min_length=1)
    chapter_number: int = Field(..., alias="chapter_number", ge=1)
    chapter_type: Literal["understand"] = Field(default="understand", alias="chapter_type")
    chapter_estimated_word_count: int = Field(
        ...,
        alias="chapter_estimated_word_count",
        ge=1,
    )
    chapter_estimated_time_minutes: int = Field(
        ...,
        alias="chapter_estimated_time_minutes",
        ge=1,
    )
    learning_objectives: list[StructuredLearningObjective] = Field(
        ...,
        alias="learning_objectives",
        min_length=1,
    )

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class StructuredPart(BaseModel):
    """One enforced content part consumed by the DCIM node."""

    part_name: str = Field(..., alias="part_name", min_length=1)
    part_number: int = Field(..., alias="part_number", ge=2)
    understand_chapter_count: int = Field(..., alias="understand_chapter_count", ge=1)
    chapters: list[StructuredChapter] = Field(..., min_length=1)

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class StructureValidationSummary(BaseModel):
    """Validation summary emitted by the pack-and-merge step."""

    total_input_los: int = Field(..., alias="total_input_los", ge=0)
    total_placed_los: int = Field(..., alias="total_placed_los", ge=0)
    all_parts_gte_4_chapters: bool = Field(..., alias="all_parts_gte_4_chapters")
    duplicate_urns: list[str] = Field(default_factory=list, alias="duplicate_urns")
    missing_urns: list[str] = Field(default_factory=list, alias="missing_urns")
    extra_urns: list[str] = Field(default_factory=list, alias="extra_urns")
    valid: bool = Field(...)

    model_config = {"populate_by_name": True}


class PackMergeResponse(BaseModel):
    """Response body for the deterministic pack-and-merge step."""

    course_title: str = Field(..., alias="course_title", min_length=1)
    grade_band: str = Field(..., alias="grade_band", min_length=1)
    subject_area: str = Field(..., alias="subject_area", min_length=1)
    chapter_word_count_limit: int = Field(..., alias="chapter_word_count_limit", gt=0)
    minutes_per_lesson_day: int = Field(..., alias="minutes_per_lesson_day", gt=0)
    total_lesson_days: int = Field(..., alias="total_lesson_days", gt=0)
    progression_type: str = Field(..., alias="progression_type", min_length=1)
    annotated_objectives: AnnotatedObjectivesPayload = Field(
        ...,
        alias="annotated_objectives",
    )
    enforcement_log: str = Field(..., alias="enforcement_log")
    parts: list[StructuredPart] = Field(..., min_length=1)
    validation: StructureValidationSummary = Field(...)
    content_chapter_count: int = Field(..., alias="content_chapter_count", ge=0)
    num_content_parts: int = Field(..., alias="num_content_parts", ge=0)
    total_chapter_count: int = Field(..., alias="total_chapter_count", ge=0)

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}
