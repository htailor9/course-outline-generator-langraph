# Session Context — Course Outline Generator (Berlin → Python + LangGraph)

> Read this first in a new session. It is the complete state of the work as of 2026-08-27 ~21:00.
> Repo: `C:\Users\a\Documents\Hiral\Berlin-Pearson`, branch `feat/outline-generator`.
> **Git state: 5 commits (docs + Tasks 0–3), everything after Task 3 is STAGED but UNCOMMITTED (user instruction: "do not commit anything and push").** `git diff --cached` shows all code.

---

## 1. What this project is

Pearson PAICE Studio "Course Outline Generation" (Jira STUDIOPE-6/93/301). Input = JSON of learning objectives (LOs/LGs) + course metadata; output = DCIM course outline JSON (Course → Parts/Units → Chapters/Lessons → Modules), 1 LO ↔ 1 module, ≥ 4 understand chapters per unit (merge undersized), chapters fit `minutes_per_lesson`/word limit, structural chapters (Intro/Apply/Review/Test, Semester A/B Review+Exam), estimates, pacing.

The user's existing system is a **Berlin** (Pearson's visual LangGraph builder) 4-node graph: `LearningObjectiveAnalyser → {Skills|Theme|Chronological|StandardsDriven}Planner → CourseOutlinePackAndMerge (FastAPI REST tool) → DCIMCourseOutlineGenerator`, GPT-5.2. Reference material in `berlin-tool-node/` (prompts, FastAPI service code, sample inputs 43/49/94/123, SSE responses, llmlogs).

**Why it was rebuilt:** measured from `llmlogs-94-lgs-new.json` — the Planner LLM re-serialised the 72-chapter tool payload and emitted only 2 parts/9 chapters (silent truncation), DCIM failure-guard fired. The DCIM node regenerates the whole JSON (13.6k output tokens at 43 LOs → ~90k at 300). Root cause: LLM used as a data bus + O(n) synthesizer.

## 2. Design (binding docs)

- `docs/DESIGN-Course-Outline-Generator-LangGraph.md` — **lean design, the authority**
- `docs/superpowers/specs/2026-08-27-course-outline-generator-langgraph-design.md` — full spec, diagnosis, 10 architecture answers, scaling tiers
- `docs/BUILD-GUIDE-Course-Outline-Generator.md` — from-scratch build guide + production notes
- `docs/superpowers/plans/2026-08-27-course-outline-generator.md` — 12-task implementation plan (executed)

Principles: LLMs return **ID-keyed deltas only** (`L17 → …`); Python owns data and builds the document; counting/packing/merging/numbering = code; every prompt bounded; every LLM node = validate → re-ask missing ids once → deterministic fallback with a flag.

Graph (`outline/graph.py`):
```
ingest[code] → annotate[LLM ∥ batches of 30] → plan_parts[LLM ×1 compact; skill-mode >300 LOs]
→ plan_chapters[LLM ∥ per unit] → pack_and_merge[code, ported from FastAPI service]
→ titles[LLM ∥ per unit] → assemble[code, DCIM JSON] → validate[code, 7 invariants] → END
```

## 3. Code layout (`outline/`)

