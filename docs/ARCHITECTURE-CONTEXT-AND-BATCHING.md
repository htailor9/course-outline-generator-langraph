# Architecture Deep-Dive — Batching & Context Management

> Complete explanation of how the pipeline splits work into batches and how context (course-level,
> LG-level, previous-version) is carried, so that no prompt grows with course size and no parallel
> worker can corrupt shared data. Numbers are from real runs (43 → 1,000 LOs live on Claude Sonnet).

---

## 1. The context problem this design solves

The old Berlin graph carried context by **forwarding payloads through LLMs**: every node re-typed
everything it received. Measured consequence at 94 LGs: the planner's post-tool prompt hit 43,708
tokens and it re-emitted only 2 of 11 units — silent context loss, run failed. Context handled as
LLM output *is* the failure mode.

This architecture inverts it:

> **Context lives in ONE Python dict. Prompts receive projections of it. LLMs return ID-keyed
> deltas. Reducers merge deltas back. The document is built from the dict, never from prompts.**

## 2. The single source of truth: state

```python
class State(TypedDict):
    course:  dict                                   # title, band, subject, calendar, progression, user_prompt, regen_context
    budget:  dict                                   # total_lesson_days, word_limit
    batches: list[list[str]]                        # the batching plan
    los:     Annotated[dict[str, LO], merge_los]    # ← THE context: one entry per LG, id-keyed
    parts:   list[dict]                             # unit skeleton after planning
    packed:  dict                                   # deterministic structure after pack/merge
    titles:  Annotated[dict[str, str], merge_dict]
    outline: dict                                   # final JSON — written once, by code
    report:  Annotated[list[dict], operator.add]    # per-call metrics
```

Each LG's full context accumulates in `los[id]` across the run:

```
after ingest:        {id:L4, urn:…, text:"Evaluate…", idx:3}
after annotate:      + verb:"evaluate", skill:"Deductive Validity"     (LLM delta)
after tier lookup:   + tier:"Advanced"                                 (code)
after plan_parts:    + part_id:"P1"                                    (LLM delta)
after plan_chapters: + chapter:"Truth Tables", rank:4                  (LLM delta)
after titles:        + title:"Evaluating Argument Validity"            (LLM delta)
```

Nothing is ever copied node-to-node; nodes *read projections* of this dict and *return patches* to it.

## 3. Batching — how work is split

### 3.1 Batch formation (ingest, code)

```
ids = [L1 … Ln] in input order
batches = chunks of settings.batch_size (default 30)
43 LGs  → [[L1…L30], [L31…L43]]          → 2 annotate calls
300 LGs → 10 batches                      → 10 annotate calls, parallel
```

Why 30: ~40 tokens of objective text per row + instructions ≈ 2k-token prompts — deep inside every
model's comfort zone, cheap to retry, fast to run in parallel under `max_concurrency` (default 5).

### 3.2 The disjointness invariant (why parallel is safe)

Every `Send()` fan-out partitions the id space:

```
annotate:      batch k owns ids[30k : 30k+30]           — a partition of all ids
plan_chapters: worker for unit P owns exactly P's ids   — units partition the ids
titles:        worker for packed unit P owns its stubs  — again a partition
```

Workers return patches keyed by ids **they own**. The reducer (`merge_los`) merges per-id, so:
- two workers can never write the same key → no conflicts, no locks;
- merge order is irrelevant → results identical whichever branch finishes first;
- a failed/slow worker damages only its own slice, which the fallback then repairs.

### 3.3 What each batch call carries (the payload)

A `Send` payload is a *slice*, not the state:

```python
Send("annotate", {"batch": ids, "los": {i: los[i] for i in ids}, "course": course, "budget": budget})
Send("plan_chapters", {"part": p, "los": {i: los[i] for i in p["ids"]}, "course", "budget", "part_names"})
```

`part_names` (just the unit names) is the only cross-slice information a worker gets — deliberately.

## 4. Context management — the four context types and their carriers

### 4.1 Course-level context → the 5-line header (every LLM call)

Built fresh by `course_header()` for each call, never stored in prompts between calls:

```
COURSE: Test_Math | grade band MS | Math | SKILLS_BASED_PROGRESSION
CALENDAR: 5 lessons/week x 36 weeks = 180 lesson days; 60 min/lesson; word limit 2000
PROGRESSION: <the one paragraph for this progression type, from the GUIDANCE dict>
UNITS: 1. Logical Reasoning And Argumentation · 2. Counting … · …      (names only)
THIS UNIT: Counting Combinatorics & Number Systems (per-unit calls only)
USER GUIDANCE (takes PRIORITY … never overrides coverage/structure): <user_prompt, if any>
REGENERATION: … PREVIOUS UNIT … (regeneration only)
```

~150–400 tokens. This is 100 % of the shared context any parallel worker needs. The `UNITS:` line
is what keeps 7 concurrent unit-planners naming things coherently without seeing each other's LGs.

### 4.2 LG-level context → projections, scoped by node

Each node gets the narrowest view that lets it decide well:

