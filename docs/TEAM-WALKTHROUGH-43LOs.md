# Course Outline Generator — Full Logic Walkthrough (43-LO run, real data)

> Team reference. Every example below is taken from an actual live run of the new Python + LangGraph
> pipeline on `Test_Math` (43 learning objectives, grade band MS, Math, 60 min/lesson, 5 lessons/week ×
> 36 weeks, Claude Sonnet). Run folders: `runs/*_43LOs_Test-Math_*`.
> Companion brief (before/after, results): artifact "Course Outline Generator Rebuild".

---

## 0. The graph at a glance

```
ingest[code] → annotate[LLM ∥ batches] → plan_parts[LLM ×1] → plan_chapters[LLM ∥ per unit]
→ pack_and_merge[code] → titles[LLM ∥ per unit] → assemble[code] → validate[code] → END
```

Two laws, everywhere:

1. **LLMs return ID-keyed decisions, never data.** Prompts contain projections (`L17 | Evidence Analysis |
   Intermediate`); replies contain labels (`L17 → unit P3`). No prompt ever contains a URN.
2. **Python owns the single copy of the data and builds the document.** LangGraph state holds one `los`
   dict; parallel nodes return patches merged by reducers; the DCIM JSON is written once, by code.

Every LLM node runs the same defence loop:
```
call with Pydantic schema → code checks id coverage → re-ask ONLY missing ids once
→ still missing? deterministic fallback + flag (pipeline never crashes, report shows what fell back)
```

---

## 1. Agent/node taxonomy

| # | Node | Type | Model calls (43 LOs) | Decides | Never does |
|---|---|---|---|---|---|
| 1 | `ingest` | code gate | 0 | ids, budget, batches | — |
| 2 | `annotate` | **LLM extractor** | 2 (∥ batches of 30) | verb + skill per LO | classify Bloom's (code table does) |
| 3 | `plan_parts` | **LLM planner (global)** | 1 | unit names + LO→unit | see LO full text at scale (skill rows > 300) |
| 4 | `plan_chapters` | **LLM planner (per unit)** | 7 (∥) | lesson groups + order rank | see another unit's LOs |
| 5 | `pack_and_merge` | code rules engine | 0 | estimates, packing, min-4 merge, numbering | anything creative |
| 6 | `titles` | **LLM namer (per unit)** | 4 (∥, post-merge) | module titles | move/renumber anything |
| 7 | `assemble` | code builder | 0 | full DCIM JSON, structural lessons, assessments, pacing | — |
| 8 | `validate` | code gate | 0 | 7 invariants pass/fail | "fix" anything silently |

None of the LLM nodes is an autonomous agent: no LLM picks a route, calls a tool, or sees the graph.
Routing (which progression rules apply) is a prompt-template switch in Python.

Old Berlin graph mapping: Analyser(classifier) → #2+tier table · Planner(routerSubAgent) → #3+#4 ·
PackAndMerge(REST tool) → #5 in-process · DCIM(synthesizer) → #6 creative sliver + #7 code.

---

## 2. Step-by-step with real 43-LO data

### Step 1 — `ingest` (code)

```
input.json ─▶ CourseRequest (Pydantic) ─▶
L1 ← urn:pearson:learninggoal:36612654-… "Construct valid logical arguments using premises and conclusions…" idx=0
L2 ← urn:…:047dedb2-…                    "Apply rules of inference including modus ponens and modus tollens…" idx=1
L3 ← urn:…:2663de0d-…                    "Identify logical fallacies in arguments including ad hominem…"      idx=2
…L43
budget  = { total_lesson_days: 5×36 = 180, word_limit: 2000 }   # MS band table
batches = [[L1…L30], [L31…L43]]
```

`idx` (input position) is stamped here and is the ordering ground truth for the rest of the run.
The id↔URN map never leaves Python.

### Step 2 — `annotate` (LLM extractor, 2 parallel batches)

