# Course Outline Generator — Lean System Design (Python + LangGraph)

> One document. Everything needed to build the system from scratch. Nothing that is not needed.
> Works for 10, 100, 300, 1,000 learning objectives (LOs) with the same graph. No queues, no databases, no microservices — add those later only if a real need appears.

---

## 1. What the system does

```
INPUT  (JSON)                                   OUTPUT (JSON, DCIM contract)
──────────────────────────────                  ─────────────────────────────────────────
course_title, grade_band, subject_area          Course
minutes_per_lesson, lessons_per_week,            ├─ Part 1  Course Overview (guide, intro)
course_duration_weeks                            ├─ Part 2..N  content units
course_outline_progression (4 enums)             │    ├─ Introduction chapter
learning_objectives[] {urn, objective}           │    ├─ Understand chapters (≥ 4)  ← 1 module per LO
user_prompt (optional)                           │    ├─ Apply · Review · Part Test
                                                 ├─ Semester A Review + Exam
                                                 └─ Semester B Review + Exam
                                                 + totals, estimates, pacing, assessments
```

Hard rules (from `requirements.md` / STUDIOPE-301): every LO → exactly one module; every content part ≥ 4 understand chapters (merge adjacent if fewer; exception when exactly 2 parts and combined < 4); chapter ≤ word limit (grade band) and ≤ minutes per lesson; ≤ 4 LOs per chapter; word/time estimates from grade band × Bloom's; pacing vs `lessons_per_week × weeks` ± 5 %.

## 2. Five design rules

1. **LLM decides, Python owns data.** LLM outputs are ID-keyed deltas (`{"L17": ...}`). No LLM ever re-emits its input.
2. **Python builds the document.** One assembler. LLM only produces names and titles.
3. **Counting is code.** Packing, merging, numbering, totals, pacing — pure functions, unit-tested, never retried.
4. **Every prompt is bounded.** Per-item work is batched; the one global call sees a compact projection (≤ ~7k tokens).
5. **Every LLM boundary = validate → re-ask only the missing ids once → deterministic fallback.** Pipeline always ends with a valid outline.

## 3. The graph

```
                     ┌───────────┐
                     │ __start__ │
                     └─────┬─────┘
                           ▼
              ┌────────────────────────┐
              │ ingest          [code] │ validate input · ids L1..Ln · grade band ·
              │                        │ lesson days · word limit · batches
              └───────────┬────────────┘
                          │ Send × batches (30 LOs each)
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  ┌───────────┐     ┌───────────┐     ┌───────────┐
  │ annotate  │     │ annotate  │     │ annotate  │   [LLM ∥]  {id: verb, skill}
  └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
        └─────────────────┼─────────────────┘
                          ▼  reducer merges; code maps verb → Bloom's tier
              ┌────────────────────────┐
              │ plan_parts      [LLM]  │ ONE call. input: [{id, skill, tier}]
              │                        │ (>300 LOs: input = unique skills instead)
              │                        │ output: parts[{name, order, ids}]
              └───────────┬────────────┘
                          │ Send × parts
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │plan_chapters│   │plan_chapters│   │plan_chapters│  [LLM ∥]  per part:
  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘  {id: chapter_name, order_rank}
         └─────────────────┼─────────────────┘
                           ▼
              ┌────────────────────────┐
              │ pack_and_merge  [code] │ estimates · bin-pack · min-4 merge ·
              │ (existing service)     │ uniquify names · number · coverage check
              └───────────┬────────────┘
                          │ Send × parts
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │   titles    │   │   titles    │   │   titles    │  [LLM ∥]  per part: {id: title}
  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
         └─────────────────┼─────────────────┘
                           ▼
              ┌────────────────────────┐
              │ assemble        [code] │ DCIM JSON · structural chapters · semesters ·
              │                        │ assessments · totals · pacing
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
              │ validate        [code] │ 6 invariants
              └───────────┬────────────┘
                          ▼
                     ┌───────────┐
                     │  __end__  │
                     └───────────┘
```

