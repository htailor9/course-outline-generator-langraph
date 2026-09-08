"""REST API for course-outline generation and regeneration.

Async job model: every POST returns 202 with a `run_id` (== the run-folder name on disk);
poll GET /v1/outline/runs/{run_id}, then fetch artifacts. Completed runs survive server
restarts because the folder IS the persistence. Swagger UI at /docs, OpenAPI at /openapi.json.

Run:  uvicorn outline.api:app --port 8000            (single worker — in-memory job registry)
Env:  OUTLINE_RUNS_DIR (default "runs") · OUTLINE_CONFIG (default "config.yaml")
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from outline.config import load
from outline.jobs import registry
from outline.llm import FakeLLM, make_llm
from outline.prompt_guard import (
    PromptRejected,
    course_vocab_from_input,
    validate_user_prompt,
)
from outline.report import make_run_dir
from outline.service import run_generation, run_regeneration

RUN_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")

app = FastAPI(
    title="Course Outline Generator API",
    version="1.0.0",
    description=(
        "Generate and regenerate DCIM course outlines from learning objectives.\n\n"
        "**Async job model**: POST returns `202 {run_id}` immediately; poll "
        "`GET /v1/outline/runs/{run_id}` until `done`, then fetch `/outline`, `/report`, "
        "`/analysis` (or `/regeneration` for regen runs). The `run_id` is the run folder on "
        "disk, so completed runs remain available after a server restart.\n\n"
        "Regeneration scopes: `unit='all'` (full course, previous outline passed as context), "
        "`unit='2'` (one unit, others locked), `unit='1', lesson='2'` (one lesson's module "
        "titles only). `prompt` is optional user guidance with explicit priority; invalid or "
        "unrelated prompts are rejected with 400 before any model call."
    ),
    openapi_tags=[
        {"name": "generate", "description": "Create a new course outline"},
        {
            "name": "regenerate",
            "description": "Regenerate a prior run (full / unit / lesson)",
        },
        {"name": "runs", "description": "Job status, run listing and artifacts"},
        {"name": "meta", "description": "Health and service info"},
    ],
)


def _runs_dir() -> Path:
    d = Path(os.environ.get("OUTLINE_RUNS_DIR", "runs"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _settings_and_llm(
    provider: str | None, model: str | None, batch_size: int | None = None
):
    settings = load(
        os.environ.get("OUTLINE_CONFIG", "config.yaml"),
        provider=provider,
        batch_size=batch_size,
    )
    if provider == "claude_cli" and not model:
        settings.models = {
            "default": "sonnet",
            "annotate": "sonnet",
            "titles": "sonnet",
        }
    if model:
        settings.models = {"default": model, "annotate": model, "titles": model}
    if provider == "fake":
        settings.provider = "fake"
        return settings, FakeLLM()
    return settings, make_llm(settings)


class JobAccepted(BaseModel):
    run_id: str = Field(examples=["20260908-153000_43LOs_Test-Math_claude_cli"])
    status: str = Field(default="queued", examples=["queued"])


class RegenerateRequest(BaseModel):
    baseline_run_id: str | None = Field(
        default=None, description="run_id of a prior run under the runs dir (preferred)"
    )
    baseline_dir: str | None = Field(
        default=None,
        description="absolute/relative path to a prior run folder (alternative)",
    )
    unit: str = Field(
        description="'all' = full course; '2' or exact unit name = one unit",
        examples=["all", "2", "Counting Combinatorics & Number Systems"],
    )
    lesson: str | None = Field(
        default=None,
        description="lesson number or exact name within --unit (module titles only); not with unit='all'",
    )
    prompt: str | None = Field(
        default=None, examples=["make lesson names more application-focused"]
    )
    provider: str | None = Field(
        default=None, examples=["claude_cli", "anthropic", "fake"]
    )
    model: str | None = Field(default=None, examples=["sonnet"])


@app.get("/healthz", tags=["meta"])
def healthz() -> dict:
    return {"ok": True}


@app.post(
    "/v1/outline/generate",
    status_code=202,
    response_model=JobAccepted,
    tags=["generate"],
    summary="Generate a course outline (async)",
    description=(
        "Body = the standard input payload (course_title, grade_band, learning_objectives[], …) "
        "plus optional `provider` (`fake` runs offline), `model`, `batch_size`. Returns 202 with "
        "the run_id to poll. A bad `user_prompt` returns 400 immediately (nothing queued)."
    ),
)
async def generate(payload: dict = Body(...)) -> JobAccepted:
    provider = payload.pop("provider", None)
    model = payload.pop("model", None)
    batch_size = payload.pop("batch_size", None)
    try:
        validate_user_prompt(
            payload.get("user_prompt"), course_vocab_from_input(payload)
        )
        settings, llm = _settings_and_llm(provider, model, batch_size)
    except PromptRejected as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # bad provider/model config
        raise HTTPException(status_code=422, detail=str(exc))
    runs_dir = _runs_dir()
    provider_name = "fake" if provider == "fake" else settings.provider
    run_dir, run_id = make_run_dir(
        runs_dir,
        payload.get("course_title", "course"),
        provider_name,
        n_los=len(payload.get("learning_objectives", [])),
    )
    registry.submit(
        run_id,
        run_generation(payload, settings, llm, runs_dir=runs_dir, out=run_dir),
    )
    return JobAccepted(run_id=run_id)


@app.post(
    "/v1/outline/regenerate",
    status_code=202,
    response_model=JobAccepted,
    tags=["regenerate"],
    summary="Regenerate a prior run (full / unit / lesson, async)",
)
async def regenerate(req: RegenerateRequest) -> JobAccepted:
    runs_dir = _runs_dir()
    if req.baseline_run_id:
        if not RUN_ID_RE.match(req.baseline_run_id):
            raise HTTPException(status_code=422, detail="invalid baseline_run_id")
        baseline = runs_dir / req.baseline_run_id
    elif req.baseline_dir:
        baseline = Path(req.baseline_dir)
    else:
        raise HTTPException(
            status_code=422, detail="baseline_run_id or baseline_dir is required"
        )
    if not (baseline / "outline.json").exists():
        raise HTTPException(
            status_code=404, detail=f"baseline run not found: {baseline.name}"
        )
    try:
        baseline_input = json.loads(
            (baseline / "input.json").read_text(encoding="utf-8")
        )
        validate_user_prompt(req.prompt, course_vocab_from_input(baseline_input))
        settings, llm = _settings_and_llm(req.provider, req.model)
    except PromptRejected as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    if req.lesson and req.unit.strip().lower() == "all":
        raise HTTPException(
            status_code=422, detail="lesson requires a specific unit (not 'all')"
        )
    # run_id is decided by the service (depends on regenerated scope); reserve a provisional id
    # by submitting under a placeholder that the wrapper rewrites is complex — instead run the
    # service and let it name the folder; we track the job under a deterministic ticket id.
    ticket = (
        f"regen-{baseline.name}-{req.unit}-{req.lesson or 'x'}-{os.urandom(3).hex()}"
    )
    ticket = re.sub(r"[^A-Za-z0-9._-]+", "-", ticket)

    async def job():
        return await run_regeneration(
            baseline, req.unit, req.lesson, req.prompt, settings, llm, runs_dir=runs_dir
        )

    registry.submit(ticket, job())
    return JobAccepted(run_id=ticket)


@app.get(
    "/v1/outline/runs",
    tags=["runs"],
    summary="List runs (completed folders + live jobs)",
)
def list_runs() -> list[dict]:
    runs_dir = _runs_dir()
    out = []
    for folder in sorted(runs_dir.iterdir()):
        rep = folder / "report.json"
        if not rep.exists():
            continue
        try:
            r = json.loads(rep.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        out.append(
            {
                "run_id": folder.name,
                "n_los": r.get("n_los"),
                "provider": r.get("provider"),
                "started_at": r.get("started_at"),
                "valid": r.get("validation") == [],
                "status": "done",
            }
        )
    for job_id, st in ((j, registry.status(j)) for j in list(registry._jobs)):
        if st["status"] in ("queued", "running", "failed"):
            out.append(
                {
                    "run_id": job_id,
                    "status": st["status"],
                    **({"error": st["error"]} if "error" in st else {}),
                }
            )
    return out


@app.get(
    "/v1/outline/runs/{run_id}",
    tags=["runs"],
    summary="Job/run status (+ report when done)",
)
def run_status(run_id: str) -> dict:
    if not RUN_ID_RE.match(run_id):
        raise HTTPException(status_code=422, detail="invalid run_id")
    st = registry.resolve(run_id, _runs_dir())
    if st["status"] == "unknown":
        raise HTTPException(status_code=404, detail=f"unknown run_id: {run_id}")
    if st["status"] == "done" and "report" not in st:
        rep = Path(st["run_dir"]) / "report.json"
        if rep.exists():
            st["report"] = json.loads(rep.read_text(encoding="utf-8"))
    return st


_ARTIFACTS = {
    "outline": ("outline.json", "application/json"),
    "report": ("report.json", "application/json"),
    "analysis": ("analysis.md", "text/markdown"),
    "regeneration": ("regeneration.md", "text/markdown"),
    "enforcement": ("enforcement.log", "text/plain"),
    "input": ("input.json", "application/json"),
}


@app.get(
    "/v1/outline/runs/{run_id}/{artifact}",
    tags=["runs"],
    summary="Fetch a run artifact",
)
def run_artifact(run_id: str, artifact: str):
    if not RUN_ID_RE.match(run_id) or artifact not in _ARTIFACTS:
        raise HTTPException(
            status_code=422, detail=f"artifact must be one of {sorted(_ARTIFACTS)}"
        )
    st = registry.resolve(run_id, _runs_dir())
    run_dir = Path(st["run_dir"]) if st.get("run_dir") else _runs_dir() / run_id
    resolved = run_dir.resolve()
    if (
        _runs_dir().resolve() not in resolved.parents
        and resolved != _runs_dir().resolve()
    ):
        raise HTTPException(status_code=404, detail="run not found")
    fname, media = _ARTIFACTS[artifact]
    path = resolved / fname
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{fname} not present for {run_id}")
    if media == "application/json":
        return JSONResponse(json.loads(path.read_text(encoding="utf-8")))
    return FileResponse(path, media_type=media)