| File | Role |
|---|---|
| `schemas.py` | Pydantic: `CourseRequest`, LLM outputs (`AnnotateOut`, `PartsOut`, `ChaptersOut`, `TitlesOut`), DCIM `Outline` |
| `state.py` | `LO`/`State` TypedDicts, reducers `merge_los` (flags union; `flags` key only when non-empty → read with `.get("flags", [])`), `merge_dict` |
| `config.py` | `Settings` (provider, models per role, batch_size 30, max_concurrency 5, skill_mode_threshold 300, timeouts, retries) + `load(config.yaml, **overrides)` |
| `llm.py` | `render(template, **vars)`; `LLM` (LangChain `init_chat_model` + `with_structured_output`, tenacity retry only on 429/5xx/timeouts); **`ClaudeCliLLM`** (provider `claude_cli`: headless `claude -p --json-schema`, uses local Claude Code subscription, no API key); `FakeLLM` (offline deterministic); `make_llm(settings)` |
| `nodes.py` | all nodes + `Send` fan-outs + `GUIDANCE` per progression (skills/theme/chronological/standards-driven with adjacency rule) + `course_header` (global context for per-unit calls) + `PipelineBug` |
| `prompts/*.md` | `annotate`, `plan_parts` (with `{columns}` legend, `{guidance}`), `plan_chapters`, `titles` — split on `---USER---` |
| `rules/` | `grade_band`, `blooms` (verb→tier table, lowest wins), `estimates`, `naming` (`skill_key`, merge/uniquify), `packing` (bin-pack ≤4 LOs, word+minute limits), `merging` (`enforce_min_4` + 2-part exception), `structure.build_structure` (full pack_and_merge core) |
| `assemble/` | `dcim.build` (reproduces golden byte-for-byte), `assessments` (per chapter type, optional `assessment` field), `pacing` (±5 %) |
| `validate/invariants.py` | `LO_COVERAGE, MIN4, SEMESTERS, ORDER, SUMS, TITLES(soft), LIMITS(soft)`; `BANNED` title regex |
| `report.py` | `build_report`, `make_run_dir`, `write` (input.json, outline.json, report.json, enforcement.log, analysis.md) |
| `analysis.py` | human-readable `analysis.md` per run (verdict, input, annotation stats, structure tables, pacing, LLM calls, quality signals) |
| `__main__.py` | CLI |
| `scripts/` | `make_synthetic.py N OUT` (synthetic inputs from fixtures, uuid5 URNs), `compare_old_new.py` (old Berlin vs new, per-LO), `compare_runs.py` |
| `tests/` | unit (rules/assemble/validate/llm/nodes), graph e2e (43/94/123 + scale 300/1000 + skewed-skill), live (opt-in) — **65 passed, 1 skipped** |

## 4. How to run

```powershell
.\.venv\Scripts\python.exe -m pytest -q                         # offline suite
.\.venv\Scripts\python.exe -m outline generate tests\fixtures\sample-input-94.json --fake        # offline
.\.venv\Scripts\python.exe -m outline generate tests\fixtures\sample-input-94.json --provider claude_cli --model sonnet   # live via subscription
.\.venv\Scripts\python.exe -m outline generate INPUT.json --provider anthropic     # needs ANTHROPIC_API_KEY; models in config.yaml
.\.venv\Scripts\python.exe scripts\compare_old_new.py           # refresh runs/COMPARISON*.md
```
Outputs → `runs/<YYYYMMDD-HHMMSS>_<N>LOs_<course>_<provider>/` (gitignored). `--out DIR` overrides. Venv is Python 3.13 (`py -3.13`); langgraph 1.2.x, langchain 1.3.x.

`runs/` layout (as of 2026-08-31):
```
runs/
  COMPARISON.md                          summary table: old Berlin graph vs new, all sizes
  old-graph/                             old Berlin SSE responses as clean JSON
    outline-43.json  outline-49.json  outline-94.error.json
  synthetic-inputs/                      generated inputs + the live batch driver
    input-synthetic-{150,175,200,250,300}LOs.json   batch.sh  batch.log
  20260827-203356_43LOs_Test-Math_claude_cli/       one folder per run:
    input.json  outline.json  report.json  enforcement.log  analysis.md
    comparison-vs-old-graph.md           per-LO old/new placement + titles (only where an old response exists: 43/49/94)
    old-graph-outline-43.json            the old response this run is compared against
  20260827-204050_49LOs_Math-test_claude_cli/
  20260827-204534_94LOs_Math-6A_claude_cli/
  20260827-205011_123LOs_Math-for-Middle-School_claude_cli/
  20260827-205613_150LOs_Synthetic-150_claude_cli/
  20260827-202320_43LOs_Test-Math_fake/
```
`scripts/compare_old_new.py` regenerates COMPARISON.md and the in-folder comparison files (writes `runs/COMPARISON-<n>.md` at top level only when no matching run folder exists).

