"""Shared service layer: transport-agnostic generation/regeneration used by CLI and API."""

import pytest

from outline.config import Settings
from outline.llm import FakeLLM
from outline.prompt_guard import PromptRejected
from outline.service import run_generation, run_regeneration


async def test_run_generation_writes_folder_and_report(tmp_path, input43):
    run_dir, rep = await run_generation(
        input43, Settings(), FakeLLM(), runs_dir=tmp_path
    )
    assert run_dir.parent == tmp_path
    assert (run_dir / "outline.json").exists() and (run_dir / "analysis.md").exists()
    assert rep["n_los"] == 43 and rep["validation"] == []


async def test_run_generation_rejects_bad_prompt(tmp_path, input43):
    bad = {**input43, "user_prompt": "buy pizza tomorrow"}
    with pytest.raises(PromptRejected):
        await run_generation(bad, Settings(), FakeLLM(), runs_dir=tmp_path)


async def test_run_generation_progress_callback(tmp_path, input43):
    seen: list[str] = []
    await run_generation(
        input43,
        Settings(),
        FakeLLM(),
        runs_dir=tmp_path,
        progress=lambda node, update: seen.append(node),
    )
    assert "ingest" in seen and "validate" in seen


async def test_run_regeneration_all_scopes(tmp_path, input43):
    base_dir, _ = await run_generation(
        input43, Settings(), FakeLLM(), runs_dir=tmp_path
    )
    for unit, lesson in [("all", None), ("1", None), ("1", "1")]:
        run_dir, rep = await run_regeneration(
            base_dir, unit, lesson, None, Settings(), FakeLLM(), runs_dir=tmp_path
        )
        assert rep["validation"] == []
        assert (run_dir / "regeneration.md").exists()


async def test_run_regeneration_bad_baseline(tmp_path):
    with pytest.raises(FileNotFoundError):
        await run_regeneration(
            tmp_path / "nope",
            "all",
            None,
            None,
            Settings(),
            FakeLLM(),
            runs_dir=tmp_path,
        )
