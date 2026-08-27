# Course Outline Generator (Python + LangGraph) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CLI-driven LangGraph pipeline that turns a JSON list of K-12 learning objectives into a valid DCIM course outline, reliably for 10 → 1,000 objectives, on Anthropic / OpenAI / Bedrock.

**Architecture:** Seven node types — `ingest`(code) → `annotate`(LLM, parallel batches) → `plan_parts`(LLM, one compact call) → `plan_chapters`(LLM, parallel per part) → `pack_and_merge`(code, ported from existing FastAPI service) → `titles`(LLM, parallel per part) → `assemble`(code) → `validate`(code). LLMs return ID-keyed deltas only; Python owns all data and builds the final JSON. Every LLM node validates → re-asks missing ids once → deterministic fallback.

**Tech Stack:** Python 3.11+, `langgraph`, `langchain` (`init_chat_model`), `langchain-anthropic`, `langchain-openai`, `langchain-aws`, `pydantic` v2, `pyyaml`, `tenacity`, `pytest`, `pytest-asyncio`, `hypothesis`.

**Spec:** `docs/DESIGN-Course-Outline-Generator-LangGraph.md` (lean design). Background: `docs/superpowers/specs/2026-08-27-course-outline-generator-langgraph-design.md`.

## Global Constraints

- Python `>=3.11`. Package name `outline`, layout `outline/` at repo root (`C:\Users\a\Documents\Hiral\Berlin-Pearson`).
- Output JSON must match the DCIM contract in `berlin-tool-node/tool-response-43-lg-new.txt`: root keys `course_title, grade_band, subject_area, chapter_word_count_limit, total_parts, total_chapters, title, label, children, total_lesson_days, total_chapters_in_course, pacing_overrun, pacing_overrun_lesson_days, split_notes, unassigned_objective_urns`; `label` values `project|part|chapter|module`; `split_notes` is a list of strings.
- Structural constants: `MINIMUM_UNDERSTAND_CHAPTERS = 4`, `MAX_LOS_PER_CHAPTER = 4`, `MAX_PART_NAME_WORDS = 6`, `GRADE_WORD_LIMITS = {"K-2": 400, "3-5": 600, "MS": 2000, "HS": 2250}`, pacing tolerance `0.05`.
- Totals: `total_parts = 1 + content_parts + 2`; `total_chapters = 1 + content_chapters + 4*content_parts + 4`.
- Structural chapters: `chapter_estimated_word_count = null`, `chapter_estimated_time_minutes = minutes_per_lesson`.
- LLM outputs are Pydantic models via `with_structured_output`; prompts never contain URNs (short ids `L1..Ln` only).
- `temperature=0`; default `batch_size=30`, `max_concurrency=5`, `skill_mode_threshold=300`.
- No LLM node may raise on bad LLM output; it must re-ask once for missing ids, then apply the deterministic fallback and flag the LO.
- Commit after every task. Run `pytest -q` before each commit.

---

## File Structure

```
Berlin-Pearson/
├── pyproject.toml
├── config.yaml
├── outline/
│   ├── __init__.py
│   ├── __main__.py         CLI (argparse): generate
│   ├── config.py           Settings dataclass + yaml loader
│   ├── schemas.py          CourseRequest, LLM output models, DCIM output models
│   ├── state.py            LO / State TypedDicts + reducers
│   ├── llm.py              LLM (LangChain) + FakeLLM + render()
│   ├── nodes.py            all graph nodes + fan-out functions
│   ├── graph.py            build_graph()
│   ├── report.py           write report.json
│   ├── prompts/
│   │   ├── annotate.md  plan_parts.md  plan_chapters.md  titles.md
│   ├── rules/
│   │   ├── __init__.py  grade_band.py  blooms.py  estimates.py  naming.py  packing.py  merging.py  structure.py
│   ├── assemble/
│   │   ├── __init__.py  assessments.py  pacing.py  dcim.py
│   └── validate/
│       ├── __init__.py  invariants.py
├── scripts/
│   └── make_synthetic.py
└── tests/
    ├── conftest.py         fixtures: golden outline, sample inputs, parse_sse
    ├── fixtures/           sample-input-43/49/94/123.json, tool-response-43-lg-new.txt
    ├── unit/               test_schemas.py test_blooms.py test_estimates.py test_naming.py
    │                       test_packing.py test_merging.py test_structure.py test_assemble.py
    │                       test_validate.py test_llm.py test_nodes.py
    └── graph/              test_end_to_end.py test_scale.py
```

Responsibilities: `rules/` and `assemble/` and `validate/` are pure functions on dicts (no I/O, no Pydantic). `schemas.py` is the only place Pydantic lives. `nodes.py` glues state ↔ rules ↔ LLM. `graph.py` only wires.

---

### Task 0: Project scaffold, fixtures, golden parser

**Files:**
- Create: `pyproject.toml`, `config.yaml`, `outline/__init__.py`, `outline/rules/__init__.py`, `outline/assemble/__init__.py`, `outline/validate/__init__.py`, `tests/conftest.py`, `tests/unit/__init__.py`, `tests/graph/__init__.py`, `.gitignore`
- Copy: `berlin-tool-node/sample-input-43-lg.json → tests/fixtures/sample-input-43.json`, `sample-input-49-lg.json → sample-input-49.json`, `sample-input-94-lg.json → sample-input-94.json`, `sample-input-123-lgs.txt → sample-input-123.json`, `tool-response-43-lg-new.txt → tests/fixtures/tool-response-43.txt`
- Test: `tests/unit/test_fixtures.py`

**Interfaces:**
- Produces: `tests/conftest.py::parse_sse(path) -> dict`, fixtures `golden43: dict`, `input43: dict`, `input94: dict`, `input123: dict`, `fixtures_dir: Path`.

- [ ] **Step 1: Init git repo and scaffold**

```powershell
cd C:\Users\a\Documents\Hiral\Berlin-Pearson
git init
New-Item -ItemType Directory -Force outline\rules, outline\assemble, outline\validate, outline\prompts, tests\unit, tests\graph, tests\fixtures, scripts
Copy-Item berlin-tool-node\sample-input-43-lg.json tests\fixtures\sample-input-43.json
Copy-Item berlin-tool-node\sample-input-49-lg.json tests\fixtures\sample-input-49.json
Copy-Item berlin-tool-node\sample-input-94-lg.json tests\fixtures\sample-input-94.json
Copy-Item berlin-tool-node\sample-input-123-lgs.txt tests\fixtures\sample-input-123.json
Copy-Item berlin-tool-node\tool-response-43-lg-new.txt tests\fixtures\tool-response-43.txt
```

`.gitignore`:
```
__pycache__/
*.pyc
.venv/
out/
.pytest_cache/
.hypothesis/
*.egg-info/
```

`pyproject.toml`:
```toml
[project]
name = "outline"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "langgraph>=0.2.60",
  "langchain>=0.3.20",
  "langchain-core>=0.3.40",
  "langchain-anthropic>=0.3.5",
  "langchain-openai>=0.3.5",
  "langchain-aws>=0.2.10",
  "pydantic>=2.7",
  "pyyaml>=6",
  "tenacity>=8.2",
]
[project.optional-dependencies]
dev = ["pytest>=8", "pytest-asyncio>=0.23", "hypothesis>=6.100"]

[tool.setuptools]
packages = ["outline", "outline.rules", "outline.assemble", "outline.validate"]
[tool.setuptools.package-data]
outline = ["prompts/*.md"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
markers = ["live: needs real provider credentials"]
```

`config.yaml`:
```yaml
provider: anthropic            # anthropic | openai | bedrock_converse
models:
  default: claude-sonnet-4-5
  annotate: claude-haiku-4-5
  titles: claude-haiku-4-5
batch_size: 30
max_concurrency: 5
skill_mode_threshold: 300
llm_timeout_seconds: 90
transport_retries: 3
```

Empty `__init__.py` files in `outline/`, `outline/rules/`, `outline/assemble/`, `outline/validate/`, `tests/unit/`, `tests/graph/`.

- [ ] **Step 2: Install**

