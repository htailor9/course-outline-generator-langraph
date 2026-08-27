# Build Guide — Scalable Course Outline Generator (Python + LangGraph)

> **Purpose:** A complete, from-scratch guide to designing, building, testing and productionising the Course Outline Generator described in `docs/superpowers/specs/2026-08-27-course-outline-generator-langgraph-design.md`.
> **Audience:** An engineer who has never seen this codebase and must recreate it end-to-end.
> **Conventions:** `[code]` = deterministic Python, `[LLM]` = model call, `∥` = runs in parallel. Code blocks are reference skeletons — they show shape and contracts, not final implementations.

---

## Table of Contents

- [Part A — What You Are Building](#part-a--what-you-are-building)
  - [A1. Problem in one paragraph](#a1-problem-in-one-paragraph)
  - [A2. Design principles (non-negotiable)](#a2-design-principles-non-negotiable)
  - [A3. Architecture diagrams](#a3-architecture-diagrams)
  - [A4. Data-flow diagram (what each node reads/writes)](#a4-data-flow-diagram-what-each-node-readswrites)
- [Part B — Environment and Repository Setup](#part-b--environment-and-repository-setup)
- [Part C — Data Contracts](#part-c--data-contracts)
- [Part D — Step-by-Step Build (12 phases)](#part-d--step-by-step-build-12-phases)
- [Part E — Prompt Engineering Guide](#part-e--prompt-engineering-guide)
- [Part F — Coding Conventions ("Styling")](#part-f--coding-conventions-styling)
- [Part G — Testing and Evaluation](#part-g--testing-and-evaluation)
- [Part H — Production Architecture](#part-h--production-architecture)
- [Part I — Operations Runbook](#part-i--operations-runbook)
- [Part J — Completion Checklist](#part-j--completion-checklist)
- [Part K — Scaling to 500, 1,000, 2,000+ LOs and Large Outputs](#part-k--scaling-to-500-1000-2000-los-and-large-outputs)

---

# Part A — What You Are Building

## A1. Problem in one paragraph

Input: a JSON list of K-12 learning objectives (LOs), each with a URN and text, plus course metadata (title, grade band, subject, minutes per lesson, lessons per week, duration in weeks, progression type, optional user prompt). Output: a DCIM course outline JSON — a tree of **Parts (Units) → Chapters (Lessons) → Modules**, where every LO becomes exactly one module, every content part has ≥ 4 understand chapters, chapters fit within a lesson day, structural chapters (Introduction, Apply, Review, Part Test, Semester A/B Review and Exam) are inserted, word/time estimates are attached, and pacing against the course calendar is reported. It must work identically for 10 or 300+ LOs, and run on Anthropic, OpenAI or Bedrock models.

## A2. Design principles (non-negotiable)

1. **LLMs decide, Python owns the data.** No LLM ever re-emits data it was given. LLM outputs are ID-keyed deltas (`{"L17": ...}`).
2. **The document is built by code, once.** No LLM writes the final JSON.
3. **Structure is unfalsifiable.** Counting, packing, merging, numbering, totals — all code, all unit-tested, never retried.
4. **Every prompt is bounded.** Batch sizes are derived from a character budget, never from "hope".
5. **Every LLM boundary has: schema validation → semantic validation → targeted repair → deterministic fallback.** The pipeline always terminates with a valid outline.
6. **Provider-agnostic by construction.** One `LLMClient` interface, Pydantic schemas as the only contract, vendor-neutral prompts.
7. **Short IDs in prompts, URNs in code.** The LLM never sees a URN.

## A3. Architecture diagrams

### A3.1 Layered architecture

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ ENTRY POINTS                                                                    │
│   CLI (MVP)      FastAPI /v1/outline/generate (prod)      Berlin node adapters  │
├────────────────────────────────────────────────────────────────────────────────┤
│ ORCHESTRATION — LangGraph StateGraph (graph.py)                                 │
│   • nodes are plain async functions  • Send() fan-out  • reducers fan-in        │
│   • conditional edges for validate→repair  • checkpointer (memory → Postgres)   │
├──────────────────────────────┬─────────────────────────────────────────────────┤
│ LLM NODES  (nodes/*.py)      │ DETERMINISTIC CORE  (rules/, assemble/, validate/)│
│   annotate                   │   blooms.py      verb → tier lookup              │
│   normalise_skills           │   estimates.py   grade × tier → words/minutes    │
│   plan_parts                 │   packing.py     bin-pack LOs into chapters      │
│   plan_chapters              │   merging.py     min-4 rule + 2-part exception   │
│   generate_titles            │   naming.py      merge/uniquify names            │
│   repair                     │   dcim.py        DCIM JSON builder               │
│                              │   assessments.py lesson-type → assessment        │
│   uses ──► llm/client.py     │   pacing.py      lesson-day tolerance            │
│            prompts/*.md      │   invariants.py  7 final checks                  │
├──────────────────────────────┴─────────────────────────────────────────────────┤
│ STATE  (state.py)  — TypedDict + reducers; single ID-keyed copy of all LO data  │
├────────────────────────────────────────────────────────────────────────────────┤
│ INFRA  — config.py (yaml+env)  logging  metrics  checkpointer  secrets          │
└────────────────────────────────────────────────────────────────────────────────┘
```

### A3.2 Graph topology

```
                                 ┌──────────────┐
                                 │  __start__   │
                                 └──────┬───────┘
                                        ▼
                    ┌───────────────────────────────────────┐
                    │ ingest                          [code] │
                    │  • validate input (Pydantic)           │
                    │  • mint ids L1..Ln ↔ URN               │
                    │  • normalise grade band                │
                    │  • lesson-day + word-limit math        │
                    │  • compute batch plan                  │
                    └───────────────────┬───────────────────┘
                                        │ Send() × ⌈n / batch⌉
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
  │ annotate [LLM] b=1   │  │ annotate [LLM] b=2   │  │ annotate [LLM] b=k   │
  │ in : [{id,text}]     │  │                      │  │                      │
  │ out: [{id,verb,skill}]│ │                      │  │                      │
  └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘
             └──────────────────────────┼──────────────────────────┘
                                        ▼  reducer: los[id] ← verb, skill
                    ┌───────────────────────────────────────┐
                    │ tier_lookup                     [code] │  blooms_level = TABLE[verb]
                    └───────────────────┬───────────────────┘
                                        ▼
                    ┌───────────────────────────────────────┐
                    │ normalise_skills                [LLM] │  unique skills → canonical
                    │ in : [{skill, count}]  (≤ ~100)        │  (skipped if ≤ 8 skills)
                    │ out: [{raw, canonical}]                │
                    └───────────────────┬───────────────────┘
                                        ▼
                    ┌───────────────────────────────────────┐
                    │ plan_parts                      [LLM] │  ONE compact global call
                    │ in : course meta + [{id,skill,tier}]   │  prompt chosen by
                    │ out: parts[{part_id,name,order,        │  progression type
                    │            complexity, lo_ids[]}]      │
                    └───────────────────┬───────────────────┘
                                        │ Send() × parts
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
  │ plan_chapters P1[LLM]│  │ plan_chapters P2[LLM]│  │ plan_chapters Pm[LLM]│
  │ in : skeleton summary│  │                      │  │                      │
  │      + part's LOs    │  │                      │  │                      │
  │ out: [{id,chapter,   │  │                      │  │                      │
  │       order_rank}]   │  │                      │  │                      │
  └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘
             └──────────────────────────┼──────────────────────────┘
                                        ▼
                    ┌───────────────────────────────────────┐
                    │ pack_and_merge                  [code] │  estimates → bin-pack →
                    │ (existing service logic, imported)     │  min-4 merge → uniquify →
                    │ out: packed.parts[].chapters[].stubs[] │  number → coverage check
                    └───────────────────┬───────────────────┘
                                        │ Send() × packed parts
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
  │ generate_titles [LLM]│  │ generate_titles [LLM]│  │ generate_titles [LLM]│
  │ in : part stubs      │  │                      │  │                      │
  │ out: {id: title}     │  │                      │  │                      │
  └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘
             └──────────────────────────┼──────────────────────────┘
                                        ▼
                    ┌───────────────────────────────────────┐
                    │ assemble                        [code] │  Overview part, content
                    │                                        │  parts w/ structural
                    │ out: outline (DCIM JSON)               │  chapters, semesters,
                    └───────────────────┬───────────────────┘  assessments, totals,
                                        ▼                      pacing
                    ┌───────────────────────────────────────┐
                    │ validate                        [code] │  7 invariants
                    └──────┬──────────────────┬─────────────┘
                     valid │                  │ title defects & attempts < 2
                           ▼                  ▼
                    ┌────────────┐   ┌───────────────────────┐
                    │  __end__   │   │ repair          [LLM] │  only failing ids
                    └────────────┘   └───────────┬───────────┘
                                                 └───────► assemble
                           (attempts == 2 → fallback_titles [code] → assemble)
```

### A3.3 Sequence diagram (300 LOs)

```
 CLI            Graph            LLM provider              Deterministic core
  │  invoke()     │                    │                            │
  ├──────────────►│  ingest            │                            │
  │               ├────────────────────┼───────────────────────────►│ ids, budget, batches
  │               │  annotate ×10 ∥    │                            │
  │               ├───────────────────►│ (10 calls, ~2k tok each)   │
  │               │◄───────────────────┤ {id: verb, skill}          │
  │               ├────────────────────┼───────────────────────────►│ verb → tier
  │               │  normalise_skills  │                            │
  │               ├───────────────────►│ (1 call, ~1k tok)          │
  │               │  plan_parts        │                            │
  │               ├───────────────────►│ (1 call, ~6.5k tok)        │
  │               │◄───────────────────┤ 9 parts, id→part           │
  │               │  plan_chapters ×9 ∥│                            │
  │               ├───────────────────►│ (9 calls, ~3k tok each)    │
  │               ├────────────────────┼───────────────────────────►│ pack_and_merge
  │               │◄───────────────────┼────────────────────────────┤ 8 parts (1 merge)
  │               │  generate_titles ×8∥                            │
  │               ├───────────────────►│ (8 calls, ~3k tok each)    │
  │               ├────────────────────┼───────────────────────────►│ assemble → validate
  │◄──────────────┤  outline.json + report.json                     │
```

## A4. Data-flow diagram (what each node reads/writes)

```
 STATE KEY        ingest annotate tier norm plan_parts plan_ch pack titles assemble validate repair
 ─────────────── ────── ──────── ──── ──── ────────── ─────── ──── ────── ──────── ──────── ──────
 course             W      R                   R         R      R           R
 budget             W                                           R           R        R
 batches            W      R
 los[*].text        W      R                             R             R
 los[*].verb               W      R                                    R
 los[*].raw_skill          W           R
 los[*].primary_skill             W    W       R         R      R      R
 los[*].blooms_level              W            R         R      R      R
 los[*].part_id                                W         R      R
 los[*].chapter_name                                     W      R
 los[*].order_rank                                       W      R
 skill_map                             W
 parts_plan                                    W         R      R
 packed                                                         W      R      R        R
 titles                                                                W      R        R       W
 outline                                                                      W        R
 validation                                                                            W       R
 repair_attempts                                                                       W       R
 metrics                   A           A       A         A             A                       A
 (W = writes, R = reads, A = appends via reducer)
```

---

# Part B — Environment and Repository Setup

## B1. Toolchain

| Tool | Version | Why |
|---|---|---|
| Python | 3.11+ | `TypedDict` generics, `asyncio.TaskGroup`, performance |
| Package manager | `uv` (or Poetry) | Lockfile, fast installs |
| Formatter/linter | `ruff` | Format + lint in one |
| Type checker | `mypy --strict` (or `pyright`) | Contracts are types |
| Tests | `pytest`, `pytest-asyncio`, `pytest-cov` | |
| Pre-commit | `pre-commit` | ruff, mypy, trailing whitespace |

## B2. Dependencies

```toml
[project]
name = "outline"
requires-python = ">=3.11"
dependencies = [
  "langgraph>=0.2",
  "langchain-core>=0.3",
  "langchain>=0.3",              # init_chat_model
  "langchain-anthropic>=0.3",
  "langchain-openai>=0.3",
  "langchain-aws>=0.2",          # ChatBedrockConverse
  "pydantic>=2.7",
  "pydantic-settings>=2.3",
  "pyyaml>=6",
  "typer>=0.12",                 # CLI
  "rich>=13",                    # progress/tables
  "tenacity>=8",                 # transport retries
  "structlog>=24",               # structured logs
]
[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio", "pytest-cov", "ruff", "mypy", "pre-commit", "respx"]
prod = ["fastapi", "uvicorn[standard]", "langgraph-checkpoint-postgres", "psycopg[binary,pool]", "opentelemetry-sdk", "boto3"]
```

## B3. Environment variables

```
OUTLINE_PROVIDER=anthropic            # anthropic | openai | bedrock
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
AWS_REGION=us-east-1                  # bedrock
AWS_PROFILE=...                       # or role-based in prod
OUTLINE_CONFIG=config/default.yaml
LANGSMITH_TRACING=false               # optional tracing
```

Never read keys anywhere except `config.py`. Nodes receive an `LLMClient`, not credentials.

## B4. Repository layout

```
outline-generator/
├── pyproject.toml
├── README.md
├── config/
│   ├── default.yaml
│   └── providers/{anthropic,openai,bedrock}.yaml
├── src/outline/
│   ├── __init__.py
│   ├── __main__.py            # typer CLI
│   ├── config.py              # Settings (pydantic-settings) + yaml merge
│   ├── state.py               # OutlineState, LO, reducers
│   ├── schemas/
│   │   ├── input.py           # CourseRequest
│   │   ├── llm.py             # AnnotateOut, SkillMapOut, PartsPlanOut, ChaptersOut, TitlesOut, RepairOut
│   │   └── dcim.py            # DCIM output models (Project/Part/Chapter/Module)
│   ├── graph.py               # build_graph()
│   ├── nodes/
│   │   ├── ingest.py  annotate.py  tier_lookup.py  normalise_skills.py
│   │   ├── plan_parts.py  plan_chapters.py  pack_and_merge.py
│   │   ├── generate_titles.py  assemble.py  validate.py  repair.py
│   ├── rules/
│   │   ├── blooms.py  estimates.py  packing.py  merging.py  naming.py  grade_band.py
│   ├── assemble/
│   │   ├── dcim.py  assessments.py  pacing.py
│   ├── validate/
│   │   └── invariants.py
│   ├── llm/
│   │   ├── client.py          # LLMClient protocol + LangChainClient
│   │   ├── providers.py       # factory per provider
│   │   ├── budget.py          # char→token estimates, batch sizing
│   │   └── fake.py            # deterministic FakeLLM for tests
│   ├── prompts/
│   │   ├── annotate.md  normalise_skills.md
│   │   ├── plan_parts/{skills_based,theme_based,chronological,standards_driven}.md
│   │   ├── plan_chapters.md  titles.md  repair_titles.md
│   └── reporting.py           # report.json writer
├── tests/
│   ├── unit/                  # rules, assemble, validate, budget
│   ├── graph/                 # end-to-end with FakeLLM
│   ├── live/                  # @pytest.mark.live, real provider smoke
│   └── fixtures/              # sample-input-43/49/94/123.json, synthetic-300.json, golden outputs
├── scripts/
│   ├── make_synthetic.py      # concatenates fixtures, re-mints URNs
│   └── compare_runs.py        # diff two report.json files
└── docs/
```

---

# Part C — Data Contracts

## C1. Input (`schemas/input.py`)

```python
class LearningObjectiveIn(BaseModel):
    learning_objective_urn: str = Field(min_length=1)
    objective: str = Field(min_length=1)

class CourseRequest(BaseModel):
    course_title: str
    grade_band: str                       # "K-2" | "3-5" | "MS" | "HS" | raw ("Grade 6")
    subject_area: str
    minutes_per_lesson: int = Field(gt=0)
    lessons_per_week: int = Field(gt=0, le=7)
    course_duration_weeks: int = Field(gt=0)
    course_outline_progression: Literal[
        "SKILLS_BASED_PROGRESSION", "THEME_BASED_PROGRESSION",
        "CHRONOLOGICAL_PROGRESSION", "STANDARDS_DRIVEN_PROGRESSION"]
    learning_objectives: list[LearningObjectiveIn] = Field(min_length=1)
    user_prompt: str | None = None
    effort: EffortConfig | None = None    # overall/grading/teaching 1–5, passthrough
    PearsonExtSSOSession: str | None = None
```

## C2. State (`state.py`)

```python
class LO(TypedDict, total=False):
    id: str; urn: str; text: str; input_index: int
    verb: str; raw_skill: str; primary_skill: str; blooms_level: str
    part_id: str; chapter_name: str; order_rank: int
    module_title: str
    flags: list[str]

def merge_los(left: dict[str, LO], right: dict[str, LO]) -> dict[str, LO]:
    out = {**left}
    for k, patch in right.items():
        out[k] = {**out.get(k, {}), **patch}
    return out

class OutlineState(TypedDict, total=False):
    course: CourseMeta
    budget: Budget                      # total_lesson_days, total_course_hours, word_limit, minutes_per_lesson
    batches: list[list[str]]
    los: Annotated[dict[str, LO], merge_los]
    skill_map: dict[str, str]
    parts_plan: list[PartPlan]
    packed: dict | None
    titles: Annotated[dict[str, str], lambda a, b: {**a, **b}]
    outline: dict | None
    validation: dict | None
    repair_attempts: int
    metrics: Annotated[list[dict], operator.add]
    errors: Annotated[list[dict], operator.add]
```

Rule: **nodes return partial dicts**; reducers merge. A node never mutates `state` in place.

## C3. LLM output schemas (`schemas/llm.py`)

```python
class AnnotatedItem(BaseModel):
    id: str; verb: str = Field(min_length=1); primary_skill: str = Field(min_length=2, max_length=60)
class AnnotateOut(BaseModel):
    items: list[AnnotatedItem]

class SkillAlias(BaseModel): raw: str; canonical: str
class SkillMapOut(BaseModel): aliases: list[SkillAlias]

class PartPlanItem(BaseModel):
    part_id: str; part_name: str = Field(max_length=80); order: int
    part_domain_complexity: Literal["Foundational","Intermediate","Advanced"]
    lo_ids: list[str] = Field(min_length=1)
class PartsPlanOut(BaseModel):
    parts: list[PartPlanItem] = Field(min_length=1); planning_notes: str | None = None

class ChapterAssignment(BaseModel): id: str; chapter_name: str; order_rank: int = Field(ge=1)
class ChaptersOut(BaseModel): assignments: list[ChapterAssignment]

class TitleItem(BaseModel): id: str; title: str = Field(min_length=3, max_length=80)
class TitlesOut(BaseModel):
    modules: list[TitleItem]; chapters: list[TitleItem] = []
```

## C4. DCIM output (`schemas/dcim.py`) — must match `tool-response-43-lg-new.txt`

```
Project
  course_title, grade_band, subject_area, chapter_word_count_limit
  total_parts, total_chapters, title{en}, label="project"
  total_lesson_days, total_chapters_in_course
  pacing_overrun, pacing_overrun_lesson_days, split_notes
  unassigned_objective_urns[]
  children[]: Part
    label="part", type ∈ {overview, understand, semester}, part_number, title{en}
    children[]: Chapter
      label="chapter", type ∈ {overview, introduction, understand, apply, review, test,
                               semester_review, semester_exam}
      chapter_number, title{en}, chapter_estimated_word_count|null, chapter_estimated_time_minutes
      assessment (optional, new): {type, scoring, delivery} | null
      children[]: Module
        label="module", type ∈ {course_guide, overview_introduction, introduction, understand,
                                apply, review, semester_review}
        module_number, title{en}, learning_objective_urn|null,
        estimated_word_count|null, estimated_time_minutes|null, primary_skill|null, blooms_level|null
```

Counting rules: `total_parts = 1 + content_parts + 2`; `total_chapters = 1 + content_chapters + 4·content_parts + 4`.

## C5. Report (`report.json`)

```json
{
  "run_id": "…", "provider": "anthropic", "n_los": 300,
  "calls": [{"node": "annotate", "batch": 3, "model": "…", "prompt_tokens": 1980, "completion_tokens": 410, "latency_ms": 2100, "attempt": 1}],
  "totals": {"prompt_tokens": 38120, "completion_tokens": 8033, "llm_calls": 30, "wall_ms": 71000},
  "enforcement_log": "…", "fallbacks": [], "invariants": {"lo_coverage": true, "...": true},
  "pacing": {"total_lesson_days": 180, "total_chapters": 121, "overrun": false}
}
```

---

# Part D — Step-by-Step Build (12 phases)

Each phase: **Goal → Files → How → Tests → Done when**. Build in this order; each phase is runnable/testable on its own.

## Phase 0 — Scaffold

- **Files:** `pyproject.toml`, `src/outline/__init__.py`, `config/default.yaml`, `.pre-commit-config.yaml`, `tests/conftest.py`.
- **How:** `uv init`, add deps, `ruff` + `mypy` config, copy the four sample inputs into `tests/fixtures/`.
- **Done when:** `uv run pytest` passes with one placeholder test; `pre-commit run --all-files` clean.

## Phase 1 — Config and settings

- **Files:** `config.py`, `config/default.yaml`.
- **How:** `pydantic-settings` `Settings` class; load yaml, overlay env vars. Fields: provider, per-role models, batching (`annotate_batch_size`, `max_prompt_chars`, `max_concurrency`), retries, timeouts.

```yaml
provider: anthropic
models: {default: claude-sonnet-4-5, annotate: claude-haiku-4-5, titles: claude-haiku-4-5}
batching: {annotate_batch_size: 30, max_prompt_chars: 32000, max_concurrency: 5}
retries: {schema: 1, semantic: 2, transport: 3}
timeouts: {llm_seconds: 90}
rules: {min_understand_chapters: 4, max_los_per_chapter: 4, pacing_tolerance: 0.05}
```

- **Tests:** yaml + env override precedence.

## Phase 2 — Schemas and state

- **Files:** `schemas/input.py`, `schemas/llm.py`, `schemas/dcim.py`, `state.py`.
- **How:** Transcribe Part C. For `dcim.py` build models from the real output in `tool-response-43-lg-new.txt` and add a test that parses that file's JSON payload successfully (extract the `content` chunks, join, `json.loads`).
- **Done when:** golden DCIM output round-trips through `Project.model_validate`.

## Phase 3 — Deterministic rules (port existing service)

- **Files:** `rules/grade_band.py`, `rules/blooms.py`, `rules/estimates.py`, `rules/packing.py`, `rules/merging.py`, `rules/naming.py`.
- **How:**
  - `grade_band.normalize()` ← `_normalize_grade_band`.
  - `blooms.py`: build `VERB_TIER: dict[str, str]` from the three verb lists in `LearningObjectiveAnalyser.md`; **lowest tier wins** on duplicates; `tier_for(verb) -> str` lower-cases, strips, falls back to `"Foundational"`. Handle multi-word verbs (`"figure out"`, `"back up"`).
  - `estimates.py` ← `_estimate_time_minutes`, `_estimate_word_count`, tables `GRADE_WORD_LIMITS`, `GRADE_WORD_RANGES`, `BLOOMS_TIME_RANGES`.
  - `packing.py` ← `_pack_los_into_chapters`, `_chapter_base_name`, `_assign_module_numbers`.
  - `merging.py` ← `_get_best_adjacent`, `_merge_parts`, `_enforce_minimum_4` (returns `(parts, log_lines)`; keep the exact exception semantics: only when `len(parts)==2` and combined `< 4`).
  - `naming.py` ← `_merge_part_names`, `_build_chapter_differentiator`, `_uniquify_chapter_names`.
  - Pure functions, plain dicts/dataclasses, no Pydantic inside rules (speed + testability).
- **Tests (unit, exhaustive):** the 7-row test matrix from `Implementation_Guide_Deterministic_Packing.md` §9; property test: for random inputs, output URN multiset == input URN multiset; all parts ≥ 4 or exception logged; chapter words ≤ limit; chapter minutes ≤ limit.
- **Done when:** 100 % branch coverage on `rules/`.

## Phase 4 — LLM client (provider-agnostic)

- **Files:** `llm/client.py`, `llm/providers.py`, `llm/budget.py`, `llm/fake.py`.
- **How:**

```python
class CallMetric(BaseModel):
    node: str; model: str; prompt_tokens: int; completion_tokens: int; latency_ms: int; attempt: int

class LLMClient(Protocol):
    async def structured(self, *, role: str, system: str, user: str,
                         schema: type[T]) -> tuple[T, CallMetric]: ...

class LangChainClient:
    def __init__(self, settings: Settings):
        self._models = {role: init_chat_model(f"{settings.provider}:{name}", temperature=0,
                                              timeout=settings.timeouts.llm_seconds)
                        for role, name in settings.models.items()}
    async def structured(self, *, role, system, user, schema):
        model = self._models.get(role, self._models["default"])
        runnable = model.with_structured_output(schema, include_raw=True)
        # tenacity: retry on RateLimit/5xx/timeout with exp backoff (transport retries)
        # on ValidationError: one corrective retry appending the error text (schema retry)
        ...
        return parsed, CallMetric(...)
```

  - `providers.py`: map `bedrock` → `bedrock_converse:` prefix + model-id table; `openai` → `openai:`; `anthropic` → `anthropic:`. Detect structured-output capability; for models lacking it, use `method="json_mode"` or plain text + `schema.model_validate_json` with fence stripping.
  - `budget.py`: `estimate_tokens(text) = len(text)//4`; `plan_batches(items, per_item_chars, max_prompt_chars, overhead_chars)`.
  - `fake.py`: `FakeLLM` that answers from rules (e.g. verb = first word, skill = first two nouns, parts by skill hash) so graph tests are deterministic and offline. Also supports scripted failures (`fail_once_on="plan_parts"`) to test repair paths.
- **Tests:** unit for budget; `FakeLLM` used everywhere else; `tests/live` marked and skipped by default.
- **Done when:** `structured()` works against one real provider on a 3-item prompt.

## Phase 5 — Prompt templates

- **Files:** `prompts/*.md`. Load via `importlib.resources`; render with `str.format_map` or Jinja2 (no logic in templates beyond variable substitution).
- **How:** Write per Part E. Each file has front-matter comment: purpose, inputs, output schema name, size limits.
- **Tests:** every template renders with a fixture context; no unresolved `{placeholders}`.

## Phase 6 — Nodes 1–4 (ingest, annotate, tier_lookup, normalise_skills)

- **Files:** `nodes/ingest.py`, `nodes/annotate.py`, `nodes/tier_lookup.py`, `nodes/normalise_skills.py`.
- **How:**

```python
# ingest
def ingest(state: OutlineState, config: RunnableConfig) -> dict:
    req = CourseRequest.model_validate(state["raw_input"])
    los = {f"L{i+1}": LO(id=f"L{i+1}", urn=lo.learning_objective_urn, text=lo.objective,
                         input_index=i, flags=[]) for i, lo in enumerate(req.learning_objectives)}
    band = normalize(req.grade_band)
    budget = Budget(total_lesson_days=req.lessons_per_week * req.course_duration_weeks,
                    total_course_hours=..., word_limit=GRADE_WORD_LIMITS[band],
                    minutes_per_lesson=req.minutes_per_lesson)
    batches = plan_batches(list(los), per_item_chars=avg_len+40, max_prompt_chars=settings.batching.max_prompt_chars, overhead_chars=len(ANNOTATE_PROMPT))
    return {"course": ..., "budget": budget, "los": los, "batches": batches, "repair_attempts": 0}

# fan-out edge
def fan_out_annotate(state) -> list[Send]:
    return [Send("annotate", {"batch_ids": ids, "los": {i: state["los"][i] for i in ids}, "course": state["course"]})
            for ids in state["batches"]]

# annotate (receives only its slice)
async def annotate(payload: dict, config) -> dict:
    items = [{"id": i, "text": payload["los"][i]["text"]} for i in payload["batch_ids"]]
    out, metric = await llm.structured(role="annotate", system=ANNOTATE_SYS, user=render(items), schema=AnnotateOut)
    got = {x.id: x for x in out.items if x.id in payload["batch_ids"]}
    missing = [i for i in payload["batch_ids"] if i not in got]
    if missing:  # targeted repair once
        out2, m2 = await llm.structured(..., user=render([...missing...]), schema=AnnotateOut)
        ...
    patches = {i: {"verb": got[i].verb, "raw_skill": got[i].primary_skill} for i in got}
    for i in still_missing: patches[i] = fallback_annotation(payload["los"][i]["text"]) | {"flags": ["annotated_by_fallback"]}
    return {"los": patches, "metrics": [metric.model_dump(), ...]}
```

  - `tier_lookup`: pure map over `los` → `blooms_level`.
  - `normalise_skills`: collect `Counter(raw_skill)`; if ≤ 8 unique → identity map; else one call; apply map → `primary_skill`; unknown keys ignored.
- **Tests (graph with FakeLLM):** 43-LO fixture → all LOs have verb/skill/tier; forced missing ids → repair path → fallback flagged.

## Phase 7 — Nodes 5–6 (plan_parts, plan_chapters)

- **How:**
  - `plan_parts`: build compact projection sorted by `input_index`: `L1 | Logical Arguments | Intermediate`. Choose template by progression type. Post-validate: set of ids == all ids; duplicates → keep first occurrence; missing → repair call *with the existing part list* (“place these ids”); after `retries.semantic` → fallback: part whose members share `primary_skill`, else last part. Renumber `order` 1..m. Write `parts_plan` and `los[id].part_id`.
  - `plan_chapters` fan-out via `Send("plan_chapters", {"part": p, "los": slice, "skeleton": names})`. Post-validate coverage within the part; fallback: group by `primary_skill`, `order_rank` by tier then `input_index`. Write `chapter_name`, `order_rank`.
- **Tests:** coverage invariants under FakeLLM; scripted drop of 5 ids triggers repair; scripted double failure triggers fallback and flags.

## Phase 8 — Node 7 (pack_and_merge)

- **How:** Build the old `GroupingPlan`/`AnnotatedObjectivesPayload` equivalents from state (plain dicts), call `rules.*` in the same order as the existing `pack_and_merge_course_outline_structure`. Output `packed = {parts, enforcement_log, validation, content_chapter_count, num_content_parts, total_chapter_count}`. If `validation.valid is False` → raise `PipelineBug` (never retry).
- **Tests:** feed the 43-LO real planner output (extract from `llmlogs-43-lgs-new.json` tool-call args) → identical `parts` to the real tool response.

## Phase 9 — Node 8 (generate_titles) and Node 9 (assemble)

- **generate_titles:** fan-out per packed part; prompt lists chapters and stubs with short ids; validate distinctness within chapter (`casefold`), banned regex `(?i)\b(continued|part\s*(2|3|ii|iii)|module\s*\d+|activity|practice)\b`, title ≠ chapter name; repair failing ids; fallback `f"{skill}: {verb.title()}"`.
- **assemble (`assemble/dcim.py`):**

```python
def build_project(course, budget, packed, titles, settings) -> dict:
    parts = [overview_part(course, budget)]
    for p in packed["parts"]:
        chapters = [intro_chapter(p, budget)]
        for ch in p["chapters"]:
            chapters.append(understand_chapter(ch, titles, budget))
        chapters += [apply_chapter(p, budget), review_chapter(p, budget), test_chapter(p, budget)]
        parts.append(content_part(p, chapters))
    parts += [semester_part(course, "A", budget), semester_part(course, "B", budget)]
    renumber(parts)                                   # part_number, chapter_number, module_number
    attach_assessments(parts)                         # assessments.py table
    totals = compute_totals(parts)                    # total_parts, total_chapters
    pacing = pacing_report(totals, budget, settings)  # pacing.py
    return {..., "children": parts, **totals, **pacing, "unassigned_objective_urns": []}
```

  - `assessments.py`: `{"understand": QuickCheck(auto, mcq), "apply": SampleWork(teacher, dropbox), "review": UnitOnlinePractice(auto), "test": UnitTest(auto+teacher), "semester_review": SemesterOnlinePractice(auto), "semester_exam": SemesterExam(auto)}`.
  - `pacing.py`: `tol = round(days*0.05)`; overrun if `total_chapters > days + tol`; notes string.
- **Tests:** assemble from the real 43-LO packed output + real titles → **equals golden** DCIM JSON (ignore `assessment` field). Unit tests for totals formula and pacing edges.

## Phase 10 — Node 10 (validate) and Node 11 (repair)

- **validate (`validate/invariants.py`):** returns `{"valid": bool, "failures": [{"code": "TITLE_DUPLICATE", "ids": [...]}, ...]}`. Codes: `LO_COVERAGE`, `MIN4`, `SEMESTERS`, `ORDER`, `SUMS_TOTALS`, `TITLES`, `SCHEMA`.
- **Routing:**

```python
def route_after_validate(state) -> str:
    v = state["validation"]
    if v["valid"]: return END
    codes = {f["code"] for f in v["failures"]}
    if codes <= {"TITLES"} and state["repair_attempts"] < settings.retries.semantic: return "repair"
    if codes <= {"TITLES"}: return "fallback_titles"
    raise PipelineBug(v)          # structural failure = bug
```

- **repair:** prompt with only failing ids + their chapter context; merge into `titles`; `repair_attempts += 1` → `assemble`.
- **Tests:** scripted duplicate titles → repair → valid; scripted persistent duplicates → fallback → valid.

## Phase 11 — Graph wiring, CLI, reporting

- **graph.py:**

```python
def build_graph(llm: LLMClient, settings: Settings, checkpointer=None):
    g = StateGraph(OutlineState)
    for name, fn in NODES.items(): g.add_node(name, fn)
    g.add_edge(START, "ingest")
    g.add_conditional_edges("ingest", fan_out_annotate, ["annotate"])
    g.add_edge("annotate", "tier_lookup")
    g.add_edge("tier_lookup", "normalise_skills")
    g.add_edge("normalise_skills", "plan_parts")
    g.add_conditional_edges("plan_parts", fan_out_chapters, ["plan_chapters"])
    g.add_edge("plan_chapters", "pack_and_merge")
    g.add_conditional_edges("pack_and_merge", fan_out_titles, ["generate_titles"])
    g.add_edge("generate_titles", "assemble")
    g.add_edge("assemble", "validate")
    g.add_conditional_edges("validate", route_after_validate, {END: END, "repair": "repair", "fallback_titles": "fallback_titles"})
    g.add_edge("repair", "assemble"); g.add_edge("fallback_titles", "assemble")
    return g.compile(checkpointer=checkpointer)
```

  - Inject `llm` and `settings` via `functools.partial` or `config["configurable"]`; never globals.
  - `max_concurrency` via `RunnableConfig(max_concurrency=settings.batching.max_concurrency)`.
- **CLI (`__main__.py`):** `outline generate INPUT --provider X --out DIR [--model-override role=name] [--stream]`; streams `graph.astream(..., stream_mode="updates")` to a `rich` progress table; writes `outline.json`, `report.json`, `enforcement.log`.
- **reporting.py:** aggregates `metrics`, `fallbacks` (from `los[*].flags`), invariants, pacing.
- **Done when:** 43 / 94 / 123 / synthetic-300 all produce valid outlines with FakeLLM and with one live provider.

## Phase 12 — Evaluation harness and demo

- `scripts/make_synthetic.py`: concatenates fixtures, re-mints URNs (`uuid5`), scales `course_duration_weeks`.
- `scripts/compare_runs.py`: prints table of per-node token maxima and totals across runs; asserts "max single prompt < 10k tokens" and "completion tokens per LO < 40".
- Demo order: 43 → 94 → 300 → `--provider openai` on 43 → open report.

---

# Part E — Prompt Engineering Guide

General rules for every template:

- **System message:** role, hard rules, output schema description (the schema is *also* enforced by structured output — prose is a hint).
- **User message:** only the projection for this call, as a compact table (`id | field | field`), never JSON blobs of the whole state.
- **IDs are opaque tokens.** Say: "Return each `id` exactly as given. Do not invent ids."
- **No transport instructions** (no "escape quotes", no "wrap in fences") — the client handles it.
- **No counting instructions.** Never ask the model to verify counts; code does that.
- **Keep ≤ 800 tokens of instructions** per template; long rule lists dilute attention.

| Template | Role sentence | Inputs | Output schema | Key rules |
|---|---|---|---|---|
| `annotate.md` | "You extract the action verb and the primary skill noun phrase from K-12 learning objectives." | `id \| objective` rows | `AnnotateOut` | verb = first student-action verb, lowercase, base form; skill = 2–4 word Title Case noun phrase from the object of the verb; same skill name for same competency |
| `normalise_skills.md` | "You merge near-duplicate skill names into one canonical name each." | `skill \| count` rows | `SkillMapOut` | only merge true synonyms/plural/word-order variants; canonical = most frequent form; never invent new skills |
| `plan_parts/skills_based.md` | "You group learning objectives into coherent skill-domain units and order them foundational → advanced." | course meta, `id \| skill \| tier` rows, `user_prompt` | `PartsPlanOut` | 4–8 chapter groups per part *as guidance*; part names ≤ 6 words, noun phrases, non-generic; every id exactly once; do not worry about minimum sizes (downstream merges) |
| `plan_parts/theme_based.md` | "…by theme or big idea…" | same | same | group by conceptual theme; ordering by narrative arc |
| `plan_parts/chronological.md` | "…in historical/chronological sequence…" | same | same | detect period/date cues in skill/text; order by time |
| `plan_parts/standards_driven.md` | "…in the exact order standards appear…" | same + standard codes if present | same | preserve input order as framework order; parts = contiguous runs |
| `plan_chapters.md` | "Within one unit, group objectives into lesson-sized chapters and order them." | skeleton names, this part's `id \| objective \| skill \| tier` | `ChaptersOut` | ~3 LOs per chapter, 2 for deep/advanced; chapter names 2–4 word Title Case noun phrases, unique within part; `order_rank` Foundational < Intermediate < Advanced then prerequisites |
| `titles.md` | "Write a specific 2–5 word noun-phrase title for each module from its objective." | chapters with `id \| objective \| skill` stubs | `TitlesOut` | distinct within chapter; not the chapter title; no generic labels or "Part 2/Continued"; optionally improve chapter names containing "and Related Concepts" |
| `repair_titles.md` | "Some titles violate rules; provide replacements for only these ids." | failing ids with reason + sibling titles | `TitlesOut` | must differ from all listed sibling titles |

Example `plan_chapters.md` body:

```
You are planning one unit of a K-12 {subject_area} course for grade band {grade_band}.
Unit: "{part_name}" (unit {order} of {n_parts}). Other units, for context only: {other_unit_names}.
{user_prompt_block}

Group the objectives below into lesson-sized chapters and order them.
Rules:
- Aim for about 3 objectives per chapter; use 2 for deep or Advanced objectives.
- Chapter names: 2–4 word Title Case noun phrases, unique within this unit, no generic labels.
- order_rank: Foundational before Intermediate before Advanced; within a tier, prerequisites first.
- Assign every id exactly once. Return ids exactly as given.

id | objective | skill | tier
{rows}
```

---

# Part F — Coding Conventions ("Styling")

| Area | Convention |
|---|---|
| Node signature | `async def node(state: OutlineState, config: RunnableConfig) -> dict` — returns partial state only |
| Fan-out payloads | Small dicts containing only the slice needed; never the whole `state` |
| Purity | `rules/`, `assemble/`, `validate/` are pure functions, no I/O, no logging beyond `structlog.debug` |
| Types | `mypy --strict`; `TypedDict` for state, Pydantic for boundaries (input, LLM, output) |
| Errors | `PipelineBug` (structural invariant violated — never retry), `LLMTransportError` (retry w/ backoff), `LLMSchemaError` (one corrective retry). Nodes never swallow exceptions silently; fallbacks are logged and flagged |
| Logging | `structlog`, JSON in prod, keys: `run_id`, `node`, `batch`, `attempt`, `prompt_tokens`, `completion_tokens`, `latency_ms` |
| Prompts | Markdown files, versioned; template variables in `{snake_case}`; changelog line at top |
| Naming | Nodes = verbs (`annotate`, `plan_parts`); schemas = `XxxOut`; rules = nouns (`packing`, `merging`) |
| Tests | One test module per source module; graph tests use `FakeLLM`; live tests behind `-m live` |
| Determinism | `temperature=0`; sort everything (`input_index`, `order_rank`) before use; never rely on dict order from the LLM |
| Docs | Every node file starts with a docstring: purpose, reads, writes, LLM calls, failure policy |

---

# Part G — Testing and Evaluation

## G1. Pyramid

```
            ┌──────────────┐
            │  live smoke  │  1 provider × 43-LO fixture, nightly / on demand
            ├──────────────┤
            │  graph e2e   │  FakeLLM: 43, 94, 123, 300; failure-injection paths
            ├──────────────┤
            │  contract    │  golden DCIM JSON round-trip; assemble == golden
            ├──────────────┤
            │  unit        │  rules/, assemble/, validate/, budget/ — 100 % branches
            └──────────────┘
```

## G2. Property tests (Hypothesis) for `rules/`

- URN multiset preserved through pack + merge.
- All parts ≥ 4 chapters unless exactly-2-parts exception logged.
- No chapter exceeds word/time/density limits.
- Part order preserved (merged part sits at the earlier index).

## G3. Evaluation metrics (in `report.json`, tracked over time)

| Metric | Target |
|---|---|
| Valid outline rate | 100 % |
| Fallback usage rate (per LO) | < 1 % |
| Max single prompt tokens | < 10k |
| Completion tokens per LO | < 40 |
| Wall-clock @ 300 LOs | < 2 min |
| Title rule violations before repair | < 3 % |

Add a small **human-rubric sample**: 20 random module titles + 5 part names per run scored 1–5 by a curriculum reviewer; store in `eval/` for prompt regression.

---

# Part H — Production Architecture

## H1. Deployment topology

```
                    ┌─────────────────────┐
   Berlin / UI ───► │ API  (FastAPI)      │  POST /v1/outline/generate   → 202 {run_id}
                    │  auth: PearsonExt   │  GET  /v1/outline/{run_id}   → status / result
                    │  SSO header check   │  GET  /v1/outline/{run_id}/events (SSE progress)
                    └─────────┬───────────┘
                              │ enqueue (SQS / Redis)
                    ┌─────────▼───────────┐        ┌───────────────────────┐
                    │ Worker(s)           │◄──────►│ Postgres              │
                    │  LangGraph runtime  │        │  • langgraph checkpts │
                    │  max_concurrency=N  │        │  • runs, reports      │
                    └─────────┬───────────┘        └───────────────────────┘
                              │
              ┌───────────────┼─────────────────┐
              ▼               ▼                 ▼
        Anthropic API     OpenAI API        AWS Bedrock        (chosen by config / per-tenant)
                              │
                    ┌─────────▼───────────┐
                    │ Observability       │  OpenTelemetry traces (one span per node/call),
                    │ LangSmith optional  │  Prometheus metrics, structured logs → CloudWatch
                    └─────────────────────┘
```

## H2. Production checklist

| Concern | Decision |
|---|---|
| Execution model | Async job: API returns `run_id`; worker runs graph; client polls or subscribes to SSE. Generation takes 30–120 s — never block an HTTP request |
| Checkpointing | `PostgresSaver`; `thread_id = run_id`; resume on worker crash; retention 30 days |
| Idempotency | `Idempotency-Key` header → same `run_id`; nodes idempotent by design |
| Concurrency & rate limits | Per-provider semaphore (`max_concurrency`), token-bucket for TPM; queue depth alarm |
| Retries | Transport: 3× exp backoff + jitter; semantic: 2 targeted; structural: none (bug → alert) |
| Timeouts | Per LLM call 90 s; per run 10 min; worker visibility timeout > run timeout |
| Provider failover | Ordered provider list per role; on repeated 5xx/429 switch provider for the remainder of the run (schemas identical, so safe) |
| Cost control | Per-run token budget in state; abort + alert if exceeded; small models for `annotate`/`titles` |
| Caching | Cache `annotate` results by `hash(objective_text)` (LOs repeat across state courses — see STUDIOPE-568); cache prompt prefixes (provider prompt caching) |
| Secrets | AWS Secrets Manager / SSM; injected as env at runtime; never in config files |
| Auth | Validate `PearsonExtSSOSession` at API edge; workers trust the queue only |
| PII / data | LO text is curriculum, not PII, but tenant-isolate by `tenantId` in every log/trace/checkpoint key |
| Prompt injection | LO text goes only into user turn tables; ids opaque; structured output enforced; validators reject foreign ids |
| Observability | One trace per run, one span per node and per LLM call with token counts; dashboards: valid-rate, fallback-rate, p95 latency, cost/run |
| Prompt & model versioning | `prompt_version` + `model` recorded in `report.json`; golden eval run in CI on prompt change |
| Config per environment | `config/{dev,staging,prod}.yaml` overlaid on `default.yaml` |
| Packaging | Docker (python:3.11-slim, non-root, `uv sync --frozen`); ECS Fargate or Kubernetes; Lambda not recommended (10-min limit is tight, cold start + fan-out) |
| CI/CD | ruff → mypy → unit → graph(FakeLLM) → contract; nightly live smoke; canary deploy |
| Berlin integration | Option A: Berlin single Tool node calls `/v1/outline/generate` (recommended). Option B: expose each graph node as a Berlin REST tool and keep Berlin edges — only if the visual graph is a product requirement |
| Regeneration (future) | Node-level re-run keyed by `part_id` using the same checkpoint; undo = previous checkpoint version |

## H3. FastAPI surface (production)

```python
@app.post("/v1/outline/generate", status_code=202)
async def generate(req: CourseRequest, bg: BackgroundTasks, sso: str = Header(alias="PearsonExtSSOSession")):
    run_id = new_run_id(req)                       # idempotent hash or uuid
    await queue.enqueue(run_id, req.model_dump())
    return {"run_id": run_id, "status": "queued"}

@app.get("/v1/outline/{run_id}")
async def status(run_id: str): ...                 # queued | running{node,progress} | done{outline_url} | failed{error}
```

---

# Part I — Operations Runbook

| Symptom | Likely cause | Action |
|---|---|---|
| `PipelineBug: LO_COVERAGE` | Reducer or id-slicing bug | Structural → fix code; never retried by design. Inspect checkpoint `los` vs `packed` |
| Many `annotated_by_fallback` flags | Provider returning wrong ids / schema drift | Check `metrics[].attempt`, provider model version; tighten prompt row format |
| `plan_parts` repair every run | Projection too terse for subject | Add first 6 words of objective text to projection (config flag) |
| 429s, long wall-clock | `max_concurrency` too high for TPM | Lower concurrency; enable provider failover |
| Pacing overrun on most courses | Estimates table vs. real calendar | Product decision: tune `BLOOMS_TIME_RANGES` / `MAX_LOS_PER_CHAPTER`, not prompts |
| Titles violate rules after repair | Banned regex too strict / model weak | Review `report.fallbacks`; move `titles` role to stronger model |
| Bedrock schema errors | Model lacks native structured output | Client auto-falls back to JSON-text mode; verify `providers.py` capability table |

Debug commands: `outline generate … --stream --log-level debug`; `outline replay RUN_ID --from plan_chapters` (uses checkpoint).

---

# Part J — Completion Checklist

- [ ] Phase 0–2: scaffold, config, schemas; golden DCIM output parses
- [ ] Phase 3: rules ported, 100 % branch coverage, property tests green
- [ ] Phase 4: `LLMClient` works on Anthropic; `FakeLLM` deterministic
- [ ] Phase 5: all 8 templates render; ≤ 800 instruction tokens each
- [ ] Phase 6–7: annotate/tier/normalise/plan nodes with repair + fallback paths tested
- [ ] Phase 8: pack_and_merge reproduces real 43-LO tool response exactly
- [ ] Phase 9: assemble reproduces golden 43-LO DCIM JSON
- [ ] Phase 10: validate/repair routing tested incl. fallback
- [ ] Phase 11: CLI streams progress; `report.json` complete
- [ ] Phase 12: 43 / 94 / 123 / 300 valid on FakeLLM and one live provider; `--provider openai` run identical in structure
- [ ] Docs: README quickstart, this guide, spec linked
- [ ] Prod (later): FastAPI + queue + Postgres checkpointer, OTel, CI gates, canary
- [ ] Scale (Part K): tier selector, skill-level + domain planning, CCC + name registry, `OutlineStore`, synthetic 500/1000/2000 green

---

# Part K — Scaling to 500, 1,000, 2,000+ LOs and Large Outputs

> Requirement: the system must accept **any** number of learning objectives and manage the **full course context end to end**, with output size handled as carefully as input size. This part specifies the tiered planning design, the global-context carrier, and the large-output pipeline. Everything in Parts A–J still applies; Part K adds four nodes, one selector, and one storage abstraction.

## K1. Why the base graph already scales — and where it stops

Every per-item stage (annotate, plan_chapters, generate_titles) is already O(part) per prompt. The **only** prompt that grows with `n_los` in the base design is `plan_parts` (~20 tokens/LO). At 500 LOs that is ~10k tokens (fine), at 1,000 ~20k (risky for attention quality), at 2,000 ~40k (unacceptable). Part K removes that last linear dependency and adds output handling.

## K2. Tier selector (in `ingest`)

```python
def select_tier(n_los: int, settings) -> str:
    if n_los <= settings.scale.t0_max_los:      # default 300
        return "T0"
    if n_los <= settings.scale.t1_max_los:      # default 1000
        return "T1"
    return "T2"
```

Tier is written to `state["tier"]` and drives conditional edges after `normalise_skills`. A `--tier` CLI override exists so every tier can be tested on tiny inputs.

## K3. Tiered planning graph (ASCII)

```
   … normalise_skills [LLM] ──► skill_stats [code]: for each canonical skill →
                                 {skill, lo_ids[], lo_count, tier_mix, examples[2]}
                                          │
                       ┌──────────────────┼──────────────────────┐
                    tier T0            tier T1                 tier T2
                       │                  │                        │
                       ▼                  ▼                        ▼
        ┌────────────────────┐ ┌────────────────────┐ ┌──────────────────────────┐
        │ plan_parts   [LLM] │ │ split_big_skills   │ │ split_big_skills   [code]│
        │ over LO ids        │ │           [code]   │ └────────────┬─────────────┘
        │ (<= ~7k tokens)    │ │ skill > 40 LOs ->  │              ▼
        └─────────┬──────────┘ │ split by tier      │ ┌──────────────────────────┐
                  │            └─────────┬──────────┘ │ plan_domains        [LLM]│
                  │                      ▼            │ in : skill table (~4–8k) │
                  │            ┌────────────────────┐ │ out: domains[{name,      │
                  │            │ plan_parts   [LLM] │ │      order, skills[]}]    │
                  │            │ over SKILLS        │ └────────────┬─────────────┘
                  │            │ in : skill table   │              │ Send() x domains
                  │            │ out: parts as      │    ┌─────────┼─────────┐
                  │            │      skill lists   │    ▼         ▼         ▼
                  │            └─────────┬──────────┘ ┌──────┐ ┌──────┐ ┌──────┐
                  │                      │            │plan_ │ │plan_ │ │plan_ │  [LLM ∥]
                  │                      │            │parts │ │parts │ │parts │  per domain,
                  │                      │            │ D1   │ │ D2   │ │ Dk   │  CCC + its skills
                  │                      │            └──┬───┘ └──┬───┘ └──┬───┘
                  │                      │               └────────┼────────┘
                  │                      ▼                        ▼
                  │            ┌──────────────────────────────────────────────┐
                  │            │ expand_parts [code]: skills -> LO ids per part│
                  │            │ order parts (domain order -> part order)      │
                  └───────────►│ assign_semesters [code]: cumulative est.      │
                               │ lesson days vs total_lesson_days / 2          │
                               │ build Course Context Card + name registry     │
                               └──────────────────────┬───────────────────────┘
                                                      ▼
                                       plan_chapters (∥ per part) … unchanged
```

Nodes added: `skill_stats`, `split_big_skills`, `expand_parts` (`[code]`) and `plan_domains` (`[LLM]`). `plan_parts` gets a second prompt family (`prompts/plan_parts_by_skill/*.md`, one per progression type) with the same output shape (`lo_ids` replaced by `skills`).

## K4. Schemas added

```python
class SkillStat(BaseModel):
    skill: str; lo_count: int
    tier_mix: dict[Literal["Foundational","Intermediate","Advanced"], int]
    examples: list[str] = Field(max_length=2)        # two short objective texts (<= 90 chars each)

class DomainPlanItem(BaseModel):
    domain_id: str; domain_name: str; order: int; skills: list[str] = Field(min_length=1)
class DomainsPlanOut(BaseModel):
    domains: list[DomainPlanItem] = Field(min_length=1, max_length=20)

class PartBySkill(BaseModel):
    part_id: str; part_name: str; order: int
    part_domain_complexity: Literal["Foundational","Intermediate","Advanced"]
    skills: list[str] = Field(min_length=1)
class PartsBySkillOut(BaseModel):
    parts: list[PartBySkill] = Field(min_length=1)
```

Validation for skill-level outputs: every skill exactly once (missing → targeted repair → fallback: append to the last part of the nearest domain); unknown skill strings → dropped and logged.

## K5. Course Context Card (CCC) — the end-to-end context carrier

Built by code in `expand_parts` and **refreshed** before every fan-out (chapters, titles, repair). Prepended to the user message of every per-part call. Target ≤ 400 tokens; it never contains LO text.

```
COURSE  : {course_title} | {grade_band} | {subject_area} | {progression}
CALENDAR: {lessons_per_week}/wk x {weeks} wk = {total_lesson_days} days · {minutes}/day · word limit {word_limit}
SEMESTER A: P1 "Logic and Proof" · P2 "Counting Principles" · P3 "…"
SEMESTER B: P7 "…" · P8 "…"
THIS UNIT : P4 "Proportional Reasoning" (domain "Ratios & Rates", unit 4/11, Intermediate, 31 objectives)
NAMES USED: [Logic and Proof, Argument Fallacies, Quantified Statements, …]     <- name registry, capped at 150 most recent
GUIDANCE  : {user_prompt or "none"}
```

Implementation notes:
- `state["ccc_base"]` (course + calendar + semester lines) is computed once; per-call lines are formatted at fan-out time from `state["parts_plan"]` and `state["name_registry"]`.
- `name_registry: Annotated[list[str], operator.add]` — batches append names as they return; because fan-out batches run concurrently, the registry seen by batch *k* may lag. That is acceptable: **code enforces global uniqueness afterwards** (`naming.uniquify_global`) — the registry only improves first-pass quality.
- Optional `naming_review` [LLM] after `generate_titles` when `n_parts > 12`: input is the *list of names only* (part → chapter → module titles, ~8 tokens each; 2,000 modules ≈ 16k tokens → chunk by semester if > 10k). Output `{id: new_name}` deltas for style consistency only; code re-validates uniqueness and banned patterns.

## K6. Semester assignment at scale (code)

```python
def assign_semesters(parts, total_lesson_days):
    half = total_lesson_days / 2
    cum = 0
    for i, p in enumerate(parts):                    # parts already in final order
        p["est_lesson_days"] = 1 + p["est_understand_chapters"] + 3   # intro + understand + apply/review/test
        cum += p["est_lesson_days"]
        p["semester"] = "A" if (cum <= half or i == 0) else "B"
    # keep a domain intact: if the boundary splits a domain, move it to the nearer domain edge
    ...
```

`est_understand_chapters` comes from running the same packing function on the part's LOs before `pack_and_merge` — cheap and deterministic. `assemble` supports `semester_layout: trailing | interleaved` (default `trailing` = today's contract: both semester pairs at the end; `interleaved` places the Semester A pair after the last Semester-A content part).

## K7. Large-output pipeline

```
 generate_titles ∥ ──► assemble [code, streaming]
                         │  for part in packed.parts: build part dict -> writer.write_part(part)
                         │  writer: JSON array streamer (file / S3 multipart) + running totals
                         ▼
                   OutlineStore.put(run_id, parts_iter) ──► outline_ref = {"kind": "s3"|"file"|"db", "key": …, "bytes": N, "sha256": …}
                         │
                         ▼
                   validate [code]  reads via OutlineStore.iter_parts(run_id)  (single pass, O(n))
                         │
                         ▼
                   state["outline_ref"]  (never the blob when bytes > inline_threshold, default 1 MB)
```

- `OutlineStore` protocol: `put(run_id, parts_iter)`, `iter_parts(run_id)`, `get_part(run_id, n)`, `get_full(run_id)`, `patch_part(run_id, part_id, part)`. Implementations: `FileStore` (MVP), `S3Store`, `PostgresStore` (JSONB per part — enables per-unit regeneration and paginated UI reads).
- API: `GET /outline/{run}` returns metadata + `outline_url`; `GET /outline/{run}/parts?page=` for UIs; `GET /outline/{run}/stream` (NDJSON, one part per line) for progressive rendering; `GET /outline/{run}/export.xlsx` streamed with `openpyxl` write-only mode, one row per module (Unit #, Unit Name, Lesson #, Lesson Name, LO Type, Cypress Module, Assessment, Learning Goal, Standard Code, Standard).
- Checkpoint hygiene: `los` for 2,000 LOs ≈ 1.5 MB — fine in Postgres checkpoints; above 5,000 LOs move `los` to `OutlineStore` too and keep only ids in state (same pattern, config threshold).
- Memory: assemble never holds more than one part plus running totals; validation streams.

## K8. Regeneration and editing at scale (design hooks, not MVP)

| Operation (`requirements.md` §4) | Mechanism |
|---|---|
| Regenerate one unit with user prompt | Re-run `plan_chapters(P)` → `pack_and_merge` (scoped to P; min-4 merge may pull the neighbour — report it) → `generate_titles(P)` → `assemble.patch_part` → `validate` |
| Regenerate full outline | New run with same `run_id` lineage; previous checkpoint retained for undo |
| Undo | `OutlineStore` versions per patch; checkpoint `thread_id` + version pointer |
| Manual title/name edits | State patch to `titles` / `parts_plan` → `assemble.patch_part` → `validate` (no LLM) |
| Drag-and-drop move | State patch to `los[id].part_id / chapter_name / order_rank` → scoped `pack_and_merge` + patch |

All of these are cheap because everything is id-keyed and the document is built from state, not from an LLM transcript.

## K9. Tier test matrix (add to Phase 12)

| Fixture | n_los | Tier | Assertion |
|---|---|---|---|
| synthetic-500 | 500 | T1 | valid; max prompt < 8k; every skill planned once; semester split within ±1 part of half |
| synthetic-1000 | 1,000 | T1 | valid; outline stored via `OutlineStore`, `outline_ref` in state, no blob in checkpoint |
| synthetic-2000 | 2,000 | T2 | valid; `plan_domains` ≤ 20 domains; per-domain prompts < 8k; wall-clock < 6 min at concurrency 8 |
| forced-tier | 43 with `--tier T2` | T2 | same structure guarantees on tiny input (tier logic has no size assumptions) |

## K10. Scale summary

```
                      n_los ->   10     100     300     500    1,000    2,000    5,000
 planning tier                   T0     T0      T0      T1     T1       T2       T2
 largest single prompt (tok)    ~1k    ~3k     ~7k     ~5k    ~6k      ~8k      ~8k
 LLM calls                      ~4     ~12     ~30     ~48    ~95      ~190     ~470
 sequential LLM rounds           4      5       5       5      5        6        6
 structural failures possible    0      0       0       0      0        0        0
```