`claude_cli` provider notes: model aliases `sonnet|haiku|opus`; tokens in `report.json` include Claude Code's own system prompt (~20–40k cached per call) — not comparable to API numbers; use `completion_tokens` and structure metrics instead.

## 5. Live results (Claude Sonnet via `claude_cli`, 2026-08-27)

| LOs | source | content parts | understand chapters | LOs placed | fallbacks | invariant failures | calls | wall |
|---|---|---|---|---|---|---|---|---|
| 43 | fixture (old: OK) | 4 | 25 | 43/43 | 0 | 0 | 14 | 186 s |
| 49 | fixture (old: **dropped 2 LOs**, 9 failures) | 3 | 20 | 49/49 | 0 | 0 | 12 | 195 s |
| 94 | fixture (old: **failed**) | 8 | 52 | 94/94 | 0 | 0 | 22 | 284 s |
| 123 | fixture, standards-driven | 7 | 65 | 123/123 | 0 | 0 | 21 | 277 s |
| 150 | synthetic | 12 | 85 | 150/150 | 0 | 0 | 32 | ~6 min |
| 175 | synthetic (2026-08-31) | 14 | 93 | 175/175 | 0 | 0 | 38 | 6.9 min |
| 200 | synthetic | 14 | 108 | 200/200 | 0 | 0 | 39 | 7.5 min |
| 250 | synthetic | 20 | 135 | 250/250 | 0 | 0 | 51 | 9.4 min |
| 300 | synthetic | 18 | 156 | 300/300 | 0 | 0 | 49 | 9.6 min |

All 9 live sizes valid, zero fallbacks, zero invariant failures. Offline FakeLLM additionally proves 1,000 LOs (max prompt 5.7k tokens). TL-facing before/after brief published as artifact "Course Outline Generator Rebuild" (source: scratchpad tl-briefing.html).

### Update 2026-08-31 → 09-01

- **Scale 400–1000 live (batch3)**: 400 ✅ clean (first skill-mode live run, 43 calls, 8.2 min), 500 ✅; 600/700/800/900/1000 completed structurally valid but with `WinError 206` (Windows ~32k command-line cap) forcing fallbacks on some per-unit calls. **Fixed**: `ClaudeCliLLM._invoke` now pipes the user prompt via stdin (staged); those sizes not re-run yet.
- **All 4 progression types live-tested** (43-LO variants in `runs/synthetic-inputs/input-43LOs-{theme,chrono,standards}.json` + the 123-LO standards fixture): skills ✅, theme ✅, chronological ✅, standards ✅.
- **Requirements gap check vs `C:\Users\a\Downloads\course_outline_requirements.md`** (STUDIOPE-91/93/147/171/243/291/8/446): two gaps found and FIXED —
  1. Standards-driven ordering was prompt-enforced only; an early 43-standards run had **20 order inversions** (STUDIOPE-243 critical). Now code-enforced (`plan_parts` sorts units by earliest input idx; `plan_chapters` overrides ranks with input idx in standards mode) + adversarial regression test. Live re-run: **0 inversions, exact linear match** (`runs/20260831-154750_43LOs_Test-Math-Standards_claude_cli`).
  2. `semester_exam` assessment scoring `auto` → `auto_and_teacher` (STUDIOPE-8).
  Remaining product-contract questions (not defects): Slate level not emitted (matches old graph contract); one Apply chapter per unit (spec wording plural).
- Suite now **66 passed, 1 skipped**. Run folders renamed to `<timestamp>_<N>LOs_<course>_<provider>`; per-size old-vs-new comparisons live inside the 43/49/94 run folders; synthetic inputs under `runs/synthetic-inputs/`.
- New team doc: `docs/TEAM-WALKTHROUGH-43LOs.md` (full logic, real 43-LO example per agent type, L4 end-to-end trace). Artifact updated with scale results, progression coverage, standards-fix panel, and the L4 trace.