| Node | Projection per LG | Tokens/LG | Why this much and no more |
|---|---|---|---|
| annotate | `id \| objective text` | ~40 | needs the words to extract verb/skill |
| plan_parts (≤300) | `id \| skill \| tier` | ~20 | grouping needs semantics, not prose |
| plan_parts (>300) | `skill_id \| skill \| count \| tier-mix \| example` per **unique skill** | ~35/skill | whole-course view at O(skills), not O(LGs) |
| plan_chapters | `id \| text \| skill \| tier` (its unit only) | ~45 | full text is fine — the set is 10–30 |
| titles | `lesson \| id \| text \| skill` (its unit only) | ~45 | title needs the objective's own words |
| pack/assemble/validate | — (code reads the dict directly) | 0 | arithmetic needs no prompt |

**What is *never* in any prompt:** URNs, the outline JSON, other units' LG contents, estimates,
numbering. Those live only in Python — a model cannot corrupt what it cannot see.

### 4.3 Global-view context → exactly one call, made cheap

Only `plan_parts` needs the whole course simultaneously. Cost control:

```
 43 LGs → 43 rows  ≈ 1.3k tokens
300 LGs → 300 rows ≈ 6–7k tokens                      (measured cap of id-mode)
>300    → skill mode: 1,000 LGs → ~70 skill rows ≈ 5.7k tokens (measured live)
          skills >40 LGs pre-split by tier so no row hides an oversized cluster
```

Everything else that needs a whole-course view (min-4 merging, dedup, totals, pacing) is done
**after fan-in, in code**, where the complete state costs zero tokens.

### 4.4 Previous-version context (regeneration) → compressed summaries

The prior run's `outline.json` is read back as data (`state_from_outline`), then summarised to
names-only text at the regenerated scope:

| Scope | Context block | Carrier |
|---|---|---|
| full | `PREVIOUS UNIT 'X': lesson1; lesson2; …` per unit (~150 tokens/43 LGs) | `raw["_regen_context"]` → ingest → `course["regen_context"]` → header |
| unit | that unit's `PREVIOUS LESSONS` + `PREVIOUS MODULE TITLES` | node `payload["regen_context"]` → header append |
| lesson | that lesson's `PREVIOUS MODULE TITLES` | same payload route, one titles call |

Non-target material is context **through code, not prompts**: prior placements/ranks/titles are
reused verbatim (byte-locked, verified 31/31 modules identical in unit mode).

## 5. Ordering under concurrency

Order is data, not model behaviour:

1. `idx` (input position) stamped at ingest — immutable.
2. LLM order suggestions are just a `rank` label per id.
3. Final order = one deterministic sort: `(rank, chapter, idx)` — `idx` breaks every tie, so even
   identical ranks from a lazy model yield a stable order.
4. Standards-driven: code overwrites `rank = idx` and re-sorts units by earliest member —
   model ordering is ignored entirely (adversarially tested: reversed model output still yields
   exact input order).
5. Numbering (units/lessons/modules) is assigned by counting loops after packing — parallel
   completion order cannot influence it.

## 6. Failure containment per batch

Every LLM boundary runs the same loop, scoped to its slice:

```
schema-forced reply → coverage check on owned ids → re-ask ONLY missing ids (once)
→ deterministic fallback + flag → reducer merges whatever succeeded
```

Blast radius of any single bad call = its own slice, repaired locally. Observed live: one provider
timeout during a 43-LG full regeneration → 12 lesson names fell back deterministically, outline
still valid, incident visible in `report.json`. The run-level guarantee (100 % coverage, valid
structure) is therefore independent of model reliability.

## 7. Why prompts stay flat as courses grow (measured)

```
LGs      annotate     plan_parts        plan_chapters       titles      max single prompt
 43      2 × ~2k      1 × 1.3k          7 × ~2–3k           4 × ~3k     ~3k
300      10 × ~2k     1 × ~6.5k         ~9 ∥                ~8 ∥        ~7k
1000     34 × ~2k     1 × ~5.7k (skill) ~30 ∥               ~30 ∥       ~6k
```

Cost grows linearly with LGs (more calls); **risk does not** (largest single prompt flat).
Compare the old graph: single-thread, prompts growing to 44k, failing at 94.

## 8. One diagram to remember

```
                      ┌────────────────────────────────────────────┐
                      │        state.los  (id-keyed, in Python)     │  ← the context
                      └───────┬───────────────────────────▲────────┘
             projections      │                           │   id-keyed deltas
   (slice + 5-line header)    ▼                           │   merged by reducers
                    ┌───────────────────┐       ┌───────────────────┐
                    │  parallel LLM     │  ...  │  parallel LLM     │
                    │  worker (batch k) │       │  worker (unit P)  │
                    └───────────────────┘       └───────────────────┘
                              │  after fan-in, code only:
                              ▼
              pack → merge → number → assemble → validate  (full state, zero tokens)
```

**Say it in one sentence:** the course's context is a single Python dictionary; batches get
disjoint slices of it plus a five-line shared header; models hand back labels against IDs;
reducers merge them; and every operation that needs the whole picture happens in code after the
fan-in — which is why a 1,000-objective course never produces a prompt bigger than a 43-objective
one, and why no parallel worker can lose or reorder a learning goal.