Prompt (per batch, ~1.2k tokens):
```
COURSE: Test_Math | grade band MS | Math | SKILLS_BASED_PROGRESSION
CALENDAR: 5 lessons/week x 36 weeks = 180 lesson days; 60 min/lesson; chapter word limit 2000
Rows: id | objective
L1 | Construct valid logical arguments using premises and conclusions in symbolic form.
L3 | Identify logical fallacies in arguments including ad hominem, straw man, and false dilemma.
…
```
Reply (schema `AnnotateOut`, id-keyed):
```json
{"items":[{"id":"L1","verb":"construct","primary_skill":"Logical Arguments"},
          {"id":"L3","verb":"identify","primary_skill":"Logical Fallacies"}, …]}
```
Code then assigns Bloom's tier from the verb table (lowest tier wins; ported verbatim from the old
Analyser prompt): `construct → Intermediate`, `identify → Foundational`, `evaluate → Advanced`.
Run outcome: 9 Foundational / 28 Intermediate / 6 Advanced.

*Failure path*: if the model skipped `L7`, code re-asks with only `L7`'s row; if still missing,
fallback `verb = first word, skill = first content words`, flag `annotate_fallback`. (0 fallbacks in
all live runs.)

### Step 3 — `plan_parts` (LLM planner, the one global call)

Prompt rows are a projection, ~20 tokens/LO (~1.3k total at 43 LOs):
```
PROGRESSION: SKILLS-BASED. A unit is a coherent skill domain… order Foundational→Advanced…
Items (43): id | skill | tier
L1 | Logical Arguments | Intermediate
L3 | Logical Fallacies | Foundational
L7 | Multiplication Principle | Intermediate
…
```
Reply (schema `PartsOut`): 7 units —
`Logical Reasoning And Argumentation [L3,L1,L2,…] · Counting And Combinatorics [L7,L8,L9,…] ·
Number Systems And Information Theory · Sequences And Recursive Processes · Graph Theory And Networks ·
Voting Theory And Social Choice · Fair Division Methods`.

Scale note: above `skill_mode_threshold` (300) the rows become one line per **unique skill**
(`S1 | Ratios | 14 | Fou9/Int5 | example…`), skills > 40 LOs pre-split by tier, and code expands the
chosen skills back to LO ids — so this prompt never grows linearly (proven live to 1000 LOs).

*Coverage defence*: every id must land in exactly one unit — first-wins on duplicates, one re-ask for
missing ids listing the existing units, then fallback by `skill_key` match, flag `plan_parts_fallback`.

### Step 4 — `plan_chapters` (LLM planner, 7 parallel unit calls)

Each `Send()` payload = that unit's LOs only + shared 5-line header (course, calendar, progression rules,
**all** unit names for naming coherence, THIS UNIT marker). Full LO text is included now — the set is small.

Reply for unit 1 (schema `ChaptersOut`):
```json
{"assignments":[
 {"id":"L3","chapter_name":"Logical Fallacies","order_rank":1},
 {"id":"L1","chapter_name":"Valid Arguments","order_rank":2},
 {"id":"L2","chapter_name":"Valid Arguments","order_rank":2},
 {"id":"L5","chapter_name":"Quantifiers And Counterexamples","order_rank":3},
 {"id":"L6","chapter_name":"Quantifiers And Counterexamples","order_rank":3},
 {"id":"L4","chapter_name":"Truth Tables","order_rank":4}]}
```
Foundational fallacies first, the Advanced truth-tables LO last — the model's pedagogy, expressed only
as labels.

**Standards-driven override (STUDIOPE-243, code-enforced):** in standards mode the model's ranks are
discarded — code sets `rank = input idx`, units are re-sorted by their earliest LO's input position, and
non-adjacent groupings auto-split. Adversarial test: a fake model returning reversed units and descending
ranks still yields exact input order. Live re-run proof: 20 inversions before the fix → **0 after**.

### Step 5 — `pack_and_merge` (code — the old FastAPI algorithm, in-process)

