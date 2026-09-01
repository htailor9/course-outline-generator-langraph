import pytest
from outline.config import Settings
from outline.llm import FakeLLM
from outline.nodes import (
    ingest,
    fan_out_annotate,
    annotate,
    plan_parts,
    fan_out_chapters,
    plan_chapters,
    titles,
)
from outline.schemas import TitlesOut
from outline.state import merge_los
from outline.validate.invariants import BANNED


def cfg(llm, **kw):
    return {"configurable": {"llm": llm, "settings": Settings(**kw)}}


def test_ingest_builds_ids_and_budget(input43):
    out = ingest({"raw_input": input43}, cfg(FakeLLM(), batch_size=10))
    assert len(out["los"]) == 43 and out["los"]["L1"]["urn"].startswith("urn:")
    assert out["budget"] == {"total_lesson_days": 180, "word_limit": 2000}
    assert [len(b) for b in out["batches"]] == [10, 10, 10, 10, 3]
    assert out["course"]["progression"] == "SKILLS_BASED_PROGRESSION"


async def test_annotate_batch_with_fallback(input43):
    st = ingest({"raw_input": input43}, cfg(FakeLLM(), batch_size=10))
    fake = FakeLLM(drop_ids={"L3"})
    sends = fan_out_annotate(st)
    assert len(sends) == 5 and sends[0].node == "annotate"
    out = await annotate(sends[0].arg, cfg(fake))
    assert set(out["los"]) == set(sends[0].arg["batch"])
    assert out["los"]["L1"]["tier"] in ("Foundational", "Intermediate", "Advanced")
    assert "annotate_fallback" in out["los"]["L3"]["flags"]
    assert len(fake.calls) == 2  # first call + one re-ask for missing ids


async def test_plan_parts_covers_all_ids(input43):
    st = ingest({"raw_input": input43}, cfg(FakeLLM()))
    for lo in st["los"].values():
        lo.update(verb="identify", primary_skill="Skill", tier="Foundational")
    fake = FakeLLM(drop_ids={"L5", "L6"})
    out = await plan_parts(st, cfg(fake))
    ids = [i for p in out["parts"] for i in p["ids"]]
    assert sorted(ids) == sorted(st["los"])
    assert out["los"]["L5"]["part_id"] in {p["part_id"] for p in out["parts"]}
    assert "plan_parts_fallback" in out["los"]["L5"]["flags"] or len(fake.calls) == 2


async def test_plan_parts_skill_mode_when_large(input43):
    st = ingest({"raw_input": input43}, cfg(FakeLLM()))
    for i, lo in enumerate(st["los"].values()):
        lo.update(verb="identify", primary_skill=f"Skill {i % 7}", tier="Foundational")
    fake = FakeLLM()
    out = await plan_parts(st, cfg(fake, skill_mode_threshold=10))
    assert "skill | count" in fake.calls[0]["user"]
    assert sorted(i for p in out["parts"] for i in p["ids"]) == sorted(st["los"])


async def test_titles_rejects_banned_title_and_falls_back(input43):
    st = ingest({"raw_input": input43}, cfg(FakeLLM()))
    ids = list(st["los"])[:2]
    for i in ids:
        st["los"][i].update(verb="identify", primary_skill="Skill", tier="Foundational")
    part = {
        "part_number": 1,
        "part_name": "Unit 1",
        "chapters": [
            {
                "chapter_name": "Chapter 1",
                "learning_objectives": [{"id": i} for i in ids],
            }
        ],
    }
    payload = {
        "part": part,
        "los": {i: st["los"][i] for i in ids},
        "course": st["course"],
        "budget": st["budget"],
        "part_names": ["Unit 1"],
    }

    class BannedTitleLLM(FakeLLM):
        async def call(self, role, system, user, schema):
            if role != "titles":
                return await super().call(role, system, user, schema)
            self.calls.append({"role": role, "user": user})
            mods = [{"id": i, "title": "Guided Practice"} for i in ids]
            metric = {
                "role": role,
                "model": "fake",
                "prompt_tokens": 1,
                "completion_tokens": 0,
                "ms": 0,
                "attempt": 1,
            }
            return TitlesOut.model_validate({"modules": mods}), metric

    out = await titles(payload, cfg(BannedTitleLLM()))
    for i in ids:
        assert not BANNED.search(out["titles"][i])
        assert "titles_fallback" in out["los"][i]["flags"]


async def test_plan_chapters_per_part(input43):
    st = ingest({"raw_input": input43}, cfg(FakeLLM()))
    for lo in st["los"].values():
        lo.update(verb="identify", primary_skill="Skill", tier="Foundational")
    patch = await plan_parts(st, cfg(FakeLLM()))
    st["los"] = merge_los(st["los"], patch["los"])
    st["parts"] = patch["parts"]
    sends = fan_out_chapters(st)
    assert len(sends) == len(st["parts"])
    out = await plan_chapters(sends[0].arg, cfg(FakeLLM(drop_ids={"L1"})))
    assert set(out["los"]) == set(sends[0].arg["part"]["ids"])
    assert all("chapter" in v and "rank" in v for v in out["los"].values())