Seven node types. Three LLM (annotate, plan_parts, plan_chapters, titles = 4 prompts), four code. No repair node: **fallbacks live inside each LLM node** (re-ask once, then deterministic), so `validate` at the end can only fail on a bug.

### Why this shape

| Old graph problem (measured in llmlogs) | Fix |
|---|---|
| Planner re-emitted 72-chapter tool payload → truncated to 9 chapters at 94 LOs | Tool is a Python call inside the graph; nothing is re-emitted |
| DCIM regenerated whole JSON: 13.6k output tokens @ 43 LOs | `assemble` is code; LLM only titles (~10 tok/LO) |
| Every node re-typed all LO text | Nodes read state projections; LLM returns ids only |
| Bloom's tier classified by LLM | Verb → tier lookup table (already in the old prompt) |
| Four router nodes, one per progression | One `plan_parts` node, prompt file chosen by enum |

## 4. State

```python
class LO(TypedDict, total=False):
    id: str; urn: str; text: str; idx: int
    verb: str; skill: str; tier: str            # tier ∈ Foundational|Intermediate|Advanced
    part_id: str; chapter: str; rank: int
    title: str
    flags: list[str]                            # e.g. ["annotate_fallback"]

def merge_los(a: dict, b: dict) -> dict:            # reducer: per-id dict merge
    out = dict(a)
    for k, patch in b.items():
        out[k] = {**out.get(k, {}), **patch}
    return out

class State(TypedDict, total=False):
    course: dict            # title, band, subject, minutes, lessons_per_week, weeks, progression, user_prompt
    budget: dict            # total_lesson_days, word_limit
    batches: list[list[str]]
    los: Annotated[dict[str, LO], merge_los]           # single copy of all LO data, id-keyed
    parts: list[dict]       # [{part_id, name, order, ids}]
    packed: dict            # output of pack_and_merge
    titles: Annotated[dict[str, str], lambda a, b: {**a, **b}]
    outline: dict
    report: Annotated[list[dict], operator.add]         # per-call tokens/latency + fallbacks
```

Nodes return partial dicts; reducers merge. Fan-out payloads (`Send`) carry only the slice a batch needs.

## 5. Nodes

| Node | Type | Reads | Prompt input (projection) | Output | Fallback if LLM fails |
|---|---|---|---|---|---|
| `ingest` | code | raw input | — | course, budget, los, batches | — (input error → stop) |
| `annotate` | LLM ∥ | batch ids + text | `id \| objective` (≤ 30 rows) | `{id: verb, skill}`; code adds tier | verb = first word; skill = first 3 content words |
| `plan_parts` | LLM ×1 | all los | `id \| skill \| tier` (≤ 300) **or** `skill \| count \| tiers \| example` (> 300, code expands skills → ids) | parts with ordered ids | missing ids → part with same skill, else last part |
| `plan_chapters` | LLM ∥ | one part | part names (context) + `id \| objective \| skill \| tier` | `{id: chapter, rank}` | one chapter per skill; rank by tier then input order |
| `pack_and_merge` | code | los, parts, budget | — | packed parts/chapters/stubs, log, validation | cannot fail (bug → raise) |
| `titles` | LLM ∥ | one packed part | chapters + `id \| objective \| skill` stubs | `{id: title}` | `"{Skill}: {Verb}"` |
| `assemble` | code | course, budget, packed, titles | — | outline | — |
| `validate` | code | outline, los | — | report entry | raise on failure (bug) |

**Bloom's tier (code):** dict built from the three verb lists in `LearningObjectiveAnalyser.md`; lowest tier wins on duplicates; unknown → Foundational.

**Skill normalisation (code, not LLM):** `casefold`, strip stop words, singularise, sort words → key. Good enough; if quality needs it later, add one small LLM call over the unique-skill list (≤ 100 rows).