```
sort unit's LOs by (rank, chapter, idx)               # deterministic; idx breaks all ties
estimates (grade band × tier):  Foundational 291w/14m · Intermediate 475w/18m · Advanced 659w/26m
bin-pack per chapter group:     close a lesson when +LO would exceed 2000 words OR 60 min OR 4 LOs
  "Valid Arguments" = L1(475/18) + L2(475/18) = 950w/36m  ✓ one lesson
min-4 rule (STUDIOPE-291) from the run's enforcement.log:
  MERGE: 'Counting And Combinatorics' (3 lessons) + 'Number Systems And Information Theory' (4) → 7
  MERGE: 'Sequences And Recursive Processes' (3) + 'Graph Theory And Networks' (3) → 6
  MERGE: 'Fair Division Methods' (3) + 'Voting Theory And Social Choice' (5) → 8
  FINAL: 4 units, all ≥ 4 understand lessons               # 7 planned units → 4 shipped
number everything: units from 2, lessons from 2, modules from 1 — loops, not a model
validate coverage: 43 in / 43 placed / 0 dup / 0 missing  (a miss here raises PipelineBug — a code bug,
never retried against an LLM)
```

### Step 6 — `titles` (LLM namer, 4 parallel unit calls)

Rows: `chapter | id | objective | skill`. Reply is a title map:
```json
{"modules":[{"id":"L1","title":"Symbolic Argument Construction"},
            {"id":"L2","title":"Modus Ponens And Tollens"},
            {"id":"L3","title":"Spotting Logical Fallacies"},
            {"id":"L4","title":"Evaluating Argument Validity"}, …]}
```
Code rejects: duplicates within a lesson, title == lesson name, banned patterns (`Part 2`, `Module 3`,
`Practice`, `Continued`…). Rejected ids re-asked once → fallback `"<Skill>: <Verb>"` + flag.
43-run quality: 43/43 distinct, avg 3.1 words, 0 generic.

### Step 7 — `assemble` (code)

Builds the DCIM JSON exactly to the Berlin contract (byte-equal to the old graph's 43-LO golden output
in tests): Part 1 Course Overview (Course Guide + Course Introduction) → each content unit =
Introduction lesson + understand lessons + Apply + Review + Part Test → Semester A/B (Review + Exam).
Attaches assessment metadata per lesson type (STUDIOPE-8):

| Lesson type | assessment |
|---|---|
| understand | Quick Check · auto · multiple_choice |
| apply | Sample Work · teacher · dropbox |
| review | Unit Online Practice · auto · multiple_choice |
| test | Unit Test · auto_and_teacher |
| semester_review | Semester Online Practice · auto |
| semester_exam | Semester Exam · auto_and_teacher |
| intro/overview | none (Quick Check prohibited there) |

Totals: `total_parts = 1 + 4 + 2 = 7`, `total_chapters = 46`; pacing 46 ≤ 180+9 → under-filled note in
`split_notes`; `unassigned_objective_urns` computed from real validation (always `[]` on a clean run).

### Step 8 — `validate` (code)

Seven invariants over the finished document: `LO_COVERAGE` (every URN exactly once, duplicates by count),
`MIN4`, `SEMESTERS` (overview first, understand middle, two semester parts last), `ORDER` (sequential
numbering), `SUMS` (lesson totals = Σ module estimates; part/chapter totals), `TITLES` (soft),
`LIMITS` (soft). Structural failure → `PipelineBug`. 43-run result: `[]`.

### One LO, end to end — `L4` from input JSON to shipped module

Who touches it at each step; its URN appears exactly twice — entering Python and leaving it.