### Update 2026-09-01 (pre-commit)

- **Duplicate-name requirement implemented** (STUDIOPE-446 class): scan found duplicate lesson names within units in 7 outlines (standards-43, 600–1000). Fixed: `uniquify_chapter_names` now runs across the whole unit (not per packing bucket) and is casefold-aware; new `uniquify_part_names` guarantees unique unit names; new soft `NAMES` invariant; 3 regression tests. Module-in-lesson uniqueness was already enforced.
- **`user_prompt` explicit priority** added to `course_header` (overrides grouping/naming/ordering preferences, never coverage/standards-order/structure). **Live-verified**: 43-LO run with "exactly 3 units, ≤3-word names, real-world lesson names" → honoured on all three counts, 43/43 placed. Stored at `results/43LOs-user-prompt/`.
- **`results/` folder (tracked)**: 43-LO live runs for all 4 progression types + the user-prompt test, each with input/outline/report/enforcement/analysis (+ old-graph comparison for skills). `runs/` stays gitignored.
- `.env.example` added (all providers; app does not auto-load it); `docs/SETUP-AND-RUN.md` gained a full Bedrock section; README rewritten with guarantees + doc index.
- Old Berlin docs (`DCIM_…Technical_Documentation.md`, `Implementation_Guide_Deterministic_Packing.md`) removed from the repo (originals still in git history and `berlin-tool-node/` holds the legacy reference material). `Chat_gpt_plane.md` gitignored.
- Codebase formatted with **black**; suite 69 passed, 1 skipped. Regeneration flow (unit-level + undo) remains unbuilt.

Comparison artefacts: `runs/COMPARISON.md` (summary) + `comparison-vs-old-graph.md` and `old-graph-outline-<n>.json` inside each 43/49/94 run folder (structure + unit names + per-LO old/new placement & titles); `runs/old-graph/` holds the extracted old JSONs.

Old-vs-new observations: old ≈ 1 LO per chapter (43 chapters for 43 LOs); new packs ~2.5 LOs/chapter by time/word limits (knob: `MAX_LOS_PER_CHAPTER`, plan_chapters "~3 per chapter"). Old 7 units at 43 → new 4 (planner made 7, min-4 merge collapsed 3). Old 49 numbering broken (`[2,2,3,…]`, `[11,2,3,…]`) — LLM-typed JSON; new numbering is code.

## 6. Process record

Executed via superpowers subagent-driven development: fresh implementer + reviewer per task, fix rounds (Tasks 5,6,7,8 one each), final opus whole-branch review (0 Critical, 6 Important → one fix wave, re-review clean). Ledger with every ruling: `.superpowers/sdd/2026-08-27-course-outline-generator/progress.md` (gitignored; keep until committed). Key rulings: Python 3.13; naming guard for single-letter part names; `unassigned_objective_urns`/`split_notes` wired to validation; `merge_los` flags semantics; `ingest` upper-cases progression enum; skill chunk cap 40 (design) not 10.

## 7. Known gaps / deferred

- Prompt quality only tested live on skills-based (43/49/94/150) and standards-driven (123); theme/chronological prompts untested live.
- `LIMITS`/`TITLES` are soft invariants (reported, not fatal).
- No API/queue/DB; regeneration/undo/Excel export/graph view not built (design supports via id-keyed state).
- Deferred minors listed in the ledger (estimates tested MS band only, uniquify mutates input, etc.).
- `config.yaml` ships Claude model ids; `--provider openai|bedrock_converse` needs `models:` overridden.

## 8. Immediate next steps (suggested)

1. `git add -A`-free commit of staged work: `git commit -m "feat: LangGraph course outline generator (MVP)"` — only when user says so.
2. Optionally run 175–300 live (`runs/batch.sh` pattern, or one at a time).
3. Decide chapter density knob (1 LO/chapter like old vs packed) and unit granularity guidance with product.
4. Live-test theme/chronological progression inputs.
5. Wire into Berlin as a single Tool node calling this pipeline (see BUILD-GUIDE §H).
