"""Context-based unit regeneration: target unit changes, everything else is locked."""

import json
from pathlib import Path

from outline.config import Settings
from outline.graph import build_graph
from outline.llm import FakeLLM
from outline.regen import regenerate_unit, state_from_outline, write_regeneration_note
from outline.report import write
from outline.schemas import ChaptersOut, TitlesOut
from outline.validate.invariants import check


class RenamingFake(FakeLLM):
    """Regeneration-time model: returns different lesson names and module titles."""

    async def call(self, role, system, user, schema):
        out, metric = await super().call(role, system, user, schema)
        if schema is ChaptersOut:
            for a in out.assignments:
                a.chapter_name = "Fresh " + a.chapter_name
        if schema is TitlesOut:
            for t in out.modules:
                t.title = "Reimagined " + t.title
        return out, metric


async def _baseline(tmp_path: Path, input43: dict) -> Path:
    llm, settings = FakeLLM(), Settings()
    app = build_graph(llm, settings)
    cfg = {"configurable": {"llm": llm, "settings": settings, "thread_id": "base"}}
    final = await app.ainvoke({"raw_input": input43}, config=cfg)
    run_dir = tmp_path / "baseline"
    write(
        run_dir,
        final,
        "fake",
        0,
        input_payload=input43,
        run_id="baseline",
        settings=settings,
    )
    return run_dir


def _placements(outline: dict) -> dict:
    """urn -> (unit, lesson, module title) for every LO module."""
    out = {}
    for p in outline["children"]:
        for c in p["children"]:
            for m in c["children"]:
                if m.get("learning_objective_urn"):
                    out[m["learning_objective_urn"]] = (
                        p["title"]["en"],
                        c["title"]["en"],
                        m["title"]["en"],
                    )
    return out


async def test_regenerate_unit_locks_others_and_changes_target(tmp_path, input43):
    run_dir = await _baseline(tmp_path, input43)
    prior_outline = json.loads((run_dir / "outline.json").read_text(encoding="utf-8"))
    _, _, parts, prior_los = state_from_outline(input43, prior_outline)
    assert len(parts) >= 2
    target_name = parts[1]["part_name"]
    target_urns = {prior_los[i]["urn"] for i in parts[1]["ids"]}

    final, info, prior = await regenerate_unit(
        run_dir, "2", "make lesson names fresher", RenamingFake(), Settings()
    )
    urns = [lo["learning_objective_urn"] for lo in input43["learning_objectives"]]
    assert check(final["outline"], urns) == []
    assert final["validation"] == []

    before = _placements(prior_outline)
    after = _placements(final["outline"])
    assert set(before) == set(after)  # 100% coverage preserved

    changed_titles = 0
    for urn, (unit_b, lesson_b, title_b) in before.items():
        unit_a, lesson_a, title_a = after[urn]
        if urn in target_urns:
            changed_titles += title_a != title_b
        else:
            # locked: same unit, same lesson name, same module title
            assert (unit_a, lesson_a, title_a) == (unit_b, lesson_b, title_b), urn
    assert changed_titles > 0  # target really regenerated
    assert any(l.startswith("Fresh ") for l in {after[u][1] for u in target_urns})
    assert info["unit"] == target_name

    out_dir = tmp_path / "regen-out"
    out_dir.mkdir()
    write_regeneration_note(out_dir, final, info)
    note = (out_dir / "regeneration.md").read_text(encoding="utf-8")
    assert "before vs after" in note and target_name in note


async def test_regenerate_unit_selection_by_name_and_errors(tmp_path, input43):
    run_dir = await _baseline(tmp_path, input43)
    prior_outline = json.loads((run_dir / "outline.json").read_text(encoding="utf-8"))
    _, _, parts, _ = state_from_outline(input43, prior_outline)
    final, info, _ = await regenerate_unit(
        run_dir, parts[0]["part_name"], None, RenamingFake(), Settings()
    )
    assert info["unit"] == parts[0]["part_name"]
    assert final["validation"] == []
    import pytest

    with pytest.raises(SystemExit):
        await regenerate_unit(run_dir, "99", None, RenamingFake(), Settings())


async def test_regenerate_full_passes_prior_outline_context(tmp_path, input43):
    from outline.regen import regenerate_full, write_full_regeneration_note

    run_dir = await _baseline(tmp_path, input43)
    fake = RenamingFake()
    final, info = await regenerate_full(run_dir, "broader units", fake, Settings())
    assert final["validation"] == []
    urns = [lo["learning_objective_urn"] for lo in input43["learning_objectives"]]
    assert check(final["outline"], urns) == []
    # the previous outline's structure reached the planning prompts
    plan_calls = [c for c in fake.calls if c["role"] == "plan_parts"]
    assert plan_calls and "PREVIOUS UNIT" in plan_calls[0]["user"]
    assert info["prior_units"] and info["new_units"]
    out_dir = tmp_path / "full-out"
    out_dir.mkdir()
    write_full_regeneration_note(out_dir, final, info)
    assert "before vs after" in (out_dir / "regeneration.md").read_text(
        encoding="utf-8"
    )


async def test_regenerate_lesson_only_changes_that_lessons_titles(tmp_path, input43):
    from outline.regen import regenerate_lesson, write_lesson_regeneration_note

    run_dir = await _baseline(tmp_path, input43)
    prior_outline = json.loads((run_dir / "outline.json").read_text(encoding="utf-8"))
    final, info, _ = await regenerate_lesson(
        run_dir, "1", "1", "more applied titles", RenamingFake(), Settings()
    )
    urns = [lo["learning_objective_urn"] for lo in input43["learning_objectives"]]
    assert check(final["outline"], urns) == []
    assert final["validation"] == []
    before, after = _placements(prior_outline), _placements(final["outline"])
    assert set(before) == set(after)
    changed = 0
    for urn in before:
        ub, lb, tb = before[urn]
        ua, la, ta = after[urn]
        assert (ua, la) == (ub, lb), urn  # placements + lesson names fully locked
        if lb == info["lesson"] and ub == info["unit"]:
            changed += ta != tb
        else:
            assert ta == tb, urn  # every other module title locked
    assert changed > 0
    out_dir = tmp_path / "lesson-out"
    out_dir.mkdir()
    write_lesson_regeneration_note(out_dir, final, info)
    assert info["lesson"] in (out_dir / "regeneration.md").read_text(encoding="utf-8")


async def test_regenerate_lesson_bad_selection_lists_options(tmp_path, input43):
    from outline.regen import regenerate_lesson

    run_dir = await _baseline(tmp_path, input43)
    import pytest

    with pytest.raises(SystemExit, match="regenerable"):
        await regenerate_lesson(run_dir, "1", "99", None, RenamingFake(), Settings())