**Global context across batches:** `plan_chapters` and `titles` receive a 5-line header — course, calendar, ordered part names, "this unit N of M", user prompt. That is the whole course context any per-part call needs.

**> 300 LOs:** `plan_parts` switches input from LO rows to unique-skill rows (~10 % of LO count). Code expands each skill to its ids. Skills with > 40 LOs are pre-split by tier. Nothing else changes. Largest prompt stays < 8k tokens at 1,000+ LOs.

## 6. LLM layer (provider-agnostic)

```python
class LLM:
    def __init__(self, provider: str, models: dict[str, str]):
        # provider ∈ {"anthropic", "openai", "bedrock_converse"}
        self.m = {role: init_chat_model(f"{provider}:{name}", temperature=0) for role, name in models.items()}

    async def call(self, role: str, system: str, user: str, schema: type[T]) -> tuple[T, dict]:
        model = self.m.get(role, self.m["default"]).with_structured_output(schema, include_raw=True)
        # tenacity: 3 retries on 429/5xx/timeout; 1 corrective retry on ValidationError
        ...
        return parsed, {"role": role, "prompt_tokens": ..., "completion_tokens": ..., "ms": ...}
```

- `init_chat_model` covers Anthropic, OpenAI and Bedrock with the same code path.
- Pydantic schema is the only contract; prompts contain no vendor-specific JSON instructions.
- Per-role model choice in config (`annotate`/`titles` → small model; `plan_*` → strong model).
- `FakeLLM` with the same `call()` signature for offline tests.

## 7. Prompts (4 files, ≤ 600 tokens of instructions each)

| File | Role | Rules that matter |
|---|---|---|
| `annotate.md` | extract verb + 2–4 word Title Case skill noun phrase | same competency → same skill name; return ids exactly |
| `plan_parts_{skills,theme,chrono,standards}.md` | group into 4–8-chapter units, name ≤ 6 words, order | every id once; **do not** enforce minimum sizes (code merges); honour `user_prompt` |
| `plan_chapters.md` | ~3 LOs per chapter (2 if Advanced), 2–4 word chapter names, rank Foundational→Advanced then prerequisites | every id once; unique names in unit |
| `titles.md` | 2–5 word noun-phrase module title from objective | distinct within chapter; not the chapter name; no "Part 2/Continued/Module N" |

Format for all: system = role + rules; user = 5-line course header + pipe-delimited rows. No JSON blobs in prompts.

## 8. Deterministic core (port from `course_outline_structure_service.py`)

```
rules/
  blooms.py     VERB_TIER table, tier_for(verb)
  estimates.py  GRADE_WORD_LIMITS, GRADE_WORD_RANGES, BLOOMS_TIME_RANGES, words(band,tier), minutes(tier)
  packing.py    pack(los, word_limit, minute_limit, max_los=4) → chapters       ← _pack_los_into_chapters
  merging.py    enforce_min_4(parts) → (parts, log)                              ← _enforce_minimum_4 (+2-part exception)
  naming.py     merge_part_names, uniquify_chapter_names                         ← existing
  grade_band.py normalize(raw) → "K-2"|"3-5"|"MS"|"HS"
assemble/
  dcim.py       build(course, budget, packed, titles) → outline dict (matches tool-response-43 contract)
  assessments.py  understand→Quick Check · apply→Sample Work · review→Unit Online Practice ·
                  test→Unit Test · semester_review→Semester Online Practice · semester_exam→Semester Exam
  pacing.py     tol = round(days×0.05); overrun if total_chapters > days + tol
validate/
  invariants.py 1 every URN exactly once  2 parts ≥ 4 or exception logged  3 semesters A+B  
                4 order = packed order    5 chapter sums & totals correct    6 titles present+distinct
```

Totals: `total_parts = 1 + content_parts + 2`; `total_chapters = 1 + content_chapters + 4·content_parts + 4`.

## 9. Repo layout (minimal)

