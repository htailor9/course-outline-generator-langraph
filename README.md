# Course Outline Generator (Python + LangGraph)

Turns a JSON list of K-12 learning objectives into a valid **DCIM course outline**
(Course → Units → Lessons → Modules) for Pearson PAICE Studio. Rebuild of the Berlin 4-node
graph that failed above ~50 LOs; this pipeline is live-verified from **43 to 1,000 LOs** with
zero dropped objectives across all four progression strategies.

**Core idea:** LLMs make the pedagogical decisions (grouping, naming, ordering) as ID-keyed
labels; Python owns the data, all counting/packing/merging, and builds the final JSON. Every
LLM call is schema-validated with a re-ask + deterministic fallback, so a run always ends in a
valid outline.

```
ingest → annotate(LLM ∥) → plan_parts(LLM) → plan_chapters(LLM ∥) → pack_and_merge(code)
       → titles(LLM ∥) → assemble(code) → validate(code)
```

## Quickstart

```powershell
py -3.13 -m venv .venv ; .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m pytest -q                                                  # 69 passed, 1 skipped
python -m outline generate tests\fixtures\sample-input-43.json --fake            # offline
python -m outline generate tests\fixtures\sample-input-43.json --provider claude_cli --model sonnet   # live, no key
```

Each run writes a timestamped folder under `runs/` with `input.json`, `outline.json`,
`report.json`, `enforcement.log`, and a human-readable `analysis.md`.

Regenerate a single unit of a prior run (others locked, previous version passed as context,
baseline kept as undo):

```powershell
python -m outline regenerate runs\<prior-run> --unit 2 --prompt "fresher lesson names" --provider claude_cli --model sonnet
python -m outline regenerate runs\<prior-run> --unit all --prompt "broader units"   # full course, prior outline as context
python -m outline regenerate runs\<prior-run> --unit 2 --lesson 3 --prompt "..."    # one lesson's module titles only
```

User prompts are validated first: injection/markup and unrelated prompts are rejected with a
clear message before any model call.

## Providers

`--provider anthropic | openai | bedrock_converse | claude_cli`

- `anthropic` — needs `ANTHROPIC_API_KEY`; per-role models in `config.yaml`
- `claude_cli` — headless `claude -p` on a Claude Code subscription; `--model sonnet|haiku|opus`
- `openai` / `bedrock_converse` — set that provider's model ids in `config.yaml` `models:`, e.g.
  `{default: gpt-4o, annotate: gpt-4o-mini, titles: gpt-4o-mini}`

## Guarantees (code-enforced, test-covered)

- Every input LO URN appears exactly once in the output (`unassigned_objective_urns: []`)
- ≥ 4 understand lessons per unit (deterministic adjacent-merge, STUDIOPE-291)
- Standards-driven mode: exact input order, zero reordering (STUDIOPE-243) — adversarially tested
- No duplicate unit names in a course, lesson names in a unit, or module names in a lesson —
  collisions get skill-word differentiators (STUDIOPE-446)
- `user_prompt` steers grouping/naming/ordering with explicit priority, but can never override
  coverage, standards order, or structural rules (live-verified: 3 units / ≤3-word names on demand)
- Lessons respect minutes/word budgets; numbering, totals, pacing (±5 %), and assessment
  metadata (STUDIOPE-8) are computed, never generated
- Output matches the legacy DCIM contract byte-for-byte on the golden 43-LO fixture

## Docs

| Doc | What |
|---|---|
| [docs/SIMPLE-GUIDE.md](docs/SIMPLE-GUIDE.md) | plain-language walkthrough: what the LLM does vs what Python does, with tiny examples |
| [docs/SETUP-AND-RUN.md](docs/SETUP-AND-RUN.md) | all setup, run, test, batch, comparison commands |
| [docs/DESIGN-Course-Outline-Generator-LangGraph.md](docs/DESIGN-Course-Outline-Generator-LangGraph.md) | the binding design |
| [docs/TEAM-WALKTHROUGH-43LOs.md](docs/TEAM-WALKTHROUGH-43LOs.md) | full logic, real 43-LO examples per agent type |
| [docs/REGENERATION.md](docs/REGENERATION.md) | regeneration flows: step-by-step logic, real end-to-end examples, all edge cases |
| [docs/ARCHITECTURE-CONTEXT-AND-BATCHING.md](docs/ARCHITECTURE-CONTEXT-AND-BATCHING.md) | deep-dive: batching, context carriers, ordering under concurrency, failure containment |
| [docs/SESSION-CONTEXT.md](docs/SESSION-CONTEXT.md) | current state, live results, decisions |
| [docs/BUILD-GUIDE-Course-Outline-Generator.md](docs/BUILD-GUIDE-Course-Outline-Generator.md) | build-from-scratch + production notes |

## Layout

```
outline/            package: nodes.py graph.py llm.py schemas.py state.py config.py report.py analysis.py
  prompts/          4 templates (annotate, plan_parts, plan_chapters, titles)
  rules/            deterministic core: blooms, estimates, packing, min-4 merging, structure
  assemble/         DCIM JSON builder, assessments, pacing
  validate/         7 output invariants
scripts/            make_synthetic.py · compare_old_new.py · compare_runs.py
tests/              unit · graph (e2e + scale, offline FakeLLM) · live (opt-in)
runs/               one timestamped folder per run · old-graph/ · synthetic-inputs/ · COMPARISON.md (gitignored)
results/            tracked evidence: 43-LO live runs for all 4 progressions + user_prompt test
berlin-tool-node/   legacy Berlin graph reference material (prompts, service, sample responses)
```
