# The Simple Guide — How the Course Outline Generator Works

> Plain-language explanation of everything: what the LLM does, what Python does, and how —
> with tiny examples at every step. All examples are from the real 43-objective `Test_Math` run.

The one idea that explains the whole system:

> **The LLM decides meaning, grouping and names. Python controls structure, order, math,
> the final document — and checks everything.**

```
Learning Objectives (input JSON)
      ↓
 1. Ingest            [Python]   ids, order, budgets
 2. Annotate          [LLM ∥]    verb + skill per objective   (+ Python: Bloom's level)
 3. Plan Units        [LLM ×1]   which objectives belong together
 4. Plan Lessons      [LLM ∥]    lessons inside each unit
 5. Pack & Merge      [Python]   time/word math, min-4 rule, numbering
 6. Titles            [LLM ∥]    nice module names             (+ Python: checks them)
 7. Assemble          [Python]   the final course JSON
 8. Validate          [Python]   7 checks, or it doesn't ship
```

---

## 1. Ingest — Python reads the input

Python gives every objective a short internal ID and remembers its original position:

```
L1 → "Construct valid logical arguments…"        position 0
L2 → "Apply rules of inference…"                 position 1
L3 → "Identify logical fallacies…"               position 2
L4 → "Evaluate … using truth tables…"            position 3
…L43
```

The real URN (`urn:pearson:learninggoal:2663de0d-…`) is parked in a Python map.
**The LLM never sees a URN** — so it can never mangle or drop one.

Python also computes the budget, pure arithmetic:

```
5 lessons/week × 36 weeks = 180 lesson days
grade band MS → word limit 2000 per lesson
```

And it plans the batches: `[[L1…L30], [L31…L43]]`.

## 2. Annotate — LLM reads each objective (in parallel batches)

The 43 objectives are split into batches of 30, sent as **parallel** LLM calls.
Each call sees only its rows and returns two labels per ID:

```
IN : L3 | Identify logical fallacies in arguments including ad hominem…
OUT: L3 → verb: identify   skill: Logical Fallacies
```

The LLM does **not** decide the Bloom's level. Python looks the verb up in a fixed table:

```
identify  → Foundational
construct → Intermediate
evaluate  → Advanced
(unknown / no verb → Foundational, the safe default)
```

**Why batches don't clash:** batch 1 owns L1–L30, batch 2 owns L31–L43 — disjoint IDs.
Python merges the answers per-ID; finish order doesn't matter.

**If the LLM skips an ID:** Python re-asks *only* the missing IDs once; if still missing,
a code fallback fills it and flags it (`annotate_fallback`) in the report. Nothing is ever lost.

## 3. Plan Units — ONE LLM call sees the whole course (cheaply)

This is the only place the whole course appears in a single prompt — and only as
one tiny line per objective (~20 tokens):

```
L1 | Logical Arguments | Intermediate
L3 | Logical Fallacies | Foundational
L7 | Multiplication Principle | Intermediate
…
```

The LLM answers one question: **"which objectives belong together?"** Real answer (43 LOs → 7 units):

```
1. Logical Reasoning And Argumentation   [L3, L1, L2, L4, …]
2. Counting And Combinatorics            [L7, L8, L9, …]
3. Number Systems And Information Theory
4. Sequences And Recursive Processes
5. Graph Theory And Networks
6. Voting Theory And Social Choice
7. Fair Division Methods
```

**Big course?** Above 300 objectives the rows become unique *skills* instead
(~70 rows for 1,000 LOs) and Python expands each chosen skill back into its IDs.
That's why the prompt never explodes — proven live at 1,000 LOs, max prompt ~6k tokens.

