import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
from outline.config import Settings
from outline.graph import build_graph
from outline.llm import FakeLLM
from outline.report import build_report
from outline.validate.invariants import check

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "make_synthetic.py"


def synthetic(tmp_path: Path, n: int) -> dict:
    out = tmp_path / f"syn-{n}.json"
    subprocess.run([sys.executable, str(SCRIPT), str(n), str(out)], check=True)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data["learning_objectives"]) == n
    return data


def _skewed_input(n: int) -> dict:
    """n LOs sharing identical objective text (unique URNs) so FakeLLM annotation collapses
    them all onto the same primary_skill (and, since verb is derived from the same text, the
    same Bloom's tier) — exercising the > 40-LOs-per-skill pre-split path in one worst case.
    """
    los = [
        {
            "learning_objective_urn": f"urn:pearson:learninggoal:{uuid.uuid4()}",
            "objective": "Analyze underlying structural evidence patterns",
        }
        for _ in range(n)
    ]
    return {
        "course_title": f"Skewed_{n}",
        "grade_band": "MS",
        "subject_area": "Math",
        "minutes_per_lesson": 60,
        "lessons_per_week": 5,
        "course_duration_weeks": 200,
        "course_outline_progression": "SKILLS_BASED_PROGRESSION",
        "learning_objectives": los,
    }


async def test_skewed_skill_distribution():
    inp = _skewed_input(500)
    llm, settings = FakeLLM(), Settings(skill_mode_threshold=300)
    app = build_graph(llm, settings)
    final = await app.ainvoke(
        {"raw_input": inp},
        config={
            "configurable": {"llm": llm, "settings": settings, "thread_id": "skew"}
        },
    )
    assert final["validation"] == []
    plan_parts_call = next(c for c in llm.calls if c["role"] == "plan_parts")
    s_rows = [
        line
        for line in plan_parts_call["user"].splitlines()
        if re.match(r"^S\d+\s*\|", line)
    ]
    assert len(s_rows) >= 5
    assert len(final["parts"]) >= 2


@pytest.mark.parametrize("n", [300, 1000])
async def test_scale_fake(tmp_path, n):
    inp = synthetic(tmp_path, n)
    llm, settings = FakeLLM(), Settings(batch_size=30, skill_mode_threshold=300)
    app = build_graph(llm, settings)
    final = await app.ainvoke(
        {"raw_input": inp},
        config={
            "configurable": {"llm": llm, "settings": settings, "thread_id": f"s{n}"}
        },
    )
    assert final["validation"] == []
    assert (
        check(
            final["outline"],
            [lo["learning_objective_urn"] for lo in inp["learning_objectives"]],
        )
        == []
    )
    rep = build_report(final, "fake", 0)
    assert rep["max_prompt_tokens"] < 10_000
    assert rep["n_los"] == n
    if n > 300:
        assert any(
            "skill | count" in c["user"] for c in llm.calls if c["role"] == "plan_parts"
        )
