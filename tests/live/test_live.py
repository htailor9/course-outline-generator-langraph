import os
import pytest
from outline.config import load
from outline.graph import build_graph
from outline.llm import LLM

pytestmark = pytest.mark.live


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"), reason="needs ANTHROPIC_API_KEY"
)
async def test_live_43(input43):
    settings = load("config.yaml", provider="anthropic")
    llm = LLM(settings)
    app = build_graph(llm, settings)
    final = await app.ainvoke(
        {"raw_input": input43},
        config={
            "configurable": {"llm": llm, "settings": settings, "thread_id": "live43"}
        },
    )
    assert final["validation"] == []
    assert not any(lo.get("flags") for lo in final["los"].values())
