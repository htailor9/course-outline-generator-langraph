import asyncio

import pytest
from langchain_core.messages import AIMessage

from outline.config import Settings
from outline.llm import LLM, render, FakeLLM
from outline.schemas import AnnotateOut, PartsOut, ChaptersOut, TitlesOut
from outline.state import merge_los


class _StubStructured:
    """Stand-in for `model.with_structured_output(...)`: returns queued results in order."""

    def __init__(self, results: list[dict]):
        self._results = list(results)

    async def ainvoke(self, messages):
        return self._results.pop(0)


class _StubModel:
    def __init__(self, results: list[dict]):
        self._results = results

    def with_structured_output(self, schema, include_raw=True):
        return _StubStructured(self._results)


async def test_llm_call_corrective_retry_on_schema_failure():
    good = AnnotateOut.model_validate(
        {"items": [{"id": "L1", "verb": "identify", "primary_skill": "Main Idea"}]}
    )
    bad_result = {
        "parsed": None,
        "raw": AIMessage(
            content="x",
            usage_metadata={"input_tokens": 5, "output_tokens": 1, "total_tokens": 6},
        ),
        "parsing_error": "bad",
    }
    good_result = {
        "parsed": good,
        "raw": AIMessage(
            content="y",
            usage_metadata={"input_tokens": 5, "output_tokens": 1, "total_tokens": 6},
        ),
        "parsing_error": None,
    }

    llm = LLM.__new__(LLM)
    llm.settings = Settings()
    llm._models = {"default": _StubModel([bad_result, good_result])}
    llm._sem = asyncio.Semaphore(5)

    out, metric = await llm.call("annotate", "sys", "user", AnnotateOut)

    assert out == good
    assert metric["attempt"] == 2
    assert metric["prompt_tokens"] == 5
    assert metric["completion_tokens"] == 1


def test_render_splits_system_and_user():
    system, user = render("annotate", header="H", rows="L1 | Identify the main idea")
    assert "verb" in system.lower()
    assert "L1 | Identify the main idea" in user
    assert "{rows}" not in user and "{header}" not in user


async def test_fake_annotate_and_drop():
    fake = FakeLLM(drop_ids={"L2"})
    out, metric = await fake.call(
        "annotate",
        "sys",
        "L1 | Identify the main idea\nL2 | Analyze evidence",
        AnnotateOut,
    )
    assert [i.id for i in out.items] == ["L1"]
    assert out.items[0].verb == "identify"
    assert metric["role"] == "annotate" and metric["prompt_tokens"] > 0


async def test_fake_parts_chapters_titles():
    fake = FakeLLM()
    rows = "\n".join(f"L{i} | Skill {i // 3} | Intermediate" for i in range(30))
    parts, _ = await fake.call("plan_parts", "s", rows, PartsOut)
    assert sorted(i for p in parts.parts for i in p.ids) == sorted(
        f"L{i}" for i in range(30)
    )
    chap, _ = await fake.call("plan_chapters", "s", rows, ChaptersOut)
    assert len(chap.assignments) == 30 and chap.assignments[0].order_rank == 1
    titles, _ = await fake.call("titles", "s", rows, TitlesOut)
    assert len({t.title for t in titles.modules}) == 30


def test_fake_rows_skip_headers():
    user = (
        "COURSE: X | grade band MS | Math\n"
        "CALENDAR: 5/wk x 36 wk | 60 min\n"
        "\n"
        "Rows: id | objective\n"
        "skill | count | tiers | example\n"
        "L1 | Identify the main idea"
    )
    rows = FakeLLM()._rows(user)
    assert len(rows) == 1 and rows[0][0] == "L1"


def test_merge_los_patches_by_id():
    a = {"L1": {"id": "L1", "text": "x"}}
    b = {"L1": {"verb": "identify"}, "L2": {"id": "L2"}}
    m = merge_los(a, b)
    assert m["L1"] == {"id": "L1", "text": "x", "verb": "identify"} and "L2" in m