Run: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -e ".[dev]"`
Expected: installs without error.

- [ ] **Step 3: Write conftest with SSE parser and fixtures**

`tests/conftest.py`:
```python
import json
from pathlib import Path
import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def parse_sse(path: Path) -> dict:
    """Join the streamed `chunk` contents of a Berlin SSE log and parse the JSON payload."""
    parts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        body = line[5:].strip()
        if not body:
            continue
        try:
            d = json.loads(body)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "chunk":
            parts.append(d.get("content", ""))
    text = "".join(parts).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def load_input(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def golden43() -> dict:
    return parse_sse(FIXTURES / "tool-response-43.txt")


@pytest.fixture
def input43() -> dict:
    return load_input("sample-input-43.json")


@pytest.fixture
def input94() -> dict:
    return load_input("sample-input-94.json")


@pytest.fixture
def input123() -> dict:
    return load_input("sample-input-123.json")
```

- [ ] **Step 4: Write fixture sanity test**

`tests/unit/test_fixtures.py`:
```python
def test_golden_parses(golden43, input43):
    assert golden43["label"] == "project"
    assert golden43["total_parts"] == 10
    assert golden43["total_chapters"] == 76
    urns = [m["learning_objective_urn"] for p in golden43["children"] for c in p["children"]
            for m in c["children"] if m.get("learning_objective_urn")]
    assert len(urns) == 43 and len(set(urns)) == 43
    assert set(urns) == {lo["learning_objective_urn"] for lo in input43["learning_objectives"]}


def test_inputs_load(input94, input123):
    assert len(input94["learning_objectives"]) == 94
    assert len(input123["learning_objectives"]) == 123
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/unit/test_fixtures.py -v`
Expected: 2 PASS.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: scaffold outline package, fixtures and golden SSE parser"
```

---

### Task 1: Schemas (input, LLM outputs, DCIM output)

**Files:**
- Create: `outline/schemas.py`
- Test: `tests/unit/test_schemas.py`

**Interfaces:**
- Produces:
  - `CourseRequest` (fields below), `LearningObjectiveIn(learning_objective_urn: str, objective: str)`
  - `AnnotateItem(id, verb, primary_skill)`, `AnnotateOut(items: list[AnnotateItem])`
  - `PartItem(part_name: str, ids: list[str])`, `PartsOut(parts: list[PartItem])`
  - `ChapterItem(id, chapter_name, order_rank: int)`, `ChaptersOut(assignments: list[ChapterItem])`
  - `TitleItem(id, title)`, `TitlesOut(modules: list[TitleItem])`
  - `Outline` Pydantic model (root) with nested `Part`, `Chapter`, `Module`; `Outline.model_validate(dict)` must accept the golden output.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_schemas.py`:
```python
import pytest
from pydantic import ValidationError
from outline.schemas import CourseRequest, AnnotateOut, PartsOut, ChaptersOut, TitlesOut, Outline


def test_course_request_accepts_sample(input43):
    req = CourseRequest.model_validate(input43)
    assert req.course_outline_progression == "SKILLS_BASED_PROGRESSION"
    assert len(req.learning_objectives) == 43
    assert req.minutes_per_lesson == 60


def test_course_request_rejects_empty_los(input43):
    bad = {**input43, "learning_objectives": []}
    with pytest.raises(ValidationError):
        CourseRequest.model_validate(bad)


def test_llm_schemas_roundtrip():
    a = AnnotateOut.model_validate({"items": [{"id": "L1", "verb": "identify", "primary_skill": "Main Idea"}]})
    assert a.items[0].id == "L1"
    p = PartsOut.model_validate({"parts": [{"part_name": "Logic", "ids": ["L1", "L2"]}]})
    assert p.parts[0].ids == ["L1", "L2"]
    c = ChaptersOut.model_validate({"assignments": [{"id": "L1", "chapter_name": "Fallacies", "order_rank": 1}]})
    assert c.assignments[0].order_rank == 1
    t = TitlesOut.model_validate({"modules": [{"id": "L1", "title": "Logical Fallacy Identification"}]})
    assert t.modules[0].title.startswith("Logical")


def test_outline_accepts_golden(golden43):
    o = Outline.model_validate(golden43)
    assert o.total_parts == 10
    assert o.children[0].type == "overview"
    assert o.children[1].children[1].children[0].learning_objective_urn.startswith("urn:")
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_schemas.py -v`
Expected: FAIL with `ModuleNotFoundError: outline.schemas`.

- [ ] **Step 3: Implement schemas**

`outline/schemas.py`:
```python
"""All Pydantic contracts: input request, LLM structured outputs, DCIM output."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Progression = Literal[
    "SKILLS_BASED_PROGRESSION",
    "THEME_BASED_PROGRESSION",
    "CHRONOLOGICAL_PROGRESSION",
    "STANDARDS_DRIVEN_PROGRESSION",
]
Tier = Literal["Foundational", "Intermediate", "Advanced"]


# ---------- input ----------
class LearningObjectiveIn(BaseModel):
    learning_objective_urn: str = Field(min_length=1)
    objective: str = Field(min_length=1)


class CourseRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    course_title: str = Field(min_length=1)
    grade_band: str = Field(min_length=1)
    subject_area: str = Field(min_length=1)
    minutes_per_lesson: int = Field(gt=0)
    lessons_per_week: int = Field(gt=0, le=7)
    course_duration_weeks: int = Field(gt=0)
    course_outline_progression: Progression
    learning_objectives: list[LearningObjectiveIn] = Field(min_length=1)
    user_prompt: str | None = None


# ---------- LLM outputs (ID-keyed deltas only) ----------
class AnnotateItem(BaseModel):
    id: str
    verb: str = Field(min_length=1)
    primary_skill: str = Field(min_length=2, max_length=60)


class AnnotateOut(BaseModel):
    items: list[AnnotateItem]


class PartItem(BaseModel):
    part_name: str = Field(min_length=2, max_length=80)
    ids: list[str] = Field(min_length=1)


class PartsOut(BaseModel):
    parts: list[PartItem] = Field(min_length=1)


class ChapterItem(BaseModel):
    id: str
    chapter_name: str = Field(min_length=2, max_length=80)
    order_rank: int = Field(ge=1)


class ChaptersOut(BaseModel):
    assignments: list[ChapterItem]


class TitleItem(BaseModel):
    id: str
    title: str = Field(min_length=3, max_length=80)


class TitlesOut(BaseModel):
    modules: list[TitleItem]


# ---------- DCIM output ----------
class Title(BaseModel):
    en: str


class Module(BaseModel):
    model_config = ConfigDict(extra="allow")
    label: Literal["module"]
    type: str
    module_number: int
    title: Title
    learning_objective_urn: str | None = None
    estimated_word_count: int | None = None
    estimated_time_minutes: int | None = None
    primary_skill: str | None = None
    blooms_level: str | None = None


class Chapter(BaseModel):
    model_config = ConfigDict(extra="allow")
    label: Literal["chapter"]
    type: str
    chapter_number: int
    title: Title
    chapter_estimated_word_count: int | None = None
    chapter_estimated_time_minutes: int | None = None
    children: list[Module]


class Part(BaseModel):
    model_config = ConfigDict(extra="allow")
    label: Literal["part"]
    type: Literal["overview", "understand", "semester"]
    part_number: int
    title: Title
    children: list[Chapter]


class Outline(BaseModel):
    model_config = ConfigDict(extra="allow")
    course_title: str
    grade_band: str
    subject_area: str
    chapter_word_count_limit: int
    total_parts: int
    total_chapters: int
    title: Title
    label: Literal["project"]
    children: list[Part]
    total_lesson_days: int
    total_chapters_in_course: int
    pacing_overrun: bool
    pacing_overrun_lesson_days: int | None
    split_notes: list[str] | str | None
    unassigned_objective_urns: list[str]
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_schemas.py -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add outline/schemas.py tests/unit/test_schemas.py
git commit -m "feat: add input, LLM and DCIM pydantic schemas"
```

---

### Task 2: Rules — grade band, Bloom's lookup, estimates

**Files:**
- Create: `outline/rules/grade_band.py`, `outline/rules/blooms.py`, `outline/rules/estimates.py`
- Test: `tests/unit/test_blooms.py`, `tests/unit/test_estimates.py`

**Interfaces:**
- Produces: `grade_band.normalize(raw: str) -> str` (one of `K-2|3-5|MS|HS`); `blooms.tier_for(verb: str) -> str`; `estimates.word_limit(band) -> int`, `estimates.estimate_words(band, tier) -> int`, `estimates.estimate_minutes(tier) -> int`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_blooms.py`:
```python
from outline.rules.blooms import tier_for
from outline.rules.grade_band import normalize


def test_lowest_tier_wins_for_duplicate_verbs():
    assert tier_for("compare") == "Foundational"     # in Foundational and elsewhere
    assert tier_for("analyze") == "Intermediate"
    assert tier_for("design") == "Advanced"
    assert tier_for("Summarize") == "Foundational"   # case-insensitive; also in Advanced list
    assert tier_for("categorize") == "Intermediate"  # Intermediate and Advanced → Intermediate


def test_unknown_verb_defaults_foundational():
    assert tier_for("zork") == "Foundational"
    assert tier_for("") == "Foundational"


def test_multiword_verbs():
    assert tier_for("figure out") == "Intermediate"
    assert tier_for("set up") == "Advanced"


def test_grade_band_normalize():
    assert normalize("MS") == "MS"
    assert normalize("Grade 6") == "MS"
    assert normalize("k-2") == "K-2"
    assert normalize("Grade 4") == "3-5"
    assert normalize("9-12") == "HS"
    assert normalize("") == "3-5"
```

`tests/unit/test_estimates.py`:
```python
from outline.rules.estimates import word_limit, estimate_words, estimate_minutes


def test_minutes_by_tier():
    assert estimate_minutes("Foundational") == 14
    assert estimate_minutes("Intermediate") == 18
    assert estimate_minutes("Advanced") == 26


def test_words_ms_matches_golden():
    # golden 43-LO output: MS Foundational=291, Intermediate=475, Advanced=659
    assert estimate_words("MS", "Foundational") == 291
    assert estimate_words("MS", "Intermediate") == 475
    assert estimate_words("MS", "Advanced") == 659


def test_word_limit():
    assert word_limit("MS") == 2000
    assert word_limit("Grade 3") == 600
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_blooms.py tests/unit/test_estimates.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement**

`outline/rules/grade_band.py` (port of `_normalize_grade_band`):
```python
"""Normalise raw grade-band strings to K-2 | 3-5 | MS | HS."""


def normalize(grade_band: str | None) -> str:
    if not grade_band:
        return "3-5"
    raw = grade_band.strip().lower()
    if raw in ("k-2", "3-5", "ms", "hs"):
        return {"k-2": "K-2", "3-5": "3-5", "ms": "MS", "hs": "HS"}[raw]
    if any(k in raw for k in ["k-2", "k_2", "k2", "kindergarten", "grade 1", "grade 2", "grade1", "grade2"]):
        return "K-2"
    if any(k in raw for k in ["3-5", "3_5", "grade 3", "grade 4", "grade 5", "grade3", "grade4", "grade5", "elem"]):
        return "3-5"
    if any(k in raw for k in ["ms", "middle", "6-8", "6_8", "k6-8", "grade 6", "grade 7", "grade 8", "grade6", "grade7", "grade8"]):
        return "MS"
    if any(k in raw for k in ["hs", "high", "9-12", "9_12", "grade 9", "grade 10", "grade 11", "grade 12", "grade9", "grade10", "grade11", "grade12"]):
        return "HS"
    return "3-5"
```

`outline/rules/blooms.py` (verb lists copied verbatim from `LearningObjectiveAnalyser.md`; lowest tier wins):
```python
"""Deterministic Bloom's tier lookup: verb -> Foundational | Intermediate | Advanced."""

_FOUNDATIONAL = """add, approximate, articulate, associate, calculate, characterize, cite, clarify, classify, compare, compute, contrast, convert, defend, define, describe, detail, differentiate, discuss, distinguish, draw, duplicate, elaborate, enumerate, estimate, expand, explain, express, extend, extrapolate, factor, find, generalize, give original examples of, identify, index, indicate, infer, interact, interpolate, interpret, label, list, locate, match, name, outline, paraphrase, point, predict, quote, recall, recite, recognize, record, relate, repeat, reproduce, report, restate, rewrite, select, state, subtract, summarize, tabulate, tell, trace, translate, underline, write"""

_INTERMEDIATE = """acquire, adapt, advertise, allocate, alphabetize, analyze, apply, appraise, ascertain, assign, attain, attribute, audit, avoid, back up, blueprint, break down, capture, categorize, change, choose, confirm, construct, correlate, criticize, customize, debate, demonstrate, derive, detect, determine, diagnose, diagram, discriminate, dissect, document, dramatize, employ, examine, execute, exercise, experiment, expose, figure out, file, graph, group, handle, illustrate, implement, inspect, interconvert, investigate, inventory, layout, manage, manipulate, maximize, minimize, model, modify, operate, optimize, order, organize, perform, personalize, plot, point out, prepare, present, price, prioritize, process, produce, project, proofread, provide, query, round off, separate, sequence, show, simulate, simplify, sketch, solve, subdivide, subscribe, tabulate, test, train, transcribe, transform, use, utilize"""

_ADVANCED = """abstract, animate, appraise, argue, arrange, assemble, assess, budget, build, categorize, change, code, collect, combine, compile, compose, conclude, construct, convince, correspond, counsel, create, criticize, critique, cultivate, debate, debug, decide, depict, derive, design, develop, devise, dictate, discriminate, dispute, editorialize, enhance, evaluate, facilitate, format, formulate, generate, grade, hire, hypothesize, import, improve, incorporate, integrate, interface, invent, join, judge, justify, lecture, manage, measure, model, modify, network, organize, outline, plan, portray, predict, prepare, prescribe, produce, program, propose, rank, rate, rearrange, recommend, reconstruct, release, reorganize, revise, rewrite, score, set up, specify, support, summarize, validate, verify"""


def _split(s: str) -> list[str]:
    return [v.strip().lower() for v in s.split(",") if v.strip()]


VERB_TIER: dict[str, str] = {}
# Insert highest tier first so that lower tiers overwrite → lowest tier wins.
for _tier, _verbs in (("Advanced", _ADVANCED), ("Intermediate", _INTERMEDIATE), ("Foundational", _FOUNDATIONAL)):
    for _v in _split(_verbs):
        VERB_TIER[_v] = _tier


def tier_for(verb: str | None) -> str:
    if not verb:
        return "Foundational"
    key = " ".join(verb.strip().lower().split())
    if key in VERB_TIER:
        return VERB_TIER[key]
    first = key.split(" ")[0]
    return VERB_TIER.get(first, "Foundational")
```

`outline/rules/estimates.py` (port of `_estimate_*`):
```python
"""Word and time estimates from grade band x Bloom's tier."""
from outline.rules.grade_band import normalize

GRADE_WORD_LIMITS = {"K-2": 400, "3-5": 600, "MS": 2000, "HS": 2250}
GRADE_WORD_RANGES = {"K-2": (50, 200), "3-5": (50, 300), "MS": (200, 750), "HS": (300, 1000)}
BLOOMS_TIME_RANGES = {"Foundational": (12, 18), "Intermediate": (15, 22), "Advanced": (20, 28)}


def word_limit(grade_band: str) -> int:
    return GRADE_WORD_LIMITS[normalize(grade_band)]


def estimate_minutes(tier: str) -> int:
    low, high = BLOOMS_TIME_RANGES.get(tier, BLOOMS_TIME_RANGES["Foundational"])
    if tier == "Foundational":
        return low + 2
    if tier == "Intermediate":
        return (low + high) // 2
    return max(low, high - 2)


def estimate_words(grade_band: str, tier: str) -> int:
    low, high = GRADE_WORD_RANGES[normalize(grade_band)]
    span = high - low
    if tier == "Foundational":
        return low + max(1, span // 6)
    if tier == "Intermediate":
        return low + span // 2
    return high - max(1, span // 6)
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_blooms.py tests/unit/test_estimates.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add outline/rules tests/unit/test_blooms.py tests/unit/test_estimates.py
git commit -m "feat(rules): grade band normalisation, Bloom's verb lookup, estimates"
```

---

### Task 3: Rules — naming and packing

**Files:**
- Create: `outline/rules/naming.py`, `outline/rules/packing.py`
- Test: `tests/unit/test_naming.py`, `tests/unit/test_packing.py`

**Interfaces:**
- Produces:
  - `naming.skill_key(skill: str) -> str` (normalised key for grouping equal skills)
  - `naming.merge_part_names(a, b) -> str`, `naming.uniquify_chapter_names(chapters: list[dict]) -> list[dict]`, `naming.chapter_base_name(bucket: list[dict]) -> str`
  - `packing.pack_chapters(los: list[dict], word_limit: int, minute_limit: int) -> list[dict]` where each input LO dict has `estimated_word_count, estimated_time_minutes, source_chapter_name, primary_skill` and each output chapter is `{"chapter_name", "chapter_estimated_word_count", "chapter_estimated_time_minutes", "learning_objectives": [lo dicts with "module_number"]}`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_naming.py`:
```python
from outline.rules.naming import skill_key, merge_part_names, uniquify_chapter_names


def test_skill_key_normalises():
    assert skill_key("Rules Of Inference") == skill_key("inference rules")
    assert skill_key("Logical Fallacies") == skill_key("logical fallacy")
    assert skill_key("Main Idea") != skill_key("Key Details")


def test_merge_part_names():
    assert merge_part_names("Logic", "Logic") == "Logic"
    assert merge_part_names("Logic and Proof", "Proof") == "Logic and Proof"
    assert merge_part_names("Basic Skills", "Advanced Skills") == "Basic Skills & Advanced Skills"
    assert len(merge_part_names("Cultural Context in Art", "Arts Analysis and Response").split()) <= 6


def test_uniquify_uses_skill_differentiator():
    chapters = [
        {"chapter_name": "Fractions", "learning_objectives": [{"primary_skill": "Fraction Addition"}]},
        {"chapter_name": "Fractions", "learning_objectives": [{"primary_skill": "Fraction Denominators"}]},
        {"chapter_name": "Decimals", "learning_objectives": [{"primary_skill": "Decimals"}]},
    ]
    out = uniquify_chapter_names(chapters)
    names = [c["chapter_name"] for c in out]
    assert names[0] == "Fractions"
    assert names[1].startswith("Fractions - ") and "Denominators" in names[1]
    assert len(set(names)) == 3
```

`tests/unit/test_packing.py`:
```python
from outline.rules.packing import pack_chapters


def lo(words, mins, chap="C", skill="S"):
    return {"estimated_word_count": words, "estimated_time_minutes": mins,
            "source_chapter_name": chap, "primary_skill": skill, "urn": f"u{words}{mins}"}


def test_splits_on_time_limit():
    chapters = pack_chapters([lo(100, 30), lo(100, 30), lo(100, 30)], word_limit=2000, minute_limit=60)
    assert [len(c["learning_objectives"]) for c in chapters] == [2, 1]
    assert chapters[0]["chapter_estimated_time_minutes"] == 60


def test_splits_on_density_4():
    chapters = pack_chapters([lo(10, 1) for _ in range(9)], word_limit=2000, minute_limit=60)
    assert [len(c["learning_objectives"]) for c in chapters] == [4, 4, 1]


def test_module_numbers_reset_per_chapter():
    chapters = pack_chapters([lo(10, 1) for _ in range(5)], word_limit=2000, minute_limit=60)
    assert [m["module_number"] for m in chapters[0]["learning_objectives"]] == [1, 2, 3, 4]
    assert chapters[1]["learning_objectives"][0]["module_number"] == 1


def test_chapter_name_from_sources():
    chapters = pack_chapters([lo(10, 1, "A"), lo(10, 1, "B")], word_limit=2000, minute_limit=60)
    assert chapters[0]["chapter_name"] == "A and B"
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_naming.py tests/unit/test_packing.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement**

`outline/rules/naming.py`:
```python
"""Deterministic naming helpers (ported from course_outline_structure_service.py)."""
import re
from collections import OrderedDict

MAX_PART_NAME_WORDS = 6
STOP_WORDS = {
    "a", "an", "the", "of", "in", "for", "to", "by", "on", "with", "from", "that", "this", "their",
    "its", "and", "or", "is", "are", "be", "been", "being", "was", "were", "will", "can", "could",
    "should", "would", "may", "might", "has", "have", "had", "do", "does", "did", "using", "use",
    "related", "concept", "concepts",
}
_CONJ = {"and", "or", "the", "of", "in", "for", "to", "a"}


def _singular(w: str) -> str:
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 3 and w.endswith("es") and not w.endswith("ses"):
        return w[:-2] if w[:-2].endswith(("sh", "ch", "x")) else w[:-1]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def skill_key(skill: str) -> str:
    words = re.findall(r"[a-z0-9]+", (skill or "").lower())
    words = [_singular(w) for w in words if w not in STOP_WORDS]
    return " ".join(sorted(words)) or (skill or "").strip().lower()


def chapter_base_name(bucket: list[dict]) -> str:
    names = list(OrderedDict.fromkeys(lo["source_chapter_name"] for lo in bucket))
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} and Related Concepts"


def merge_part_names(first: str, second: str) -> str:
    if first == second:
        return first
    if second.lower() in first.lower():
        return first
    if first.lower() in second.lower():
        return second
    wa, wb = first.split(), second.split()
    while wa and wa[-1].lower() in _CONJ:
        wa.pop()
    while wb and wb[-1].lower() in _CONJ:
        wb.pop()
    combined = f"{' '.join(wa)} & {' '.join(wb)}"
    if len(combined.split()) <= MAX_PART_NAME_WORDS:
        return combined
    sa = " ".join([w for w in wa if w.lower() not in _CONJ][:2])
    sb = " ".join([w for w in wb if w.lower() not in _CONJ][:2])
    return f"{sa} & {sb}"


def _differentiator(chapter_los: list[dict], base_name: str) -> str:
    base = {w.lower() for w in base_name.split()}
    novel: list[str] = []
    for lo in chapter_los:
        for word in (lo.get("primary_skill") or "").split():
            clean = word.strip(".,;:()")
            if clean.lower() not in base and clean.lower() not in STOP_WORDS and clean.title() not in novel:
                novel.append(clean.title())
    return " ".join(novel[:2])


def uniquify_chapter_names(chapters: list[dict]) -> list[dict]:
    counts: dict[str, int] = {}
    for c in chapters:
        counts[c["chapter_name"]] = counts.get(c["chapter_name"], 0) + 1
    seen: dict[str, int] = {}
    used: set[str] = set()
    for c in chapters:
        name = c["chapter_name"]
        if counts[name] <= 1:
            used.add(name)
            continue
        occ = seen.get(name, 0) + 1
        seen[name] = occ
        if occ == 1:
            used.add(name)
            continue
        diff = _differentiator(c.get("learning_objectives", []), name)
        new = f"{name} - {diff}" if diff else f"{name} ({occ})"
        if new in used:
            new = f"{name} ({occ})"
        c["chapter_name"] = new
        used.add(new)
    return chapters
```

`outline/rules/packing.py`:
```python
"""Bin-pack ordered LOs into lesson-sized understand chapters."""
import copy

from outline.rules.naming import chapter_base_name, uniquify_chapter_names

MAX_LOS_PER_CHAPTER = 4


def _close(bucket: list[dict], words: int, mins: int) -> dict:
    los = copy.deepcopy(bucket)
    for i, lo in enumerate(los, start=1):
        lo["module_number"] = i
    return {
        "chapter_name": chapter_base_name(bucket),
        "chapter_estimated_word_count": words,
        "chapter_estimated_time_minutes": mins,
        "learning_objectives": los,
    }


def pack_chapters(los: list[dict], word_limit: int, minute_limit: int) -> list[dict]:
    chapters: list[dict] = []
    bucket: list[dict] = []
    words = mins = 0
    for lo in los:
        over_words = words + lo["estimated_word_count"] > word_limit
        over_time = mins + lo["estimated_time_minutes"] > minute_limit
        over_density = len(bucket) >= MAX_LOS_PER_CHAPTER
        if bucket and (over_words or over_time or over_density):
            chapters.append(_close(bucket, words, mins))
            bucket, words, mins = [], 0, 0
        bucket.append(lo)
        words += lo["estimated_word_count"]
        mins += lo["estimated_time_minutes"]
    if bucket:
        chapters.append(_close(bucket, words, mins))
    return uniquify_chapter_names(chapters)
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_naming.py tests/unit/test_packing.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add outline/rules/naming.py outline/rules/packing.py tests/unit/test_naming.py tests/unit/test_packing.py
git commit -m "feat(rules): naming helpers and chapter bin-packing"
```

---

### Task 4: Rules — minimum-4 merging

**Files:**
- Create: `outline/rules/merging.py`
- Test: `tests/unit/test_merging.py`

**Interfaces:**
- Produces: `merging.enforce_min_4(parts: list[dict]) -> tuple[list[dict], list[str]]`; input/output part = `{"part_name": str, "chapters": list[dict]}`; returns `(parts, log_lines)`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_merging.py`:
```python
from outline.rules.merging import enforce_min_4


def part(name, n):
    return {"part_name": name, "chapters": [{"chapter_name": f"{name} {i}", "learning_objectives": [{"urn": f"{name}-{i}"}]} for i in range(n)]}


def counts(parts):
    return [len(p["chapters"]) for p in parts]


def test_matrix_1_multiple_merges():
    parts, log = enforce_min_4([part("A", 3), part("B", 3), part("C", 3), part("D", 3), part("E", 4)])
    assert counts(parts) == [6, 6, 4]
    assert any(l.startswith("MERGE") for l in log)


def test_matrix_2_single_merge_large_course():
    parts, _ = enforce_min_4([part(n, c) for n, c in zip("ABCDEFGH", [4, 5, 3, 4, 6, 4, 5, 4])])
    assert counts(parts) == [4, 5, 7, 6, 4, 5, 4]


def test_matrix_3_noop_when_valid():
    parts, log = enforce_min_4([part(n, 4) for n in "ABCDEF"])
    assert counts(parts) == [4] * 6
    assert all(l.startswith("FINAL") for l in log)


def test_matrix_4_two_part_exception():
    parts, log = enforce_min_4([part("A", 1), part("B", 2)])
    assert counts(parts) == [1, 2]
    assert any(l.startswith("EXCEPTION") for l in log)


def test_matrix_5_two_parts_merge_when_combined_ge_4():
    parts, _ = enforce_min_4([part("A", 2), part("B", 2)])
    assert counts(parts) == [4]


def test_matrix_6_best_adjacent_is_smallest():
    parts, _ = enforce_min_4([part("A", 2), part("B", 2), part("C", 8)])
    assert counts(parts) == [4, 8]


def test_urns_preserved_and_order_kept():
    src = [part("A", 3), part("B", 5)]
    parts, _ = enforce_min_4(src)
    urns = [lo["urn"] for p in parts for c in p["chapters"] for lo in c["learning_objectives"]]
    assert urns == [f"A-{i}" for i in range(3)] + [f"B-{i}" for i in range(5)]
    assert parts[0]["part_name"] == "A & B"
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_merging.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement**

`outline/rules/merging.py` (port of `_enforce_minimum_4`, `_get_best_adjacent`, `_merge_parts`):
```python
"""Merge undersized parts until every part has >= 4 understand chapters (or the 2-part exception)."""
import copy

from outline.rules.naming import merge_part_names, uniquify_chapter_names

MINIMUM_UNDERSTAND_CHAPTERS = 4


def _best_adjacent(parts: list[dict], index: int) -> int | None:
    cands: list[tuple[int, int]] = []
    if index > 0:
        cands.append((index - 1, len(parts[index - 1]["chapters"])))
    if index < len(parts) - 1:
        cands.append((index + 1, len(parts[index + 1]["chapters"])))
    if not cands:
        return None
    cands.sort(key=lambda c: (c[1], -c[0]))
    return cands[0][0]


def _merge(parts: list[dict], src: int, dst: int) -> list[dict]:
    first, second = sorted([src, dst])
    a, b = parts[first], parts[second]
    merged = {
        "part_name": merge_part_names(a["part_name"], b["part_name"]),
        "chapters": uniquify_chapter_names(copy.deepcopy(a["chapters"]) + copy.deepcopy(b["chapters"])),
    }
    return [merged if i == first else copy.deepcopy(p) for i, p in enumerate(parts) if i != second]


def enforce_min_4(parts: list[dict]) -> tuple[list[dict], list[str]]:
    log: list[str] = []
    parts = copy.deepcopy(parts)
    changed = True
    while changed:
        changed = False
        for i, p in enumerate(parts):
            n = len(p["chapters"])
            if n >= MINIMUM_UNDERSTAND_CHAPTERS:
                continue
            adj = _best_adjacent(parts, i)
            if adj is None:
                log.append(f"WARNING: Part '{p['part_name']}' has {n} chapters and no adjacent part.")
                continue
            if len(parts) == 2 and n + len(parts[adj]["chapters"]) < MINIMUM_UNDERSTAND_CHAPTERS:
                log.append(
                    f"EXCEPTION: Part '{p['part_name']}' has {n} chapters; combined pair would still have "
                    f"{n + len(parts[adj]['chapters'])} chapters (< 4). Accepted as-is."
                )
                continue
            log.append(
                f"MERGE: Part '{p['part_name']}' ({n} chapters) merged with '{parts[adj]['part_name']}' "
                f"({len(parts[adj]['chapters'])} chapters)"
            )
            parts = _merge(parts, i, adj)
            m = min(i, adj)
            log.append(f"RESULT: Part '{parts[m]['part_name']}' now has {len(parts[m]['chapters'])} chapters")
            changed = True
            break
    for p in parts:
        n = len(p["chapters"])
        log.append(f"FINAL: Part '{p['part_name']}' - {n} understand chapters {'OK' if n >= 4 else 'WARNING'}")
    return parts, log
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_merging.py -v`
Expected: 7 PASS. (Test 4: exception loop — `A`(1) checks adj `B`: combined 3 < 4 → exception; `B`(2) checks adj `A`: combined 3 → exception; loop ends.)

- [ ] **Step 5: Commit**

```bash
git add outline/rules/merging.py tests/unit/test_merging.py
git commit -m "feat(rules): minimum-4 part merging with 2-part exception"
```

---

### Task 5: Rules — full structure build (`pack_and_merge` core)

**Files:**
- Create: `outline/rules/structure.py`
- Test: `tests/unit/test_structure.py`

**Interfaces:**
- Consumes: `estimates`, `packing.pack_chapters`, `merging.enforce_min_4`.
- Produces: `structure.build_structure(course: dict, budget: dict, los: dict[str, dict], parts: list[dict]) -> dict`.
  - `course`: `{"grade_band": str, "minutes_per_lesson": int, ...}`; `budget`: `{"word_limit": int, "total_lesson_days": int}`.
  - `los[id]`: `{"id","urn","text","idx","primary_skill","tier","chapter","rank"}`.
  - `parts`: `[{"part_name": str, "ids": [id...]}]` in order.
  - Returns `packed = {"parts": [...], "enforcement_log": str, "validation": {...}, "content_chapter_count": int, "num_content_parts": int, "total_chapter_count": int}` with each part `{"part_name","part_number"(from 2),"understand_chapter_count","chapters":[{"chapter_name","chapter_number"(from 2),"chapter_type":"understand","chapter_estimated_word_count","chapter_estimated_time_minutes","learning_objectives":[{"id","urn","module_number","lo_text","primary_skill","blooms_level","source_chapter_name","estimated_word_count","estimated_time_minutes"}]}]}`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_structure.py`:
```python
from hypothesis import given, settings, strategies as st

from outline.rules.structure import build_structure

COURSE = {"grade_band": "MS", "minutes_per_lesson": 60}
BUDGET = {"word_limit": 2000, "total_lesson_days": 180}


def make_los(n, chapter_of=lambda i: f"Ch{i // 3}", tier_of=lambda i: "Intermediate"):
    return {
        f"L{i}": {"id": f"L{i}", "urn": f"urn:{i}", "text": f"Objective {i}", "idx": i,
                  "primary_skill": f"Skill {i // 3}", "tier": tier_of(i), "chapter": chapter_of(i), "rank": i // 3 + 1}
        for i in range(n)
    }


def all_urns(packed):
    return [lo["urn"] for p in packed["parts"] for c in p["chapters"] for lo in c["learning_objectives"]]


def test_basic_shape_and_numbering():
    los = make_los(24)
    parts = [{"part_name": "Unit A", "ids": [f"L{i}" for i in range(12)]},
             {"part_name": "Unit B", "ids": [f"L{i}" for i in range(12, 24)]}]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert [p["part_number"] for p in packed["parts"]] == [2, 3]
    assert packed["parts"][0]["chapters"][0]["chapter_number"] == 2
    assert packed["parts"][0]["chapters"][0]["chapter_type"] == "understand"
    assert packed["num_content_parts"] == 2
    assert packed["content_chapter_count"] == sum(len(p["chapters"]) for p in packed["parts"])
    assert packed["total_chapter_count"] == 1 + packed["content_chapter_count"] + 4 * 2 + 4
    assert packed["validation"]["valid"] is True
    assert packed["validation"]["total_placed_los"] == 24
    lo = packed["parts"][0]["chapters"][0]["learning_objectives"][0]
    assert lo["estimated_word_count"] == 475 and lo["estimated_time_minutes"] == 18
    assert lo["lo_text"] == "Objective 0" and lo["blooms_level"] == "Intermediate"


def test_undersized_part_is_merged():
    los = make_los(15)
    parts = [{"part_name": "Small", "ids": ["L0", "L1", "L2"]},
             {"part_name": "Big", "ids": [f"L{i}" for i in range(3, 15)]}]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert packed["num_content_parts"] == 1
    assert "MERGE" in packed["enforcement_log"]


def test_rank_orders_chapters_within_part():
    los = make_los(6, chapter_of=lambda i: "Early" if i >= 3 else "Late")
    for i in range(6):
        los[f"L{i}"]["rank"] = 1 if i >= 3 else 2
    packed = build_structure(COURSE, BUDGET, los, [{"part_name": "P", "ids": [f"L{i}" for i in range(6)]}])
    assert packed["parts"][0]["chapters"][0]["chapter_name"] == "Early"


@settings(max_examples=40, deadline=None)
@given(n=st.integers(1, 120), seed=st.integers(0, 10_000))
def test_property_urns_preserved_and_limits(n, seed):
    import random
    rnd = random.Random(seed)
    tiers = ["Foundational", "Intermediate", "Advanced"]
    los = make_los(n, chapter_of=lambda i: f"Ch{rnd.randint(0, max(1, n // 4))}", tier_of=lambda i: rnd.choice(tiers))
    ids = list(los)
    k = max(1, n // rnd.randint(3, 12))
    parts = [{"part_name": f"Unit {j}", "ids": ids[j * k:(j + 1) * k]} for j in range((n + k - 1) // k)]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert sorted(all_urns(packed)) == sorted(lo["urn"] for lo in los.values())
    for p in packed["parts"]:
        for c in p["chapters"]:
            assert c["chapter_estimated_time_minutes"] <= 60
            assert c["chapter_estimated_word_count"] <= 2000
            assert 1 <= len(c["learning_objectives"]) <= 4
    sizes = [len(p["chapters"]) for p in packed["parts"]]
    assert all(s >= 4 for s in sizes) or (len(sizes) <= 2 and sum(sizes) < 4)
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_structure.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement**

`outline/rules/structure.py`:
```python
"""Deterministic structure: estimates -> pack -> merge -> number -> validate."""
from collections import Counter

from outline.rules.estimates import estimate_minutes, estimate_words
from outline.rules.merging import MINIMUM_UNDERSTAND_CHAPTERS, enforce_min_4
from outline.rules.packing import pack_chapters


def _stub(lo: dict, grade_band: str) -> dict:
    return {
        "id": lo["id"],
        "urn": lo["urn"],
        "lo_text": lo["text"],
        "primary_skill": lo.get("primary_skill") or "General",
        "blooms_level": lo.get("tier") or "Foundational",
        "source_chapter_name": lo.get("chapter") or (lo.get("primary_skill") or "General"),
        "estimated_word_count": estimate_words(grade_band, lo.get("tier") or "Foundational"),
        "estimated_time_minutes": estimate_minutes(lo.get("tier") or "Foundational"),
    }


def _initial_parts(course: dict, budget: dict, los: dict[str, dict], parts: list[dict]) -> list[dict]:
    out: list[dict] = []
    for part in parts:
        ordered = sorted(
            (los[i] for i in part["ids"] if i in los),
            key=lambda lo: (lo.get("rank") or 10**6, lo.get("chapter") or "", lo["idx"]),
        )
        chapters: list[dict] = []
        bucket: list[dict] = []
        current: tuple | None = None
        for lo in ordered:
            key = (lo.get("chapter"), lo.get("rank"))
            if current is not None and key != current and bucket:
                chapters.extend(pack_chapters(bucket, budget["word_limit"], course["minutes_per_lesson"]))
                bucket = []
            current = key
            bucket.append(_stub(lo, course["grade_band"]))
        if bucket:
            chapters.extend(pack_chapters(bucket, budget["word_limit"], course["minutes_per_lesson"]))
        if chapters:
            out.append({"part_name": part["part_name"], "chapters": chapters})
    return out


def _number(parts: list[dict]) -> list[dict]:
    for pi, p in enumerate(parts, start=2):
        p["part_number"] = pi
        p["understand_chapter_count"] = len(p["chapters"])
        for ci, c in enumerate(p["chapters"], start=2):
            c["chapter_number"] = ci
            c["chapter_type"] = "understand"
            for mi, lo in enumerate(c["learning_objectives"], start=1):
                lo["module_number"] = mi
    return parts


def _validate(input_urns: list[str], parts: list[dict]) -> dict:
    placed = [lo["urn"] for p in parts for c in p["chapters"] for lo in c["learning_objectives"]]
    in_counts, out_counts = Counter(input_urns), Counter(placed)
    known_dupes = {u for u, n in in_counts.items() if n > 1}
    missing = sorted(set(input_urns) - set(placed))
    extra = sorted(set(placed) - set(input_urns))
    dupes = sorted(u for u, n in out_counts.items() if n > 1 and u not in known_dupes)
    return {
        "total_input_los": len(input_urns),
        "total_placed_los": len(placed),
        "all_parts_gte_4_chapters": all(len(p["chapters"]) >= MINIMUM_UNDERSTAND_CHAPTERS for p in parts),
        "duplicate_urns": dupes,
        "missing_urns": missing,
        "extra_urns": extra,
        "valid": not dupes and not missing and not extra,
    }


def build_structure(course: dict, budget: dict, los: dict[str, dict], parts: list[dict]) -> dict:
    initial = _initial_parts(course, budget, los, parts)
    merged, log = enforce_min_4(initial)
    numbered = _number(merged)
    validation = _validate([lo["urn"] for lo in los.values()], numbered)
    content_chapters = sum(len(p["chapters"]) for p in numbered)
    n_parts = len(numbered)
    return {
        "parts": numbered,
        "enforcement_log": "\n".join(log),
        "validation": validation,
        "content_chapter_count": content_chapters,
        "num_content_parts": n_parts,
        "total_chapter_count": 1 + content_chapters + n_parts * 4 + 4,
    }
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_structure.py -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add outline/rules/structure.py tests/unit/test_structure.py
git commit -m "feat(rules): deterministic structure build (pack, merge, number, validate)"
```

---

### Task 6: Assemble — DCIM JSON, assessments, pacing (golden round-trip)

**Files:**
- Create: `outline/assemble/assessments.py`, `outline/assemble/pacing.py`, `outline/assemble/dcim.py`
- Test: `tests/unit/test_assemble.py`

**Interfaces:**
- Consumes: `packed` from Task 5; `titles: dict[str, str]` keyed by LO `id`.
- Produces:
  - `assessments.for_chapter_type(t: str) -> dict | None`
  - `pacing.pacing_fields(total_chapters: int, total_lesson_days: int, tolerance=0.05) -> dict` with keys `pacing_overrun, pacing_overrun_lesson_days, split_notes(list[str])`
  - `dcim.build(course: dict, budget: dict, packed: dict, titles: dict[str, str]) -> dict` (the outline). `course` keys: `course_title, grade_band, subject_area, minutes_per_lesson`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_assemble.py`:
```python
import copy
from outline.assemble.dcim import build
from outline.assemble.pacing import pacing_fields
from outline.assemble.assessments import for_chapter_type


def packed_from_golden(golden: dict) -> tuple[dict, dict]:
    """Rebuild `packed` + `titles` from the golden outline so assemble can be round-tripped."""
    parts, titles = [], {}
    for p in golden["children"]:
        if p["type"] != "understand":
            continue
        chapters = []
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            los = []
            for m in c["children"]:
                lo_id = m["learning_objective_urn"]
                titles[lo_id] = m["title"]["en"]
                los.append({"id": lo_id, "urn": lo_id, "module_number": m["module_number"], "lo_text": "",
                            "primary_skill": m["primary_skill"], "blooms_level": m["blooms_level"],
                            "source_chapter_name": c["title"]["en"],
                            "estimated_word_count": m["estimated_word_count"],
                            "estimated_time_minutes": m["estimated_time_minutes"]})
            chapters.append({"chapter_name": c["title"]["en"], "chapter_number": c["chapter_number"],
                             "chapter_type": "understand",
                             "chapter_estimated_word_count": c["chapter_estimated_word_count"],
                             "chapter_estimated_time_minutes": c["chapter_estimated_time_minutes"],
                             "learning_objectives": los})
        parts.append({"part_name": p["title"]["en"], "part_number": p["part_number"],
                      "understand_chapter_count": len(chapters), "chapters": chapters})
    n_ch = sum(len(p["chapters"]) for p in parts)
    packed = {"parts": parts, "enforcement_log": "", "validation": {"valid": True},
              "content_chapter_count": n_ch, "num_content_parts": len(parts),
              "total_chapter_count": 1 + n_ch + 4 * len(parts) + 4}
    return packed, titles


def strip(o: dict) -> dict:
    o = copy.deepcopy(o)
    o.pop("split_notes", None)
    for p in o["children"]:
        for c in p["children"]:
            c.pop("assessment", None)
    return o


def test_assemble_reproduces_golden(golden43, input43):
    packed, titles = packed_from_golden(golden43)
    course = {k: input43[k] for k in ("course_title", "grade_band", "subject_area", "minutes_per_lesson")}
    budget = {"word_limit": 2000, "total_lesson_days": 180}
    out = build(course, budget, packed, titles)
    assert strip(out) == strip(golden43)
    assert isinstance(out["split_notes"], list) and out["split_notes"]


def test_pacing_overrun():
    f = pacing_fields(total_chapters=200, total_lesson_days=180)
    assert f["pacing_overrun"] is True and f["pacing_overrun_lesson_days"] == 20
    ok = pacing_fields(total_chapters=76, total_lesson_days=180)
    assert ok["pacing_overrun"] is False and ok["pacing_overrun_lesson_days"] is None


def test_assessment_mapping():
    assert for_chapter_type("understand")["type"] == "Quick Check"
    assert for_chapter_type("test")["type"] == "Unit Test"
    assert for_chapter_type("semester_exam")["type"] == "Semester Exam"
    assert for_chapter_type("introduction") is None
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_assemble.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement**

`outline/assemble/assessments.py` (requirements.md §3):
```python
"""Default assessment per DCIM chapter type."""
_TABLE = {
    "understand": {"type": "Quick Check", "scoring": "auto", "delivery": "multiple_choice"},
    "apply": {"type": "Sample Work", "scoring": "teacher", "delivery": "dropbox"},
    "review": {"type": "Unit Online Practice", "scoring": "auto", "delivery": "multiple_choice"},
    "test": {"type": "Unit Test", "scoring": "auto_and_teacher", "delivery": "test"},
    "semester_review": {"type": "Semester Online Practice", "scoring": "auto", "delivery": "multiple_choice"},
    "semester_exam": {"type": "Semester Exam", "scoring": "auto", "delivery": "exam"},
}


def for_chapter_type(chapter_type: str) -> dict | None:
    return dict(_TABLE[chapter_type]) if chapter_type in _TABLE else None
```

`outline/assemble/pacing.py`:
```python
"""Lesson-day pacing check (+/- tolerance)."""


def pacing_fields(total_chapters: int, total_lesson_days: int, tolerance: float = 0.05) -> dict:
    tol = round(total_lesson_days * tolerance)
    lower, upper = total_lesson_days - tol, total_lesson_days + tol
    if total_chapters > upper:
        return {
            "pacing_overrun": True,
            "pacing_overrun_lesson_days": total_chapters - total_lesson_days,
            "split_notes": [f"Pacing overrun: total_chapters_in_course={total_chapters} exceeds "
                            f"total_lesson_days={total_lesson_days} (+{tol} tolerance)."],
        }
    if total_chapters < lower:
        note = (f"Pacing check: total_chapters_in_course={total_chapters} is under the lesson-day target "
                f"(total_lesson_days={total_lesson_days}) within 5% tolerance ({lower}-{upper}). Course is under-filled.")
    else:
        note = f"Pacing check passed: total_chapters_in_course={total_chapters} within {lower}-{upper}."
    return {"pacing_overrun": False, "pacing_overrun_lesson_days": None, "split_notes": [note]}
```

`outline/assemble/dcim.py`:
```python
"""Build the DCIM course outline JSON from packed structure + titles. Pure, deterministic."""
from outline.assemble.assessments import for_chapter_type
from outline.assemble.pacing import pacing_fields


def _module(mtype: str, number: int, title: str, urn=None, words=None, mins=None, skill=None, tier=None) -> dict:
    return {
        "label": "module", "type": mtype, "module_number": number, "title": {"en": title},
        "learning_objective_urn": urn, "estimated_word_count": words, "estimated_time_minutes": mins,
        "primary_skill": skill, "blooms_level": tier,
    }


def _chapter(ctype: str, number: int, title: str, words, mins: int, children: list[dict]) -> dict:
    ch = {
        "label": "chapter", "type": ctype, "chapter_number": number, "title": {"en": title},
        "chapter_estimated_word_count": words, "chapter_estimated_time_minutes": mins, "children": children,
    }
    assessment = for_chapter_type(ctype)
    if assessment is not None:
        ch["assessment"] = assessment
    return ch


def _part(ptype: str, number: int, title: str, chapters: list[dict]) -> dict:
    return {"label": "part", "type": ptype, "part_number": number, "title": {"en": title}, "children": chapters}


def _overview(course: dict, mpl: int) -> dict:
    t = course["course_title"]
    return _part("overview", 1, f"{t} Course Overview", [
        _chapter("overview", 1, f"{t} Course Overview", None, mpl, [
            _module("course_guide", 1, "Course Guide"),
            _module("overview_introduction", 2, "Course Introduction"),
        ])
    ])


def _content_part(p: dict, titles: dict[str, str], mpl: int) -> dict:
    name = p["part_name"]
    chapters = [_chapter("introduction", 1, f"{name} Introduction", None, mpl,
                         [_module("introduction", 1, f"{name} Introduction")])]
    n = 1
    for c in p["chapters"]:
        n += 1
        mods = [
            _module("understand", lo["module_number"], titles.get(lo["id"], lo.get("lo_text") or lo["urn"]),
                    urn=lo["urn"], words=lo["estimated_word_count"], mins=lo["estimated_time_minutes"],
                    skill=lo["primary_skill"], tier=lo["blooms_level"])
            for lo in c["learning_objectives"]
        ]
        chapters.append(_chapter("understand", n, c["chapter_name"], c["chapter_estimated_word_count"],
                                 c["chapter_estimated_time_minutes"], mods))
    chapters.append(_chapter("apply", n + 1, f"{name} Apply", None, mpl, [_module("apply", 1, "Apply")]))
    chapters.append(_chapter("review", n + 2, f"{name} Review", None, mpl, [_module("review", 1, "Review")]))
    chapters.append(_chapter("test", n + 3, f"{name} Part Test", None, mpl, []))
    return _part("understand", p["part_number"], name, chapters)


def _semester(course: dict, letter: str, number: int, mpl: int) -> dict:
    t = course["course_title"]
    return _part("semester", number, f"{t} Semester {letter} Reflect & Review", [
        _chapter("semester_review", 1, f"Semester {letter} Review", None, mpl,
                 [_module("semester_review", 1, f"Semester {letter} Review & Reflect")]),
        _chapter("semester_exam", 2, f"Semester {letter} Exam", None, mpl, []),
    ])


def build(course: dict, budget: dict, packed: dict, titles: dict[str, str]) -> dict:
    mpl = course["minutes_per_lesson"]
    parts = [_overview(course, mpl)]
    parts += [_content_part(p, titles, mpl) for p in packed["parts"]]
    n_content = len(packed["parts"])
    parts.append(_semester(course, "A", n_content + 2, mpl))
    parts.append(_semester(course, "B", n_content + 3, mpl))
    total_chapters = sum(len(p["children"]) for p in parts)
    pacing = pacing_fields(total_chapters, budget["total_lesson_days"])
    return {
        "course_title": course["course_title"],
        "grade_band": course["grade_band"],
        "subject_area": course["subject_area"],
        "chapter_word_count_limit": budget["word_limit"],
        "total_parts": len(parts),
        "total_chapters": total_chapters,
        "title": {"en": course["course_title"]},
        "label": "project",
        "children": parts,
        "total_lesson_days": budget["total_lesson_days"],
        "total_chapters_in_course": total_chapters,
        **pacing,
        "unassigned_objective_urns": [],
    }
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_assemble.py -v`
Expected: 3 PASS. If `test_assemble_reproduces_golden` fails, print the first differing path with a small helper — do **not** loosen the comparison; the golden is the contract.

- [ ] **Step 5: Commit**

```bash
git add outline/assemble tests/unit/test_assemble.py
git commit -m "feat(assemble): DCIM builder reproduces golden 43-LO output"
```

---

### Task 7: Validate — final invariants

**Files:**
- Create: `outline/validate/invariants.py`
- Test: `tests/unit/test_validate.py`

**Interfaces:**
- Produces: `invariants.check(outline: dict, input_urns: list[str]) -> list[str]` (empty list = valid). Failure codes as string prefixes: `LO_COVERAGE`, `MIN4`, `SEMESTERS`, `ORDER`, `SUMS`, `TITLES`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_validate.py`:
```python
import copy
from outline.validate.invariants import check


def urns_of(inp):
    return [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]


def test_golden_is_valid(golden43, input43):
    assert check(golden43, urns_of(input43)) == []


def test_detects_missing_and_duplicate_urn(golden43, input43):
    bad = copy.deepcopy(golden43)
    mod = bad["children"][1]["children"][1]["children"][0]
    mod["learning_objective_urn"] = bad["children"][1]["children"][2]["children"][0]["learning_objective_urn"]
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("LO_COVERAGE") for e in errs)


def test_detects_min4_violation(golden43, input43):
    bad = copy.deepcopy(golden43)
    part = bad["children"][1]
    part["children"] = [c for c in part["children"] if c["type"] != "understand"][:1] + \
                       [c for c in part["children"] if c["type"] == "understand"][:3] + \
                       [c for c in part["children"] if c["type"] in ("apply", "review", "test")]
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("MIN4") for e in errs)


def test_detects_duplicate_titles_and_bad_sums(golden43, input43):
    bad = copy.deepcopy(golden43)
    ch = bad["children"][1]["children"][1]
    ch["chapter_estimated_word_count"] = 1
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("SUMS") for e in errs)
    bad2 = copy.deepcopy(golden43)
    for p in bad2["children"]:
        for c in p["children"]:
            if c["type"] == "understand" and len(c["children"]) >= 1:
                c["children"][0]["title"]["en"] = c["title"]["en"]
                break
    assert any(e.startswith("TITLES") for e in check(bad2, urns_of(input43)))
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_validate.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement**

`outline/validate/invariants.py`:
```python
"""Final invariants over the assembled outline. Returns a list of failure strings (empty = valid)."""
import re
from collections import Counter

BANNED = re.compile(r"(?i)\b(continued|part\s*(2|3|ii|iii)|module\s*\d+|activity|practice)\b")


def check(outline: dict, input_urns: list[str]) -> list[str]:
    errs: list[str] = []
    parts = outline["children"]
    content = [p for p in parts if p["type"] == "understand"]

    placed = [m["learning_objective_urn"] for p in parts for c in p["children"] for m in c["children"]
              if m.get("learning_objective_urn")]
    if Counter(placed) != Counter(input_urns):
        missing = sorted(set(input_urns) - set(placed))
        extra = sorted(set(placed) - set(input_urns))
        dup = sorted(u for u, n in Counter(placed).items() if n > Counter(input_urns)[u])
        errs.append(f"LO_COVERAGE missing={missing[:5]} extra={extra[:5]} duplicate={dup[:5]}")

    for p in content:
        n = sum(1 for c in p["children"] if c["type"] == "understand")
        if n < 4 and not (len(content) <= 2 and sum(
                sum(1 for c in q["children"] if c["type"] == "understand") for q in content) < 4):
            errs.append(f"MIN4 part '{p['title']['en']}' has {n} understand chapters")

    if [p["type"] for p in parts[-2:]] != ["semester", "semester"] or parts[0]["type"] != "overview":
        errs.append("SEMESTERS overview must be first and two semester parts last")

    for p in parts:
        if [c["chapter_number"] for c in p["children"]] != list(range(1, len(p["children"]) + 1)):
            errs.append(f"ORDER chapter numbers not sequential in part '{p['title']['en']}'")
        for c in p["children"]:
            if [m["module_number"] for m in c["children"]] != list(range(1, len(c["children"]) + 1)):
                errs.append(f"ORDER module numbers not sequential in chapter '{c['title']['en']}'")
            if c["type"] == "understand":
                w = sum(m["estimated_word_count"] or 0 for m in c["children"])
                t = sum(m["estimated_time_minutes"] or 0 for m in c["children"])
                if w != c["chapter_estimated_word_count"] or t != c["chapter_estimated_time_minutes"]:
                    errs.append(f"SUMS chapter '{c['title']['en']}' totals do not match modules")

    expected_parts = 1 + len(content) + 2
    expected_chapters = sum(len(p["children"]) for p in parts)
    if outline["total_parts"] != expected_parts or outline["total_chapters"] != expected_chapters \
            or outline["total_chapters_in_course"] != expected_chapters:
        errs.append("SUMS total_parts/total_chapters mismatch")

    for p in content:
        for c in p["children"]:
            if c["type"] != "understand":
                continue
            titles = [m["title"]["en"].strip().casefold() for m in c["children"]]
            if len(titles) != len(set(titles)):
                errs.append(f"TITLES duplicate module titles in chapter '{c['title']['en']}'")
            for m in c["children"]:
                t = m["title"]["en"].strip()
                if not t or t.casefold() == c["title"]["en"].strip().casefold() or BANNED.search(t):
                    errs.append(f"TITLES bad module title '{t}' in chapter '{c['title']['en']}'")
    return errs
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_validate.py -v`
Expected: 4 PASS. (If `test_golden_is_valid` reports a `TITLES` hit from the banned regex on a legitimate golden title, narrow the regex to `\b(continued|part\s*(2|3|ii|iii)|module\s*\d+)\b` — the golden defines acceptable.)

- [ ] **Step 5: Commit**

```bash
git add outline/validate tests/unit/test_validate.py
git commit -m "feat(validate): final outline invariants"
```

---

### Task 8: State, config, LLM wrapper, FakeLLM, prompt templates

**Files:**
- Create: `outline/state.py`, `outline/config.py`, `outline/llm.py`, `outline/prompts/annotate.md`, `outline/prompts/plan_parts.md`, `outline/prompts/plan_chapters.md`, `outline/prompts/titles.md`
- Test: `tests/unit/test_llm.py`

**Interfaces:**
- Produces:
  - `state.LO`, `state.State`, `state.merge_los(a, b)`, `state.merge_dict(a, b)`.
  - `config.Settings` dataclass: `provider, models: dict[str,str], batch_size, max_concurrency, skill_mode_threshold, llm_timeout_seconds, transport_retries`; `config.load(path: str | None = None, **overrides) -> Settings`.
  - `llm.render(name: str, **vars) -> tuple[str, str]` returns `(system, user)`; templates split on a line `---USER---`; variables substituted as `{name}` via `str.replace`.
  - `llm.LLM(settings).call(role, system, user, schema) -> (obj, metric_dict)` (async).
  - `llm.FakeLLM(drop_ids: set[str] = frozenset(), fail_roles: set[str] = frozenset())` same `call` signature; deterministic answers derived from the pipe-delimited rows in `user`.
  - Metric dict keys: `role, model, prompt_tokens, completion_tokens, ms, attempt`.

- [ ] **Step 1: Write failing tests**

`tests/unit/test_llm.py`:
```python
import pytest
from outline.llm import render, FakeLLM
from outline.schemas import AnnotateOut, PartsOut, ChaptersOut, TitlesOut
from outline.state import merge_los


def test_render_splits_system_and_user():
    system, user = render("annotate", header="H", rows="L1 | Identify the main idea")
    assert "verb" in system.lower()
    assert "L1 | Identify the main idea" in user
    assert "{rows}" not in user and "{header}" not in user


async def test_fake_annotate_and_drop():
    fake = FakeLLM(drop_ids={"L2"})
    out, metric = await fake.call("annotate", "sys", "L1 | Identify the main idea\nL2 | Analyze evidence", AnnotateOut)
    assert [i.id for i in out.items] == ["L1"]
    assert out.items[0].verb == "identify"
    assert metric["role"] == "annotate" and metric["prompt_tokens"] > 0


async def test_fake_parts_chapters_titles():
    fake = FakeLLM()
    rows = "\n".join(f"L{i} | Skill {i // 3} | Intermediate" for i in range(30))
    parts, _ = await fake.call("plan_parts", "s", rows, PartsOut)
    assert sorted(i for p in parts.parts for i in p.ids) == sorted(f"L{i}" for i in range(30))
    chap, _ = await fake.call("plan_chapters", "s", rows, ChaptersOut)
    assert len(chap.assignments) == 30 and chap.assignments[0].order_rank == 1
    titles, _ = await fake.call("titles", "s", rows, TitlesOut)
    assert len({t.title for t in titles.modules}) == 30


def test_merge_los_patches_by_id():
    a = {"L1": {"id": "L1", "text": "x"}}
    b = {"L1": {"verb": "identify"}, "L2": {"id": "L2"}}
    m = merge_los(a, b)
    assert m["L1"] == {"id": "L1", "text": "x", "verb": "identify"} and "L2" in m
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_llm.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement state and config**

`outline/state.py`:
```python
"""Graph state: one ID-keyed copy of LO data + small aggregates. Nodes return partial dicts."""
import operator
from typing import Annotated, TypedDict


class LO(TypedDict, total=False):
    id: str
    urn: str
    text: str
    idx: int
    verb: str
    primary_skill: str
    tier: str
    part_id: str
    chapter: str
    rank: int
    title: str
    flags: list[str]


def merge_los(a: dict[str, LO], b: dict[str, LO]) -> dict[str, LO]:
    out = {k: dict(v) for k, v in a.items()}
    for k, patch in b.items():
        cur = out.get(k, {})
        flags = list(cur.get("flags", [])) + [f for f in patch.get("flags", []) if f not in cur.get("flags", [])]
        out[k] = {**cur, **patch, "flags": flags}
    return out


def merge_dict(a: dict, b: dict) -> dict:
    return {**a, **b}


class State(TypedDict, total=False):
    raw_input: dict
    course: dict          # course_title, grade_band, subject_area, minutes_per_lesson, lessons_per_week, course_duration_weeks, progression, user_prompt
    budget: dict          # total_lesson_days, word_limit
    batches: list[list[str]]
    los: Annotated[dict[str, LO], merge_los]
    parts: list[dict]     # [{"part_id", "part_name", "ids"}]
    packed: dict
    titles: Annotated[dict[str, str], merge_dict]
    outline: dict
    validation: list[str]
    report: Annotated[list[dict], operator.add]
```

`outline/config.py`:
```python
"""Settings from config.yaml + overrides."""
from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class Settings:
    provider: str = "anthropic"
    models: dict[str, str] = field(default_factory=lambda: {"default": "claude-sonnet-4-5"})
    batch_size: int = 30
    max_concurrency: int = 5
    skill_mode_threshold: int = 300
    llm_timeout_seconds: int = 90
    transport_retries: int = 3


def load(path: str | None = None, **overrides) -> Settings:
    data: dict = {}
    p = Path(path) if path else Path("config.yaml")
    if p.exists():
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    data.update({k: v for k, v in overrides.items() if v is not None})
    return Settings(**{k: v for k, v in data.items() if k in Settings.__dataclass_fields__})
```

- [ ] **Step 4: Write prompt templates**

Each file: system text, then a line `---USER---`, then the user template. Variables: `{header}`, `{rows}`, `{guidance}`, `{count}`.

`outline/prompts/annotate.md`:
```
You are a K-12 curriculum analyst. For each learning objective row, extract:
1. verb: the first action verb describing what the student does, lowercase, base form (e.g. "identify", "analyze", "figure out").
2. primary_skill: a 2-4 word Title Case noun phrase naming the competency, derived only from the objective text, no verbs (e.g. "Evidence Analysis", "Slope", "Main Idea"). Use the same primary_skill for objectives that develop the same competency.
Return every id exactly as given. Do not invent, skip, or merge ids.
---USER---
{header}

Rows: id | objective
{rows}
```

`outline/prompts/plan_parts.md`:
```
You are a K-12 curriculum designer. Group the items below into ordered course units (parts).
{guidance}
Rules:
- Aim for units of roughly 4-8 chapter groups (about 10-30 items). This is guidance only: a downstream system merges undersized units, so never pad or force sizes.
- part_name: a specific noun phrase, at most 6 words, Title Case, no generic labels like "Unit 1" and no repeated wording across units.
- Order units so foundational content precedes advanced content, following the progression style above.
- Every id must appear in exactly one unit. Return ids exactly as given. Do not invent ids.
---USER---
{header}

Items ({count}): id | skill | tier
{rows}
```

`outline/prompts/plan_chapters.md`:
```
You are planning one unit of a K-12 course. Group the objectives below into lesson-sized chapters and order them.
Rules:
- About 3 objectives per chapter; use 2 for deep or Advanced objectives; 4 only for a coherent leftover cluster.
- chapter_name: 2-4 word Title Case noun phrase, unique within the unit, no generic labels, no "Part 2" suffixes.
- order_rank: chapters ordered Foundational -> Intermediate -> Advanced; within a tier put prerequisites first. Objectives in the same chapter share the same order_rank.
- Assign every id exactly once. Return ids exactly as given.
---USER---
{header}

Rows: id | objective | skill | tier
{rows}
```

`outline/prompts/titles.md`:
```
You write module titles for a K-12 course. For each objective row, write a specific 2-5 word Title Case noun phrase describing the concrete skill or concept taught (derived from the objective's verb and object).
Rules:
- Titles must be distinct within a chapter and must not equal the chapter name.
- Never use generic labels ("Module 1", "Activity", "Practice") or suffixes ("Continued", "Part 2").
- Return every id exactly as given.
---USER---
{header}

Rows: chapter | id | objective | skill
{rows}
```

- [ ] **Step 5: Implement `outline/llm.py`**

```python
"""Provider-agnostic structured LLM calls + offline FakeLLM + prompt rendering."""
from __future__ import annotations

import asyncio
import re
import time
from importlib import resources
from typing import TypeVar

from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from outline.config import Settings
from outline.schemas import AnnotateOut, ChaptersOut, PartsOut, TitlesOut

T = TypeVar("T", bound=BaseModel)


def render(name: str, **vars: str) -> tuple[str, str]:
    text = resources.files("outline.prompts").joinpath(f"{name}.md").read_text(encoding="utf-8")
    system, user = text.split("---USER---", 1)
    for k, v in vars.items():
        user = user.replace("{" + k + "}", str(v))
        system = system.replace("{" + k + "}", str(v))
    return system.strip(), user.strip()


def _tokens(s: str) -> int:
    return max(1, len(s) // 4)


class LLM:
    """LangChain-backed client. provider in {anthropic, openai, bedrock_converse}."""

    def __init__(self, settings: Settings):
        from langchain.chat_models import init_chat_model
        self.settings = settings
        self._models = {
            role: init_chat_model(f"{settings.provider}:{name}", temperature=0, timeout=settings.llm_timeout_seconds)
            for role, name in settings.models.items()
        }
        self._sem = asyncio.Semaphore(settings.max_concurrency)

    async def call(self, role: str, system: str, user: str, schema: type[T]) -> tuple[T, dict]:
        model = self._models.get(role, self._models["default"])
        runnable = model.with_structured_output(schema, include_raw=True)
        messages = [("system", system), ("human", user)]
        t0 = time.perf_counter()
        attempt = 0

        @retry(stop=stop_after_attempt(self.settings.transport_retries), wait=wait_exponential_jitter(1, 20), reraise=True)
        async def _invoke(msgs):
            nonlocal attempt
            attempt += 1
            async with self._sem:
                return await runnable.ainvoke(msgs)

        result = await _invoke(messages)
        parsed = result.get("parsed")
        if parsed is None:  # schema failure: one corrective retry
            err = str(result.get("parsing_error"))[:500]
            result = await _invoke(messages + [("human", f"Your previous reply did not match the schema: {err}. Reply again with valid data.")])
            parsed = result["parsed"]
            if parsed is None:
                raise ValidationError.from_exception_data(schema.__name__, [])
        usage = getattr(result.get("raw"), "usage_metadata", None) or {}
        metric = {
            "role": role, "model": self.settings.models.get(role, self.settings.models["default"]),
            "prompt_tokens": usage.get("input_tokens", _tokens(system + user)),
            "completion_tokens": usage.get("output_tokens", 0),
            "ms": int((time.perf_counter() - t0) * 1000), "attempt": attempt,
        }
        return parsed, metric


_ROW = re.compile(r"^\s*([^|]+?)\s*\|\s*(.*)$")


class FakeLLM:
    """Deterministic offline stand-in. Parses pipe rows from `user`; answers per schema."""

    def __init__(self, drop_ids: set[str] = frozenset(), fail_roles: set[str] = frozenset()):
        self.drop_ids, self.fail_roles = set(drop_ids), set(fail_roles)
        self.calls: list[dict] = []

    @staticmethod
    def _rows(user: str) -> list[list[str]]:
        rows = []
        for line in user.splitlines():
            m = _ROW.match(line)
            if m and not line.lower().startswith(("rows:", "items")):
                rows.append([m.group(1).strip()] + [c.strip() for c in m.group(2).split("|")])
        return rows

    async def call(self, role: str, system: str, user: str, schema: type[T]) -> tuple[T, dict]:
        self.calls.append({"role": role, "user": user})
        if role in self.fail_roles:
            raise RuntimeError(f"fake failure for {role}")
        rows = [r for r in self._rows(user)]
        metric = {"role": role, "model": "fake", "prompt_tokens": _tokens(system + user), "completion_tokens": 0, "ms": 0, "attempt": 1}
        if schema is AnnotateOut:
            items = []
            for r in rows:
                if r[0] in self.drop_ids:
                    continue
                words = re.findall(r"[A-Za-z]+", r[1])
                verb = words[0].lower() if words else "identify"
                skill = " ".join(w.title() for w in words[1:4] if len(w) > 3) or "General Skill"
                items.append({"id": r[0], "verb": verb, "primary_skill": skill})
            return AnnotateOut.model_validate({"items": items}), metric
        if schema is PartsOut:
            ids = [r[0] for r in rows if r[0] not in self.drop_ids]
            size = 12
            parts = [{"part_name": f"Unit {j + 1} Concepts", "ids": ids[j * size:(j + 1) * size]} for j in range((len(ids) + size - 1) // size)]
            return PartsOut.model_validate({"parts": parts or [{"part_name": "Unit 1 Concepts", "ids": ids[:1] or ["L1"]}]}), metric
        if schema is ChaptersOut:
            ids = [r[0] for r in rows if r[0] not in self.drop_ids]
            a = [{"id": i, "chapter_name": f"Chapter {k // 3 + 1} Topics", "order_rank": k // 3 + 1} for k, i in enumerate(ids)]
            return ChaptersOut.model_validate({"assignments": a}), metric
        if schema is TitlesOut:
            ids = [r[1] if len(r) > 2 and r[1].startswith("L") else r[0] for r in rows]
            mods = [{"id": i, "title": f"Concept {i} Skills"} for i in ids if i not in self.drop_ids]
            return TitlesOut.model_validate({"modules": mods}), metric
        raise NotImplementedError(schema)
```

- [ ] **Step 6: Run tests**

Run: `pytest tests/unit/test_llm.py -v`
Expected: 4 PASS.

- [ ] **Step 7: Commit**

```bash
git add outline/state.py outline/config.py outline/llm.py outline/prompts tests/unit/test_llm.py
git commit -m "feat: state, settings, provider-agnostic LLM wrapper, FakeLLM, prompt templates"
```

---

### Task 9: Nodes — ingest, annotate, plan_parts, plan_chapters

**Files:**
- Create: `outline/nodes.py`
- Test: `tests/unit/test_nodes.py`

**Interfaces:**
- Consumes: `State`, `Settings`, `LLM/FakeLLM.call`, `render`, `rules.*`.
- Produces (all `async def node(state, config) -> dict` unless noted; `config["configurable"]` carries `"llm"` and `"settings"`):
  - `ingest(state, config)` (sync) → `course, budget, los, batches, parts=[], titles={}, report=[]`
  - `fan_out_annotate(state) -> list[Send]`
  - `annotate(payload, config)` → `los` patches (`verb, primary_skill, tier, flags`) + `report`
  - `plan_parts(state, config)` → `parts` + `los` patches (`part_id`) + `report`
  - `fan_out_chapters(state) -> list[Send]`
  - `plan_chapters(payload, config)` → `los` patches (`chapter, rank`) + `report`
  - helper `course_header(course, budget, part_names=(), this_part=None) -> str`

- [ ] **Step 1: Write failing tests**

`tests/unit/test_nodes.py`:
```python
import pytest
from outline.config import Settings
from outline.llm import FakeLLM
from outline.nodes import ingest, fan_out_annotate, annotate, plan_parts, fan_out_chapters, plan_chapters


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


async def test_plan_chapters_per_part(input43):
    st = ingest({"raw_input": input43}, cfg(FakeLLM()))
    for lo in st["los"].values():
        lo.update(verb="identify", primary_skill="Skill", tier="Foundational")
    st.update(await plan_parts(st, cfg(FakeLLM())))
    sends = fan_out_chapters(st)
    assert len(sends) == len(st["parts"])
    out = await plan_chapters(sends[0].arg, cfg(FakeLLM(drop_ids={"L1"})))
    assert set(out["los"]) == set(sends[0].arg["part"]["ids"])
    assert all("chapter" in v and "rank" in v for v in out["los"].values())
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_nodes.py -v`
Expected: FAIL `ModuleNotFoundError`.

- [ ] **Step 3: Implement `outline/nodes.py` (part 1)**

```python
"""Graph nodes. LLM nodes: validate -> re-ask missing ids once -> deterministic fallback."""
from __future__ import annotations

from collections import Counter, defaultdict

from langgraph.types import Send

from outline.assemble.dcim import build as build_outline
from outline.llm import render
from outline.rules.blooms import tier_for
from outline.rules.estimates import word_limit
from outline.rules.grade_band import normalize
from outline.rules.naming import skill_key
from outline.rules.structure import build_structure
from outline.schemas import AnnotateOut, ChaptersOut, CourseRequest, PartsOut, TitlesOut
from outline.validate.invariants import check

GUIDANCE = {
    "SKILLS_BASED_PROGRESSION": "Progression style: SKILLS-BASED. Group by shared skill into coherent skill domains; order simple/foundational skills before complex ones.",
    "THEME_BASED_PROGRESSION": "Progression style: THEME-BASED. Group by theme or big idea; order units as a narrative of ideas.",
    "CHRONOLOGICAL_PROGRESSION": "Progression style: CHRONOLOGICAL. Group and order units by historical/temporal sequence implied by the objectives.",
    "STANDARDS_DRIVEN_PROGRESSION": "Progression style: STANDARDS-DRIVEN. Keep the given item order (framework order); units are contiguous runs of items.",
}


def _cfg(config):
    c = config["configurable"]
    return c["llm"], c["settings"]


def course_header(course: dict, budget: dict, part_names=(), this_part: str | None = None) -> str:
    lines = [
        f"COURSE: {course['course_title']} | grade band {course['grade_band']} | {course['subject_area']} | {course['progression']}",
        f"CALENDAR: {course['lessons_per_week']} lessons/week x {course['course_duration_weeks']} weeks = "
        f"{budget['total_lesson_days']} lesson days; {course['minutes_per_lesson']} min/lesson; chapter word limit {budget['word_limit']}",
    ]
    if part_names:
        lines.append("UNITS: " + " · ".join(f"{i + 1}. {n}" for i, n in enumerate(part_names)))
    if this_part:
        lines.append(f"THIS UNIT: {this_part}")
    if course.get("user_prompt"):
        lines.append(f"USER GUIDANCE: {course['user_prompt']}")
    return "\n".join(lines)


# ---------------- ingest ----------------
def ingest(state: dict, config) -> dict:
    _, settings = _cfg(config)
    req = CourseRequest.model_validate(state["raw_input"])
    los = {
        f"L{i + 1}": {"id": f"L{i + 1}", "urn": lo.learning_objective_urn, "text": lo.objective, "idx": i, "flags": []}
        for i, lo in enumerate(req.learning_objectives)
    }
    course = {
        "course_title": req.course_title, "grade_band": req.grade_band, "subject_area": req.subject_area,
        "minutes_per_lesson": req.minutes_per_lesson, "lessons_per_week": req.lessons_per_week,
        "course_duration_weeks": req.course_duration_weeks, "progression": req.course_outline_progression,
        "user_prompt": req.user_prompt,
    }
    budget = {"total_lesson_days": req.lessons_per_week * req.course_duration_weeks, "word_limit": word_limit(req.grade_band)}
    ids = list(los)
    batches = [ids[i:i + settings.batch_size] for i in range(0, len(ids), settings.batch_size)]
    return {"course": course, "budget": budget, "los": los, "batches": batches, "parts": [], "titles": {}, "report": []}


# ---------------- annotate ----------------
def fan_out_annotate(state: dict) -> list[Send]:
    return [Send("annotate", {"batch": ids, "los": {i: state["los"][i] for i in ids},
                              "course": state["course"], "budget": state["budget"]}) for ids in state["batches"]]


def _fallback_annotation(text: str) -> dict:
    words = [w.strip(".,;:()") for w in text.split()]
    verb = words[0].lower() if words else "identify"
    content = [w for w in words[1:] if len(w) > 3][:3]
    return {"verb": verb, "primary_skill": " ".join(w.title() for w in content) or "General Skill"}


async def annotate(payload: dict, config) -> dict:
    llm, _ = _cfg(config)
    los, batch = payload["los"], payload["batch"]
    header = course_header(payload["course"], payload["budget"])
    got: dict[str, dict] = {}
    report = []
    pending = list(batch)
    for _attempt in range(2):
        rows = "\n".join(f"{i} | {los[i]['text']}" for i in pending)
        system, user = render("annotate", header=header, rows=rows)
        try:
            out, metric = await llm.call("annotate", system, user, AnnotateOut)
            report.append({"node": "annotate", **metric})
        except Exception as exc:  # transport/schema failure → fallback below
            report.append({"node": "annotate", "error": str(exc)[:200]})
            break
        for it in out.items:
            if it.id in los and it.id not in got:
                got[it.id] = {"verb": it.verb.strip().lower(), "primary_skill": it.primary_skill.strip()}
        pending = [i for i in batch if i not in got]
        if not pending:
            break
    patches = {}
    for i in batch:
        base = got.get(i)
        flags = []
        if base is None:
            base = _fallback_annotation(los[i]["text"])
            flags = ["annotate_fallback"]
        patches[i] = {**base, "tier": tier_for(base["verb"]), "flags": flags}
    return {"los": patches, "report": report}


# ---------------- plan_parts ----------------
def _skill_rows(los: dict) -> tuple[str, dict[str, list[str]]]:
    groups: dict[str, list[str]] = defaultdict(list)
    label: dict[str, str] = {}
    for lo in sorted(los.values(), key=lambda x: x["idx"]):
        k = skill_key(lo["primary_skill"])
        groups[k].append(lo["id"])
        label.setdefault(k, lo["primary_skill"])
    keys = list(groups)
    rows, mapping = [], {}
    for n, k in enumerate(keys, start=1):
        sid = f"S{n}"
        mapping[sid] = groups[k]
        tiers = Counter(los[i]["tier"] for i in groups[k])
        tier_txt = "/".join(f"{t[:3]}{c}" for t, c in tiers.items())
        example = los[groups[k][0]]["text"][:80]
        rows.append(f"{sid} | {label[k]} | {len(groups[k])} | {tier_txt} | {example}")
    return "\n".join(rows), mapping


async def plan_parts(state: dict, config) -> dict:
    llm, settings = _cfg(config)
    los, course, budget = state["los"], state["course"], state["budget"]
    header = course_header(course, budget)
    guidance = GUIDANCE[course["progression"]]
    skill_mode = len(los) > settings.skill_mode_threshold
    report = []
    if skill_mode:
        rows, mapping = _skill_rows(los)
        all_keys = list(mapping)
        rows = "skill | count | tiers | example\n" + rows  # header row for skill mode (FakeLLM/test hook)
    else:
        mapping = {i: [i] for i in los}
        all_keys = sorted(los, key=lambda i: los[i]["idx"])
        rows = "\n".join(f"{i} | {los[i]['primary_skill']} | {los[i]['tier']}" for i in all_keys)
    parts: list[dict] = []
    assigned: set[str] = set()
    pending = list(all_keys)
    for _attempt in range(2):
        system, user = render("plan_parts", header=header, guidance=guidance, rows=rows, count=str(len(pending)))
        if parts:
            user += "\n\nExisting units: " + "; ".join(p["part_name"] for p in parts) + \
                    "\nPlace ONLY the ids below into existing units (reuse the exact part_name) or a new unit."
        try:
            out, metric = await llm.call("plan_parts", system, user, PartsOut)
            report.append({"node": "plan_parts", **metric})
        except Exception as exc:
            report.append({"node": "plan_parts", "error": str(exc)[:200]})
            break
        for item in out.parts:
            keys = [k for k in item.ids if k in mapping and k not in assigned]
            if not keys:
                continue
            existing = next((p for p in parts if p["part_name"] == item.part_name), None)
            if existing:
                existing["keys"].extend(keys)
            else:
                parts.append({"part_name": item.part_name, "keys": keys})
            assigned.update(keys)
        pending = [k for k in all_keys if k not in assigned]
        if not pending:
            break
        rows = "\n".join(r for r in rows.splitlines() if r.split(" | ")[0] in pending)
    fallback_flags: set[str] = set()
    if pending:
        if not parts:
            parts.append({"part_name": f"{course['course_title']} Core Concepts", "keys": []})
        for k in pending:
            lo_ids = mapping[k]
            sk = skill_key(los[lo_ids[0]].get("primary_skill", ""))
            target = next((p for p in parts if any(skill_key(los[j].get("primary_skill", "")) == sk
                                                   for kk in p["keys"] for j in mapping[kk])), parts[-1])
            target["keys"].append(k)
            fallback_flags.update(lo_ids)
    result_parts, patches = [], {}
    for n, p in enumerate(parts, start=1):
        pid = f"P{n}"
        ids = [i for k in p["keys"] for i in mapping[k]]
        ids.sort(key=lambda i: los[i]["idx"])
        result_parts.append({"part_id": pid, "part_name": p["part_name"], "ids": ids})
        for i in ids:
            patches[i] = {"part_id": pid, "flags": (["plan_parts_fallback"] if i in fallback_flags else [])}
    return {"parts": result_parts, "los": patches, "report": report}


# ---------------- plan_chapters ----------------
def fan_out_chapters(state: dict) -> list[Send]:
    names = [p["part_name"] for p in state["parts"]]
    return [Send("plan_chapters", {"part": p, "los": {i: state["los"][i] for i in p["ids"]},
                                   "course": state["course"], "budget": state["budget"], "part_names": names})
            for p in state["parts"]]


async def plan_chapters(payload: dict, config) -> dict:
    llm, _ = _cfg(config)
    part, los = payload["part"], payload["los"]
    header = course_header(payload["course"], payload["budget"], payload["part_names"], this_part=part["part_name"])
    got: dict[str, dict] = {}
    report = []
    pending = list(part["ids"])
    for _attempt in range(2):
        rows = "\n".join(f"{i} | {los[i]['text']} | {los[i]['primary_skill']} | {los[i]['tier']}" for i in pending)
        system, user = render("plan_chapters", header=header, rows=rows)
        try:
            out, metric = await llm.call("plan_chapters", system, user, ChaptersOut)
            report.append({"node": "plan_chapters", "part": part["part_id"], **metric})
        except Exception as exc:
            report.append({"node": "plan_chapters", "part": part["part_id"], "error": str(exc)[:200]})
            break
        for a in out.assignments:
            if a.id in los and a.id not in got:
                got[a.id] = {"chapter": a.chapter_name.strip(), "rank": a.order_rank}
        pending = [i for i in part["ids"] if i not in got]
        if not pending:
            break
    patches = {}
    tier_rank = {"Foundational": 1, "Intermediate": 2, "Advanced": 3}
    max_rank = max((v["rank"] for v in got.values()), default=0)
    for i in part["ids"]:
        if i in got:
            patches[i] = {**got[i], "flags": []}
        else:
            lo = los[i]
            patches[i] = {"chapter": lo["primary_skill"], "rank": max_rank + tier_rank.get(lo["tier"], 1),
                          "flags": ["plan_chapters_fallback"]}
    return {"los": patches, "report": report}
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_nodes.py -v`
Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add outline/nodes.py tests/unit/test_nodes.py
git commit -m "feat(nodes): ingest, annotate, plan_parts (id + skill mode), plan_chapters"
```

---

### Task 10: Nodes — pack_and_merge, titles, assemble, validate; graph wiring; end-to-end

**Files:**
- Modify: `outline/nodes.py` (append)
- Create: `outline/graph.py`
- Test: `tests/graph/test_end_to_end.py`

**Interfaces:**
- Produces:
  - `nodes.pack_and_merge(state, config)` → `packed`
  - `nodes.fan_out_titles(state) -> list[Send]`, `nodes.titles(payload, config)` → `titles` + `los` flags + `report`
  - `nodes.assemble(state, config)` → `outline`
  - `nodes.validate(state, config)` → `validation: list[str]`; raises `PipelineBug` on structural failure
  - `graph.build_graph(llm, settings) -> CompiledGraph`; run with `await app.ainvoke({"raw_input": ...}, config={"configurable": {"llm": llm, "settings": settings, "thread_id": "run-1"}})`

- [ ] **Step 1: Write failing end-to-end test**

`tests/graph/test_end_to_end.py`:
```python
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
    assert check(out, [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]) == []
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


async def test_llm_failure_in_titles_uses_fallback(input43):
    fake = FakeLLM(fail_roles={"titles"})
    final = await run(input43, llm=fake)
    assert final["validation"] == []
    assert all("titles_fallback" in lo["flags"] for lo in final["los"].values())
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/graph/test_end_to_end.py -v`
Expected: FAIL `ImportError` (graph/pack_and_merge missing).

- [ ] **Step 3: Append remaining nodes to `outline/nodes.py`**

```python
# ---------------- pack_and_merge ----------------
class PipelineBug(RuntimeError):
    """A structural invariant produced by code was violated — a bug, never retried."""


def pack_and_merge(state: dict, config) -> dict:
    packed = build_structure(state["course"], state["budget"], state["los"], state["parts"])
    if not packed["validation"]["valid"]:
        raise PipelineBug(f"pack_and_merge coverage failure: {packed['validation']}")
    return {"packed": packed, "report": [{"node": "pack_and_merge", "enforcement_log": packed["enforcement_log"]}]}


# ---------------- titles ----------------
def fan_out_titles(state: dict) -> list[Send]:
    names = [p["part_name"] for p in state["packed"]["parts"]]
    return [Send("titles", {"part": p, "los": {lo["id"]: state["los"][lo["id"]] for c in p["chapters"] for lo in c["learning_objectives"]},
                            "course": state["course"], "budget": state["budget"], "part_names": names})
            for p in state["packed"]["parts"]]


def _fallback_title(lo: dict) -> str:
    return f"{lo.get('primary_skill', 'Concept')}: {lo.get('verb', 'apply').title()}"


async def titles(payload: dict, config) -> dict:
    llm, _ = _cfg(config)
    part, los = payload["part"], payload["los"]
    header = course_header(payload["course"], payload["budget"], payload["part_names"], this_part=part["part_name"])
    chapter_of = {lo["id"]: c["chapter_name"] for c in part["chapters"] for lo in c["learning_objectives"]}
    ids = list(chapter_of)
    got: dict[str, str] = {}
    report = []
    pending = ids
    for _attempt in range(2):
        rows = "\n".join(f"{chapter_of[i]} | {i} | {los[i]['text']} | {los[i]['primary_skill']}" for i in pending)
        system, user = render("titles", header=header, rows=rows)
        try:
            out, metric = await llm.call("titles", system, user, TitlesOut)
            report.append({"node": "titles", "part": part["part_number"], **metric})
        except Exception as exc:
            report.append({"node": "titles", "part": part["part_number"], "error": str(exc)[:200]})
            break
        for t in out.modules:
            if t.id in chapter_of and t.id not in got:
                got[t.id] = t.title.strip()
        # reject duplicates within a chapter and titles equal to the chapter name
        seen: dict[str, set[str]] = defaultdict(set)
        for i in ids:
            if i in got:
                key = got[i].casefold()
                if key == chapter_of[i].casefold() or key in seen[chapter_of[i]]:
                    del got[i]
                else:
                    seen[chapter_of[i]].add(key)
        pending = [i for i in ids if i not in got]
        if not pending:
            break
    result, patches = {}, {}
    used: dict[str, set[str]] = defaultdict(set)
    for i in ids:
        title = got.get(i)
        flags = []
        if title is None:
            title = _fallback_title(los[i])
            flags = ["titles_fallback"]
        base, n = title, 2
        while title.casefold() in used[chapter_of[i]] or title.casefold() == chapter_of[i].casefold():
            title = f"{base} ({los[i]['id']})" if n == 2 else f"{base} {n}"
            n += 1
        used[chapter_of[i]].add(title.casefold())
        result[i] = title
        patches[i] = {"title": title, "flags": flags}
    return {"titles": result, "los": patches, "report": report}


# ---------------- assemble / validate ----------------
def assemble(state: dict, config) -> dict:
    return {"outline": build_outline(state["course"], state["budget"], state["packed"], state["titles"])}


def validate(state: dict, config) -> dict:
    errs = check(state["outline"], [lo["urn"] for lo in state["los"].values()])
    structural = [e for e in errs if not e.startswith("TITLES")]
    if structural:
        raise PipelineBug("; ".join(structural))
    return {"validation": errs}
```

- [ ] **Step 4: Create `outline/graph.py`**

```python
"""Wire the nodes. Edges are decided by Python only."""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from outline import nodes
from outline.state import State


def build_graph(llm, settings, checkpointer=None):
    g = StateGraph(State)
    g.add_node("ingest", nodes.ingest)
    g.add_node("annotate", nodes.annotate)
    g.add_node("plan_parts", nodes.plan_parts)
    g.add_node("plan_chapters", nodes.plan_chapters)
    g.add_node("pack_and_merge", nodes.pack_and_merge)
    g.add_node("titles", nodes.titles)
    g.add_node("assemble", nodes.assemble)
    g.add_node("validate", nodes.validate)

    g.add_edge(START, "ingest")
    g.add_conditional_edges("ingest", nodes.fan_out_annotate, ["annotate"])
    g.add_edge("annotate", "plan_parts")
    g.add_conditional_edges("plan_parts", nodes.fan_out_chapters, ["plan_chapters"])
    g.add_edge("plan_chapters", "pack_and_merge")
    g.add_conditional_edges("pack_and_merge", nodes.fan_out_titles, ["titles"])
    g.add_edge("titles", "assemble")
    g.add_edge("assemble", "validate")
    g.add_edge("validate", END)
    return g.compile(checkpointer=checkpointer or MemorySaver())
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/graph/test_end_to_end.py -v`
Expected: 5 PASS. Also run full suite: `pytest -q` → all green.

Notes if failing:
- `Send` fan-out nodes receive **only** the payload dict as their state; they must not read `state["los"]` beyond what the payload carries (already so).
- If LangGraph complains about `validation` list reducer, it is a plain overwrite field — correct.

- [ ] **Step 6: Commit**

```bash
git add outline/nodes.py outline/graph.py tests/graph/test_end_to_end.py
git commit -m "feat: pack_and_merge, titles, assemble, validate nodes and LangGraph wiring; e2e green on 43/94/123"
```

---

### Task 11: CLI, report, synthetic fixtures, scale tests, live smoke

**Files:**
- Create: `outline/report.py`, `outline/__main__.py`, `scripts/make_synthetic.py`, `tests/graph/test_scale.py`, `tests/live/test_live.py`, `README.md`

**Interfaces:**
- Produces:
  - `report.build_report(final_state: dict, provider: str, wall_ms: int) -> dict`; `report.write(out_dir: Path, final_state, provider, wall_ms)` writes `outline.json`, `report.json`, `enforcement.log`.
  - CLI: `python -m outline generate INPUT.json [--provider P] [--config config.yaml] [--out out/] [--batch-size N] [--fake]`.
  - `scripts/make_synthetic.py N OUT.json` builds an N-LO input from the fixtures (URNs re-minted with `uuid5`).

- [ ] **Step 1: Write failing tests**

`tests/graph/test_scale.py`:
```python
import json
import subprocess
import sys
from pathlib import Path

import pytest
from outline.config import Settings
from outline.graph import build_graph
from outline.llm import FakeLLM
from outline.report import build_report
from outline.validate.invariants import check


def synthetic(tmp_path: Path, n: int) -> dict:
    out = tmp_path / f"syn-{n}.json"
    subprocess.run([sys.executable, "scripts/make_synthetic.py", str(n), str(out)], check=True)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data["learning_objectives"]) == n
    return data


@pytest.mark.parametrize("n", [300, 1000])
async def test_scale_fake(tmp_path, n):
    inp = synthetic(tmp_path, n)
    llm, settings = FakeLLM(), Settings(batch_size=30, skill_mode_threshold=300)
    app = build_graph(llm, settings)
    final = await app.ainvoke({"raw_input": inp}, config={"configurable": {"llm": llm, "settings": settings, "thread_id": f"s{n}"}})
    assert final["validation"] == []
    assert check(final["outline"], [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]) == []
    rep = build_report(final, "fake", 0)
    assert rep["max_prompt_tokens"] < 10_000
    assert rep["n_los"] == n
    if n > 300:
        assert any("skill | count" in c["user"] for c in llm.calls if c["role"] == "plan_parts")
```

`tests/live/test_live.py`:
```python
import os
import pytest
from outline.config import load
from outline.graph import build_graph
from outline.llm import LLM

pytestmark = pytest.mark.live


@pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="needs ANTHROPIC_API_KEY")
async def test_live_43(input43):
    settings = load("config.yaml", provider="anthropic")
    llm = LLM(settings)
    app = build_graph(llm, settings)
    final = await app.ainvoke({"raw_input": input43}, config={"configurable": {"llm": llm, "settings": settings, "thread_id": "live43"}})
    assert final["validation"] == []
    assert not any(lo.get("flags") for lo in final["los"].values())
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/graph/test_scale.py -v`
Expected: FAIL (`scripts/make_synthetic.py` missing / `outline.report` missing).

- [ ] **Step 3: Implement `scripts/make_synthetic.py`**

```python
"""Build an N-objective synthetic input from the fixture inputs (URNs re-minted, texts lightly varied)."""
import json
import sys
import uuid
from pathlib import Path