```
outline/
  __main__.py      CLI: outline generate input.json --provider anthropic --out out/
  config.yaml      provider, models per role, batch_size=30, max_concurrency=5, retries
  state.py
  schemas.py       CourseRequest · AnnotateOut · PartsOut · ChaptersOut · TitlesOut · DCIM models
  graph.py         build_graph(llm, settings) — nodes, Send fan-outs, edges
  nodes.py         ingest · annotate · plan_parts · plan_chapters · pack_and_merge · titles · assemble · validate
  llm.py           LLM wrapper + FakeLLM
  prompts/         annotate.md · plan_parts_*.md · plan_chapters.md · titles.md
  rules/  assemble/  validate/
tests/
  unit/            rules, assemble, validate (100 % branches; property test: URN multiset preserved)
  graph/           end-to-end with FakeLLM on 43/94/123/synthetic-300/synthetic-1000 fixtures
  live/            one real-provider smoke on 43 (opt-in)
```

Graph wiring in ~40 lines:

```python
g = StateGraph(State)
for n in (ingest, annotate, plan_parts, plan_chapters, pack_and_merge, titles, assemble, validate): g.add_node(n)
g.add_edge(START, "ingest")
g.add_conditional_edges("ingest", lambda s: [Send("annotate", slice_(s, ids)) for ids in s["batches"]])
g.add_edge("annotate", "plan_parts")
g.add_conditional_edges("plan_parts", lambda s: [Send("plan_chapters", part_slice(s, p)) for p in s["parts"]])
g.add_edge("plan_chapters", "pack_and_merge")
g.add_conditional_edges("pack_and_merge", lambda s: [Send("titles", packed_slice(s, p)) for p in s["packed"]["parts"]])
g.add_edge("titles", "assemble"); g.add_edge("assemble", "validate"); g.add_edge("validate", END)
app = g.compile(checkpointer=MemorySaver())
```

## 10. Reliability and scale numbers

| n_los | LLM calls | Largest prompt | Total in / out tokens | Sequential rounds |
|---|---|---|---|---|
| 43 | ~6 | ~3k | ~8k / 2k | 4 |
| 94 | ~12 | ~4k | ~15k / 3k | 4 |
| 300 | ~30 | ~7k | ~38k / 8k | 4 |
| 1,000 | ~95 | ~6k (skill rows) | ~115k / 26k | 4 |

Old graph at 94 LOs: 77k / 32k tokens and **failed**. Here every structural rule is produced by code, so structural failure rate is zero by construction; the only LLM-quality risk is naming, which has a fallback.

Operational defaults: `temperature=0`, `max_concurrency=5`, LLM timeout 90 s, transport retries 3, `MemorySaver` checkpointer (swap for Postgres only when you need resume across processes).

## 11. Output artefacts per run

- `outline.json` — DCIM document (same shape as `tool-response-43-lg-new.txt`, plus optional `assessment` per chapter).
- `report.json` — per-call tokens/latency, enforcement log, fallbacks used, invariant results, pacing.

## 12. Build order (7 steps, each testable alone)

1. `schemas.py` + golden-output round-trip test from `tool-response-43-lg-new.txt`.
2. `rules/` ported from the existing service + unit/property tests.
3. `assemble/` + `validate/` — reproduce the golden 43-LO output from the real packed tool response + real titles.
4. `llm.py` (+ `FakeLLM`) + 4 prompt files.
5. `nodes.py` — LLM nodes with validate → re-ask → fallback.
6. `graph.py` + CLI + `report.json`.
7. Run 43 → 94 → 123 → synthetic-300 → synthetic-1000 with FakeLLM, then live on Anthropic; flip `--provider openai` on 43.

## 13. Explicitly not built (until needed)

REST API, job queue, Postgres checkpointer, object storage, per-unit regeneration/undo, Excel export, standards graph view, content reuse across states, Berlin registration. The id-keyed state makes all of them additive later; none are needed to prove the design.
