"""Route definitions for deterministic course-outline structure endpoints."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import status

from api.handlers.course_outline_structure_handler import (
    pack_and_merge_course_outline_structure_handler,
)
from api.models.course_outline_structure.course_outline_structure_models import (
    PackMergeResponse,
)


course_outline_structure_router = APIRouter()

course_outline_structure_router.add_api_route(
    name="Pack And Merge Course Outline Structure",
    path="/v1/course-outline/structure/pack-and-merge",
    endpoint=pack_and_merge_course_outline_structure_handler,
    methods=["POST"],
    tags=["Course Outline Structure"],
    status_code=status.HTTP_200_OK,
    description=(
        "Apply deterministic lesson packing and undersized-part merging to the "
        "planner output before the DCIM Berlin node runs."
    ),
    response_model=PackMergeResponse,
)


def register_routes(application: FastAPI) -> None:
    """Attach the course outline structure router to the application."""
    application.include_router(course_outline_structure_router)