**Progression types:** the only thing that changes between skills/theme/chronological/
standards-driven is one guidance paragraph injected into this prompt (the `GUIDANCE` dict in
`nodes.py`). For standards-driven, Python additionally **ignores** the model's ordering and
forces input order (that's a hard requirement — reordering is a critical defect).

## 4. Plan Lessons — one parallel LLM call per unit

Now each call sees just its own unit (10–30 objectives, full text this time) plus a shared
5-line header — course, calendar, progression rules, and the *names* of all units so naming
stays coherent. It returns lesson groups and an order rank:

```
L3 → lesson "Logical Fallacies",              rank 1   (Foundational first)
L1 → lesson "Valid Arguments",                rank 2
L2 → lesson "Valid Arguments",                rank 2
L4 → lesson "Truth Tables",                   rank 4   (Advanced last)
```

The rank is a *suggestion*; Python sorts by `(rank, lesson, input position)` — so ties always
resolve deterministically, and in standards mode rank is overwritten with input position.

## 5. Pack & Merge — Python does all the math (no LLM)

**Per-objective estimates** come from fixed tables (grade band × Bloom's tier):

```
Foundational (MS) → 291 words / 14 min
Intermediate (MS) → 475 words / 18 min
Advanced     (MS) → 659 words / 26 min
```

**Packing** — fill each lesson in order until the next objective would break a limit
(2000 words, 60 minutes, or 4 objectives):

```
Lesson "Valid Arguments":
  L1 (475w/18m) + L2 (475w/18m) = 950w/36m   → fits, one lesson
Lesson trying to add an Advanced LO at 54 min used:
  54 + 26 = 80 > 60                           → close lesson, start a new one
```

**The min-4 rule** — every unit needs ≥ 4 understand lessons, or it's merged with a neighbour.
Real log from the 43-LO run:

```
MERGE: 'Counting And Combinatorics' (3 lessons) + 'Number Systems And Information Theory' (4)
RESULT: 'Counting Combinatorics & Number Systems' now has 7 lessons
… 7 planned units → 4 shipped units, all ≥ 4 lessons
```

**Numbering** — units from 2 (unit 1 is the Course Overview), lessons from 2 (lesson 1 is the
Intro), modules from 1. Counting loops, not a model — the old system's broken numbering
(`[11, 2, 3…]`) is impossible here.

**Duplicate names** — if two lessons in a unit end up with the same name, Python makes them
specific ("Fractions - Denominators"), numeric suffix only as a last resort. Same for unit names.

## 6. Titles — LLM writes the names, Python checks them

Structure is now frozen. The LLM's only job: a 2–5 word title per module.

```
L4 "Evaluate the validity of deductive arguments using truth tables…"
   → "Evaluating Argument Validity"
```

Python rejects: duplicates within a lesson, titles equal to the lesson name, banned patterns
("Module 3", "Part 2", "Practice", "Continued"). Rejected IDs get one re-ask, then a code
fallback ("Deductive Validity: Evaluate") with a flag. In 9 live runs (43→1000 LOs): zero fallbacks.

## 7. Assemble — Python builds the final JSON

```
Course
├── Part 1  Course Overview        (Course Guide + Course Introduction)
├── Part 2  Logical Reasoning And Argumentation
│     ├── Introduction lesson
│     ├── understand lessons  (the packed ones, each module = one LO with its URN copied back byte-for-byte)
│     ├── Apply · Review · Part Test
├── Part 3, 4, 5  (same shape)
├── Semester A  Review + Exam
└── Semester B  Review + Exam
```

Plus, all computed: assessments per lesson type (Quick Check on understand, Sample Work on
apply, Unit Test, Semester Exam…), totals (`total_parts = 1 + content + 2`), and pacing
(46 chapters vs 180 days ± 5 % → "under-filled" note). The LLM never writes one character of this JSON.

## 8. Validate — Python checks everything, or it doesn't ship

```
✓ every one of the 43 URNs appears exactly once
✓ no duplicates ✓ every unit ≥ 4 understand lessons
✓ overview first, semesters last ✓ numbering sequential
✓ lesson totals = sum of their modules ✓ totals fields correct
✓ names unique at every level ✓ titles valid
→ result: []  (no errors)
```

A structural failure raises an error instead of shipping — it would mean a code bug, and we
never "retry" an LLM to fix a code bug. Soft findings (title style, over-budget lesson) are
reported in `report.json`, not fatal.

---

## What happens when the LLM makes a mistake? (every LLM step, same defence)

```
1. schema check      — reply must match the expected shape (forced, not hoped)
2. coverage check    — every expected ID present?
3. targeted re-ask   — ask again for ONLY the missing IDs, once
4. code fallback     — deterministic value + a flag in report.json
```

So the pipeline **always finishes with a valid outline**; the report tells you honestly which
parts fell back. Live proof: one provider timeout mid-run → 12 lesson names fell back, outline
still valid.

## The house analogy

- **LLM = architect**: "these rooms belong together; call this one 'Logical Reasoning'."
- **Python = structural engineer**: dimensions, budgets, room numbers, building code, inspection.
- **Final JSON = the finished house** — built by the engineer from the architect's drawings,
  never by the architect free-handing bricks.

## Regeneration, in the same simple terms

You point the tool at a **previous run's folder** and pick a scope:

```
--unit all           regenerate the whole course.  Python compresses the OLD outline into a
                     few lines ("PREVIOUS UNIT 'X': lesson1; lesson2; …") and puts them in
                     every prompt: "improve this, don't repeat it."
--unit 2             regenerate ONE unit. Its old lessons+titles go in the prompt as context;
                     every OTHER unit is locked by Python — proven byte-identical (31/31 modules).
--unit 1 --lesson 2  regenerate ONE lesson's module titles only; everything else locked.
```

Your `--prompt` ("make lesson names more application-focused") gets explicit priority over
naming/grouping preferences — but can never override coverage, standards order, or structure.
No prompt = standard regeneration (context only). Every regeneration writes a NEW folder with a
`regeneration.md` before/after diff; the old folder is untouched — that's your undo.
Real result: "Permutations Of Distinct Objects" → "Ranking Contest Winners".

Bad prompts are caught by Python *before* any model call: `<script>`, "ignore previous
instructions", or something unrelated ("buy pizza tomorrow") → clear error message, zero cost.

## Cheat sheet — who does what

| Decision | Who | How |
|---|---|---|
| verb + skill per objective | LLM | extraction from text |
| Bloom's level | Python | verb lookup table |
| which objectives form a unit; unit names | LLM | one compact call (skills-rows at scale) |
| lessons inside a unit; suggested order | LLM | one call per unit, parallel |
| final order | Python | sort (rank, lesson, input position); input-order forced for standards |
| words/minutes per objective | Python | grade×tier tables (291/475/659 w · 14/18/26 min at MS) |
| lesson packing, min-4 merging | Python | greedy bin-pack + merge loop |
| numbering, totals, pacing, assessments | Python | counting loops + formulas |
| module titles | LLM | 2–5 word phrases; Python re-checks and can fall back |
| final JSON | Python | assembler (byte-equal to legacy contract on the golden test) |
| verification | Python | 8 invariants; structural failure = don't ship |
| mistake recovery | Python | schema → re-ask missing → fallback + flag |

**Everything the course must never get wrong is Python. Everything that needs judgment or
language is the LLM — and even that is checked.**
