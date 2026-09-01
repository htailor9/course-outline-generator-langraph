import pytest
from outline.config import Settings
from outline.graph import build_graph
from outline.llm import FakeLLM
from outline.schemas import Outline
from outline.validate.invariants import check


async def run(inp, llm=None, **kw):
    llm = llm or FakeLLM()
    settings = Settings(**kw)
    app = build_graph(llm, settings)
    cfg = {"configurable": {"llm": llm, "settings": settings, "thread_id": "t1"}}
    return await app.ainvoke({"raw_input": inp}, config=cfg)


@pytest.mark.parametrize("fixture", ["input43", "input94", "input123"])
async def test_end_to_end_valid(fixture, request):
    inp = request.getfixturevalue(fixture)
    final = await run(inp, batch_size=30)
    out = final["outline"]
    Outline.model_validate(out)
    assert final["validation"] == []
    assert (
        check(out, [lo["learning_objective_urn"] for lo in inp["learning_objectives"]])
        == []
    )
    n_content = sum(1 for p in out["children"] if p["type"] == "understand")
    assert out["total_parts"] == 1 + n_content + 2
    assert out["total_chapters"] == sum(len(p["children"]) for p in out["children"])
    assert all(len(b) <= 30 for b in final["batches"])


async def test_fallbacks_still_produce_valid_outline(input43):
    fake = FakeLLM(drop_ids={"L2", "L7", "L40"})
    final = await run(input43, llm=fake)
    assert final["validation"] == []
    flagged = [i for i, lo in final["los"].items() if lo.get("flags")]
    assert flagged


async def test_standards_driven_preserves_input_order(input43):
    """STUDIOPE-243: standards mode must yield strict input order even if the model reorders."""
    from outline.schemas import ChaptersOut, PartsOut

    class ReorderingFake(FakeLLM):
        async def call(self, role, system, user, schema):
            out, metric = await super().call(role, system, user, schema)
            if schema is PartsOut:
                out.parts.reverse()  # model returns units backwards
            if schema is ChaptersOut:
                n = len(out.assignments)
                for k, a in enumerate(
                    out.assignments
                ):  # model returns descending ranks
                    a.order_rank = n - k
            return out, metric

    inp = {**input43, "course_outline_progression": "STANDARDS_DRIVEN_PROGRESSION"}
    final = await run(inp, llm=ReorderingFake())
    assert final["validation"] == []
    urns = [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]
    pos = {u: i for i, u in enumerate(urns)}
    placed = [
        m["learning_objective_urn"]
        for p in final["outline"]["children"]
        for c in p["children"]
        for m in c["children"]
        if m.get("learning_objective_urn")
    ]
    seq = [pos[u] for u in placed]
    assert seq == sorted(seq), "standards-driven output must match input order exactly"


async def test_llm_failure_in_titles_uses_fallback(input43):
    fake = FakeLLM(fail_roles={"titles"})
    final = await run(input43, llm=fake)
    assert final["validation"] == []
    assert all("titles_fallback" in lo.get("flags", []) for lo in final["los"].values())