```
① INPUT      { "learning_objective_urn": "urn:pearson:learninggoal:265c1167-4a37-4a95-988f-fb786edbbb07",
               "objective": "Evaluate the validity of deductive arguments using truth tables and logical equivalences." }

② INGEST     → id L4, idx 3 · URN parked in Python's id↔URN map · never enters a prompt again    [code]

③ ANNOTATE   row:   L4 | Evaluate the validity of deductive arguments using truth tables…        [LLM]
             reply: {id:"L4", verb:"evaluate", primary_skill:"Deductive Validity"}
             tier:  "evaluate" ∈ Advanced verb list → Advanced                                    [code]

④ PLAN_PARTS row:   L4 | Deductive Validity | Advanced   (~20 tokens of L4)                      [LLM]
             reply: L4 ∈ unit "Logical Reasoning And Argumentation"

⑤ PLAN_CHAPTERS (unit 1 call only)                                                               [LLM]
             reply: {id:"L4", chapter_name:"Truth Tables", order_rank:4}    ← Advanced last

⑥ PACK_AND_MERGE                                                                                 [code]
             sort key (rank=4, "Truth Tables", idx=3) → last lesson of the unit
             estimates (MS × Advanced): 659 words · 26 min ≤ 2000w/60m → fits
             numbering: part_number=2 · chapter_number=5 · module_number assigned

⑦ TITLES     row:   Truth Tables | L4 | Evaluate the validity… | Deductive Validity              [LLM]
             reply: {id:"L4", title:"Evaluating Argument Validity"}
             checks: ≠ lesson name ✓ · unique in lesson ✓ · not banned ✓                          [code]

⑧ ASSEMBLE — final JSON exactly as shipped in outline.json:                                      [code]
   { "label":"chapter", "type":"understand", "chapter_number":5, "title":{"en":"Truth Tables"},
     "chapter_estimated_word_count":1318, "chapter_estimated_time_minutes":52,
     "assessment":{"type":"Quick Check","scoring":"auto","delivery":"multiple_choice"},
     "children":[ …,
       { "label":"module", "type":"understand", "module_number":2,
         "title":{"en":"Evaluating Argument Validity"},
         "learning_objective_urn":"urn:pearson:learninggoal:265c1167-4a37-4a95-988f-fb786edbbb07",  ← byte-identical
         "estimated_word_count":659, "estimated_time_minutes":26,
         "primary_skill":"Deductive Validity", "blooms_level":"Advanced" } ] }

⑨ VALIDATE   URN counted exactly once ✓ · lesson 1318w/52m = Σ modules ✓ → run valid             [code]
```

Three LLM calls saw projections of L4 and returned five labels (verb, skill, unit, lesson+rank, title);
code did everything else — tier, order, estimates, numbering, assessment, JSON, verification.

---

## 3. Ordering & context under parallel execution

- **Order is data, owned by code.** `idx` from ingest + one deterministic sort `(rank, chapter, idx)`.
  LLMs attach labels; they cannot move rows. Numbering is assigned by loops after packing — the old
  graph's `[11, 2, 3…]` bug is unrepresentable.
- **Parallel safety by disjoint slices.** Each `Send()` owns a disjoint id set; workers return patches;
  the `merge_los` reducer merges per-id (flags unioned). No shared mutable state, no locks; results are
  identical whatever order branches finish.
- **Shared context = the 5-line course header** (COURSE · CALENDAR · PROGRESSION rules · all UNIT names ·
  THIS UNIT, plus USER GUIDANCE on regeneration). ~150 tokens is the entire global context a worker
  needs; whole-course operations (merging, totals, pacing) deliberately happen in code after fan-in.

## 4. The four progression types (all live-tested)

| Type | Unit logic | Ordering rule | Live proof |
|---|---|---|---|
| SKILLS_BASED | skill domains | Foundational→Advanced, prerequisites | 43…1000 LOs valid |
| STANDARDS_DRIVEN | contiguous input blocks | **input order, code-enforced, 0 inversions** | 123 + 43 (post-fix) |
| THEME_BASED | big ideas (cross-standard blending allowed) | foundational→specialised themes | 43 valid |
| CHRONOLOGICAL | eras/stages | earliest→latest | 43 valid |

The only thing that changes between types is the PROGRESSION paragraph injected into the planner prompts —
plus the standards-mode code override above.

## 5. Where to look

- Code: `outline/` (nodes, rules, assemble, validate, prompts) · tests: `pytest -q` (66 passed)
- Any run: `runs/<timestamp>_<N>LOs_<course>_<provider>/` → `input.json`, `outline.json`, `report.json`,
  `enforcement.log`, `analysis.md` (+ `comparison-vs-old-graph.md` for 43/49/94)
- Run one: `python -m outline generate INPUT.json --provider claude_cli --model sonnet` (subscription)
  or `--provider anthropic|openai|bedrock_converse` (API keys) or `--fake` (offline)
- Design: `docs/DESIGN-Course-Outline-Generator-LangGraph.md` · state handoff: `docs/SESSION-CONTEXT.md`
