# Live Results — 43 Learning Objectives, all four progression types

Verified outputs of the Course Outline Generator (Python + LangGraph) on the `Test_Math` 43-LO input,
run live on **Claude Sonnet** via the `claude_cli` provider. Copied from the gitignored `runs/` folder
so the evidence travels with the repo.

| Folder | Progression | Source run | Result |
|---|---|---|---|
| `43LOs-skills-based/` | SKILLS_BASED_PROGRESSION | 2026-08-27 20:33 | ✅ valid · 43/43 placed · 0 fallbacks · 14 calls · 3.1 min |
| `43LOs-standards-driven/` | STANDARDS_DRIVEN_PROGRESSION | 2026-08-31 15:47 (**post ordering-fix**) | ✅ valid · 43/43 · **0 order inversions vs input** (STUDIOPE-243) · 17 calls |
| `43LOs-theme-based/` | THEME_BASED_PROGRESSION | 2026-08-31 11:35 | ✅ valid · 43/43 · 0 fallbacks |
| `43LOs-chronological/` | CHRONOLOGICAL_PROGRESSION | 2026-08-31 11:37 | ✅ valid · 43/43 · 0 fallbacks |
| `43LOs-user-prompt/` | SKILLS_BASED + `user_prompt` priority test | 2026-09-01 11:10 | ✅ valid · 43/43 · prompt honoured: exactly 3 units, all names ≤ 3 words, real-world lesson names |
| `43LOs-regen-unit-with-prompt/` | UNIT regeneration, guided (unit 2, prompt: application-focused lesson names) | 2026-09-01 17:25 | ✅ valid · others locked · regeneration.md title diff |
| `43LOs-regen-unit-default/` | UNIT regeneration, standard (unit 2, NO prompt — context only) | 2026-09-01 17:27 | ✅ valid · others locked |
| `43LOs-regen-lesson-with-prompt/` | LESSON regeneration (unit 1, lesson 'Valid Arguments', prompt: applied real-world titles) | 2026-09-01 17:27 | ✅ valid · only that lesson's module titles changed |
| `43LOs-regen-full-with-prompt/` | FULL-course regeneration, guided (previous outline as context + prompt: broader real-world units) | 2026-09-01 17:31 | ✅ valid · 43/43 · units before/after in regeneration.md |
| `43LOs-regen-full-default/` | FULL-course regeneration, standard (previous outline as context, NO prompt) | 2026-09-01 17:34 | ✅ valid · 43/43 |

Each folder contains:

- `input.json` — the request (only `course_outline_progression`/title differ between the four)
- `outline.json` — the DCIM course outline produced
- `report.json` — metrics: LLM calls, tokens, per-node breakdown, fallbacks, invariant results, pacing
- `enforcement.log` — deterministic pack / min-4 merge decisions
- `analysis.md` — human-readable run analysis (verdict, structure tables, quality signals)
- `comparison-vs-old-graph.md` + `old-graph-outline-43.json` (skills folder only) — per-LO comparison
  against the legacy Berlin graph's output on the same input

Notes:

- `report.json → prompt_tokens` under `claude_cli` includes Claude Code's own system prompt
  (~20–40k cached per call); judge `completion_tokens` and the structure metrics instead.
- The standards run predating the ordering fix (2026-08-31 11:38, 20 inversions) is intentionally NOT
  included; the shipped folder is the post-fix run proving exact input-order preservation.
- Reproduce any of these: `python -m outline generate results/43LOs-<type>/input.json --provider claude_cli --model sonnet`

