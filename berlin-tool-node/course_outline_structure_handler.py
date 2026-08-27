"""FastAPI handlers for deterministic course-outline structure endpoints."""

from __future__ import annotations

import logging
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

from api.models.course_outline_structure.course_outline_structure_models import (
    PackMergeRequest,
    PackMergeResponse,
)
from api.services.course_outline_structure_service import (
    pack_and_merge_course_outline_structure,
)


async def pack_and_merge_course_outline_structure_handler(
    request: PackMergeRequest = Body(...),
) -> PackMergeResponse:
    """Return deterministic packed and merged course-outline structure."""
    try:
        return pack_and_merge_course_outline_structure(request)

    except ValueError as exc:
        error_message = str(exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": error_message,
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "data": {
                    "detail": "Validation failed — check grouping_plan and annotated_objectives.",
                    "validation_errors": error_message,
                },
            },
        )

    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": str(exc.detail),
                "status": exc.status_code,
                "data": {
                    "detail": str(exc.detail),
                },
            },
        )

    except Exception as exc:
        logger.exception("Unexpected error while enforcing course outline structure")
        error_message = str(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": error_message,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": {
                    "detail": "Unexpected error while enforcing course outline structure.",
                    "error_message": error_message,
                },
            },
        )
