# Course Outline Regeneration — Logic, End-to-End Examples, Edge Cases

> Dedicated reference for the regeneration feature (STUDIOPE-94/277/279/286/291/300/324/338/353).
> Every example below is REAL output from live Claude Sonnet runs on the 43-LO `Test_Math` baseline
> (`runs/20260827-203356_43LOs_Test-Math_claude_cli`); the evidence folders live in `results/43LOs-regen-*`.

---

## 1. The three scopes, one command

```
python -m outline regenerate <baseline-run-dir> --unit all               [--prompt "..."]   # FULL course
python -m outline regenerate <baseline-run-dir> --unit 2                 [--prompt "..."]   # ONE unit
python -m outline regenerate <baseline-run-dir> --unit 1 --lesson 2      [--prompt "..."]   # ONE lesson
```

Shared principles, all scopes:

| Principle | Meaning |
|---|---|
| Baseline is immutable | Every regeneration writes a NEW `runs/<ts>_…regen-…` folder; the baseline folder is your undo — to "restore", just use it instead |
| Previous version is context, never payload | Old names are summarised into the prompt (~10 tokens/lesson); the old JSON never passes through a model |
| Prompt is optional | No `--prompt` = **standard regeneration** (progression rules + previous-version context only); with `--prompt` = **guided**, and the guidance carries explicit priority over naming/grouping/ordering preferences |
| Structure is unoverridable | 100 % LO coverage, min-4 understand lessons, unique names, numbering, standards input-order, assessments, pacing — recomputed by code every time; no prompt or model output can break them |
| Every run is re-validated | Full 8-invariant check on the finished document; structural failure raises instead of shipping |
| Diff is written for you | `regeneration.md` in the output folder shows exactly what changed vs the baseline |

## 2. Step-by-step logic per scope

### 2.1 FULL course (`--unit all`)

```
① load baseline input.json + outline.json
② compress old outline → context block:
     REGENERATION: … improved outline per user guidance; keep what was good; don't repeat …
     PREVIOUS UNIT 'Logical Reasoning And Argumentation': Logical Fallacies; Valid Arguments; …
     PREVIOUS UNIT 'Counting Combinatorics & Number Systems': … (one line per unit)
③ inject: raw.user_prompt = --prompt · raw._regen_context = block
   → course_header appends both → EVERY planning prompt (plan_parts, plan_chapters, titles) sees them
④ run the normal 8-node graph — NOTHING is locked; the model re-plans knowing the old structure
⑤ write new folder + regeneration.md (units before vs after)
```

**Real guided run** (`results/43LOs-regen-full-with-prompt`, prompt *"broader, real-world themed units"*):

```
Before: Logical Reasoning And Argumentation · Counting Combinatorics & Number Systems ·
        Sequences Recursive & Graph Theory · Voting Theory & Fair Division
After:  Critical Thinking And Persuasion · Counting Combinatorics & Codes Ciphers ·
        Growth Patterns & Networks Route · Elections And Fair Sharing
```

**Real standard run — no prompt** (`results/43LOs-regen-full-default`): still regenerates with
context alone; produced a different, valid 4-unit organisation ("Logical Reasoning Foundations",
"Number Systems And Digital Computing", …). 43/43 placed in both, validation clean.

### 2.2 ONE unit (`--unit N` or `--unit "Exact Name"`)

```
① load baseline; rebuild full pipeline state deterministically from outline.json
   (URN→id by input order; every LO's unit/lesson/rank/title read back — no LLM)
② LOCK all other units: their prior lesson name + position become their chapter/rank;
   their module titles are pre-filled into the titles map
③ target unit only: plan_chapters re-runs (fresh lesson groups) with context =
   "PREVIOUS LESSONS: …; PREVIOUS MODULE TITLES: …" + user prompt priority
④ whole course re-flows through pack_and_merge (min-4, packing, dedup, numbering)
⑤ titles re-run ONLY for packed parts containing target LOs; all others reuse prior titles
⑥ assemble + validate + regeneration.md (per-module before/after table)
```

**Real guided run** (`results/43LOs-regen-unit-with-prompt`, unit 2, prompt *"more application-focused lesson names"*):

```
Lessons before (7): Permutations And Combinations; Multiplication And Repetition; …
Lessons after  (6): Rankings Teams And Codes; Passwords And License Plates; Solving Mixed
                    Counting Problems; Detecting Errors In Data; Compressing And Encrypting
                    Data; Optimizing Algorithm Performance
L7  Multiplication Principle Basics   → Counting License Plate Options
L8  Permutations Of Distinct Objects  → Ranking Contest Winners
L10 Arrangements With Repetition      → Password Combination Counting
```

Lock proof (tested + measured): **31/31 non-target modules byte-identical** (unit, lesson name,
module title) to the baseline. Standard (no-prompt) variant: `results/43LOs-regen-unit-default`.

### 2.3 ONE lesson (`--unit N --lesson M` or exact lesson name)

```
① rebuild state, lock EVERYTHING (all units keep prior chapter/rank)
② deterministic re-flow reproduces the baseline structure
③ titles re-run for ONLY the selected lesson's modules, context = that lesson's previous titles
④ assemble + validate + regeneration.md (that lesson's title diff only)
```