FIX = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
SOURCES = ["sample-input-43.json", "sample-input-49.json", "sample-input-94.json", "sample-input-123.json"]


def main(n: int, out: Path) -> None:
    pool = []
    for name in SOURCES:
        pool.extend(json.loads((FIX / name).read_text(encoding="utf-8"))["learning_objectives"])
    base = json.loads((FIX / "sample-input-94.json").read_text(encoding="utf-8"))
    los = []
    for i in range(n):
        src = pool[i % len(pool)]
        suffix = f" (variant {i // len(pool) + 1})" if i >= len(pool) else ""
        los.append({"learning_objective_urn": f"urn:pearson:learninggoal:{uuid.uuid5(uuid.NAMESPACE_URL, f'syn-{i}')}",
                    "objective": src["objective"] + suffix})
    weeks = max(base["course_duration_weeks"], (n * 2) // base["lessons_per_week"] + 8)
    data = {**base, "course_title": f"Synthetic_{n}", "course_duration_weeks": weeks, "learning_objectives": los}
    data.pop("PearsonExtSSOSession", None)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(int(sys.argv[1]), Path(sys.argv[2]))
```

- [ ] **Step 4: Implement `outline/report.py`**

```python
"""Run report: tokens, calls, fallbacks, invariants, pacing."""
import json
from collections import Counter
from pathlib import Path


def build_report(final: dict, provider: str, wall_ms: int) -> dict:
    calls = [r for r in final.get("report", []) if "prompt_tokens" in r]
    flags = Counter(f for lo in final["los"].values() for f in lo.get("flags", []))
    enforcement = next((r["enforcement_log"] for r in final.get("report", []) if "enforcement_log" in r), "")
    out = final.get("outline", {})
    return {
        "provider": provider,
        "n_los": len(final["los"]),
        "llm_calls": len(calls),
        "errors": [r for r in final.get("report", []) if "error" in r],
        "prompt_tokens": sum(c["prompt_tokens"] for c in calls),
        "completion_tokens": sum(c["completion_tokens"] for c in calls),
        "max_prompt_tokens": max((c["prompt_tokens"] for c in calls), default=0),
        "by_node": {n: {"calls": sum(1 for c in calls if c["role"] == n),
                        "prompt_tokens": sum(c["prompt_tokens"] for c in calls if c["role"] == n)}
                    for n in sorted({c["role"] for c in calls})},
        "fallbacks": dict(flags),
        "validation": final.get("validation", []),
        "enforcement_log": enforcement,
        "pacing": {k: out.get(k) for k in ("total_lesson_days", "total_chapters", "pacing_overrun", "pacing_overrun_lesson_days")},
        "wall_ms": wall_ms,
    }


def write(out_dir: Path, final: dict, provider: str, wall_ms: int) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "outline.json").write_text(json.dumps(final["outline"], indent=2), encoding="utf-8")
    rep = build_report(final, provider, wall_ms)
    (out_dir / "report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    (out_dir / "enforcement.log").write_text(rep["enforcement_log"], encoding="utf-8")
    return rep
```

- [ ] **Step 5: Implement `outline/__main__.py`**

```python
"""CLI: python -m outline generate INPUT.json [--provider ...] [--out out/] [--fake]"""
import argparse
import asyncio
import json
import time
from pathlib import Path

from outline.config import load
from outline.graph import build_graph
from outline.llm import LLM, FakeLLM
from outline.report import write


async def _run(args) -> None:
    settings = load(args.config, provider=args.provider, batch_size=args.batch_size)
    llm = FakeLLM() if args.fake else LLM(settings)
    app = build_graph(llm, settings)
    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    cfg = {"configurable": {"llm": llm, "settings": settings, "thread_id": f"run-{int(time.time())}"},
           "max_concurrency": settings.max_concurrency}
    t0 = time.perf_counter()
    final = None
    async for event in app.astream({"raw_input": raw}, config=cfg, stream_mode="updates"):
        for node, update in event.items():
            extra = ""
            if node == "ingest":
                extra = f"{len(update['los'])} objectives, {len(update['batches'])} batches"
            elif node == "plan_parts":
                extra = f"{len(update['parts'])} units"
            elif node == "pack_and_merge":
                extra = f"{update['packed']['num_content_parts']} parts / {update['packed']['content_chapter_count']} chapters"
            print(f"[{time.perf_counter() - t0:6.1f}s] {node:15s} {extra}")
    final = await app.aget_state(cfg)
    rep = write(Path(args.out), final.values, "fake" if args.fake else settings.provider, int((time.perf_counter() - t0) * 1000))
    print(json.dumps({k: rep[k] for k in ("n_los", "llm_calls", "prompt_tokens", "completion_tokens", "max_prompt_tokens", "fallbacks", "validation")}, indent=2))
    print(f"wrote {args.out}/outline.json and report.json")


def main() -> None:
    p = argparse.ArgumentParser(prog="outline")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("input")
    g.add_argument("--provider", default=None, choices=["anthropic", "openai", "bedrock_converse"])
    g.add_argument("--config", default="config.yaml")
    g.add_argument("--out", default="out")
    g.add_argument("--batch-size", type=int, default=None)
    g.add_argument("--fake", action="store_true", help="use FakeLLM (offline)")
    args = p.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run tests and the CLI**

Run: `pytest -q` → all green including `tests/graph/test_scale.py` (1,000-LO FakeLLM run should finish in seconds).
Run: `python -m outline generate tests/fixtures/sample-input-94.json --fake --out out/94-fake` → prints node progress and summary; `out/94-fake/outline.json` exists.
Run (needs key): `python -m outline generate tests/fixtures/sample-input-43.json --provider anthropic --out out/43-live` → `validation: []`, `fallbacks: {}` expected. Then `--provider openai` with `OPENAI_API_KEY` and `models.default` overridden in `config.yaml` to an OpenAI model id.

- [ ] **Step 7: Write README.md**

```markdown
# Course Outline Generator (LangGraph)

Turns learning objectives JSON into a DCIM course outline. LLMs decide names/grouping; Python owns structure.

## Run
    pip install -e ".[dev]"
    set ANTHROPIC_API_KEY=...
    python -m outline generate tests/fixtures/sample-input-94.json --out out/94
    python -m outline generate tests/fixtures/sample-input-94.json --fake   # offline

Providers: `--provider anthropic|openai|bedrock_converse` (model ids in `config.yaml`).

## Test
    pytest -q                 # unit + graph (offline)
    pytest -m live            # real provider smoke (needs key)

## Layout
See docs/DESIGN-Course-Outline-Generator-LangGraph.md.
```

- [ ] **Step 8: Commit**

```bash
git add outline/report.py outline/__main__.py scripts/make_synthetic.py tests/graph/test_scale.py tests/live README.md
git commit -m "feat: CLI, run report, synthetic fixtures, scale tests (300/1000), live smoke"
```

---

## Self-Review

**Spec coverage** (lean design → tasks):
- §3 graph, 7 node types → Tasks 9–10. §4 state/reducers → Task 8. §5 node table incl. fallbacks and >300 skill mode → Tasks 9–10. §6 LLM layer (`init_chat_model`, structured output, FakeLLM, per-role models) → Task 8. §7 four prompts → Task 8. §8 deterministic core (blooms, estimates, packing, merging, naming, structure, assessments, pacing, invariants) → Tasks 2–7. §9 layout + CLI + report → Tasks 0, 11. §10 scale numbers → Task 11 asserts `max_prompt_tokens < 10k`. §11 artefacts → Task 11. §12 build order → task order matches. §13 not-built list respected (no API/DB).
- Course header (global context) → `course_header` in Task 9, used by chapters/titles.

**Placeholder scan:** none; every step has code. Regex narrowing note in Task 7 is a conditional instruction with an exact replacement.

**Type consistency:** `los[id]` keys (`id, urn, text, idx, verb, primary_skill, tier, part_id, chapter, rank, title, flags`) consistent across `state.py`, `structure.py` (`tier`, `chapter`, `rank`, `primary_skill`), `nodes.py`. `packed` shape from Task 5 consumed unchanged by Task 6 `build` and Task 10 `fan_out_titles`. `titles` keyed by LO `id`; `dcim.build` reads `titles.get(lo["id"])` — in Task 6's golden test ids are URNs on both sides, consistent. `Settings` fields used in nodes: `batch_size`, `skill_mode_threshold`, `max_concurrency`, `transport_retries`, `llm_timeout_seconds` — all defined. `merge_los` preserves `flags` union; nodes always send `flags` (possibly `[]`).