**Real run** (`results/43LOs-regen-lesson-with-prompt`, unit 1 → lesson "Valid Arguments",
prompt *"more applied, real-world module titles"*):

```
L1 Symbolic Argument Construction → Courtroom Argument Building
L2 Modus Ponens And Tollens       → Detective-Style Deductive Reasoning
```

Everything else — placements, all lesson/unit names, all other titles — byte-locked (tested).

## 3. End-to-end example: one LO through a unit regeneration

`L8` ("Calculate permutations of distinct objects…") during the guided unit-2 regeneration:

```
baseline:  unit 'Counting Combinatorics & Number Systems' · lesson 'Permutations And
           Combinations' · title 'Permutations Of Distinct Objects'
① state rebuild   L8 ← urn …b1c4b83d; skill 'Permutations'; tier Foundational; prior placement read back
② lock check      L8's unit IS the target → eligible for re-planning
③ plan_chapters   context lists old lessons; model returns {L8 → lesson 'Rankings Teams And Codes', rank 1}
④ pack/merge      estimates unchanged (291w/14m, deterministic); lesson packed ≤2000w/60m; min-4 OK
⑤ titles          model returns {L8: 'Ranking Contest Winners'} — checked: unique in lesson, not banned
⑥ assemble        module JSON rebuilt; URN copied byte-for-byte from the id↔URN map
⑦ validate        43/43 coverage · numbering sequential · clean → shipped
```

## 4. Edge cases — behaviour and proof

| # | Edge case | Behaviour | Proof |
|---|---|---|---|
| 1 | No `--prompt` | Standard regeneration: context-only, USER GUIDANCE line omitted | `…-unit-default`, `…-full-default` live runs, both valid |
| 2 | Invalid/unrelated prompt ("buy pizza tomorrow") | Rejected BEFORE any model call with the user-facing message ("appears to be unrelated… e.g. 'reduce this unit to 4 lessons'") | prompt-guard tests + CLI smoke |
| 3 | Injection/override prompt (`<script>`, "ignore previous instructions", `{{…}}`) | Rejected: "contains content that is not allowed…" | 4 guard tests |
| 4 | Prompt > 2000 chars | Rejected with length message | guard test |
| 5 | `--unit 99` / wrong unit name | Exits with the numbered list of available units | test (`SystemExit`) |
| 6 | `--lesson 99` / wrong lesson name | Exits listing the unit's regenerable lessons | test |
| 7 | `--lesson` on Introduction/Apply/Review/Test/Semester | Impossible — selection only offers understand lessons; error text says these cannot be regenerated (STUDIOPE-94 exclusion) | `select_lesson` |
| 8 | Regenerated unit shrinks below 4 lessons | `pack_and_merge` merges it with the best adjacent unit — reported in `enforcement.log` and visible in `regeneration.md` | min-4 engine (same as generation) |
| 9 | Regenerated names collide (unit/lesson/module) | Casefold-aware uniquification adds skill-word differentiators, `(2)` last resort; `NAMES`/`TITLES` invariants re-checked | dedup tests |
| 10 | Standards-driven baseline | Code overrides model ordering on the regenerated scope too — input order preserved (STUDIOPE-243) | adversarial order test |
| 11 | Model omits some ids | Re-ask only the missing ids once → deterministic fallback + flag; run completes, `report.json.fallbacks` shows it | node defence loop |
| 12 | Provider timeout mid-regeneration | Affected call falls back deterministically; outline still valid; visible in `report.json.errors` | observed live (one `claude_cli` timeout on a full run → valid output, 12 fallback lesson names) |
| 13 | Structural invariant fails after regen | `RuntimeError` raised — nothing shipped (this would be a code bug, never retried against a model) | `regenerate_*` guard |
| 14 | `--lesson` with `--unit all` | Rejected: "--lesson requires a specific --unit" | CLI check |
| 15 | Undo | Use the baseline folder — regeneration never mutates it | by construction |
| 16 | Regenerating a regeneration | Works — any run folder with `input.json`+`outline.json` is a valid baseline (chains keep full lineage via `regeneration.md` baseline links) | folder contract |

## 5. Not covered (platform layer, by design)

LG-level regeneration (upstream of course outline) · slates · Studio save/undo DB lifecycle
(pending-review state, ACTIVE/SUPERSEDED trees, TITLES-undo, parallel-undo 409 handling,
STUDIOPE-300/340/341/530/532) — this engine's new-folder-per-run + immutable-baseline model is
the primitive those workflows persist.

## 6. Pointers

- Code: `outline/regen.py` (all three flows + note writers), `outline/prompt_guard.py`,
  CLI wiring in `outline/__main__.py`
- Tests: `tests/graph/test_regen.py` (lock proofs, context proof, selection errors),
  `tests/unit/test_prompt_guard.py`
- Evidence: `results/43LOs-regen-{unit,unit-default,lesson,full,full-default}-*/` each with
  `regeneration.md` diff; commands in `docs/SETUP-AND-RUN.md` §4b
