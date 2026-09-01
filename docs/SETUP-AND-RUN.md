# Setup & Execution Guide

Every command needed to install, test, run, and analyse the Course Outline Generator on a fresh machine.
Commands are PowerShell (Windows); the venv-relative `python` works the same from Git Bash with `/` paths.

---

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| Python **3.11 – 3.13** | Built and tested on 3.13 (`py -3.13`). 3.14 untested. |
| Git | repo lives on branch `feat/outline-generator` |
| One model provider | Anthropic / OpenAI / Bedrock API key, **or** Claude Code CLI installed (subscription, no key) |

## 2. Install

```powershell
cd C:\Users\a\Documents\Hiral\Berlin-Pearson
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Verify:

```powershell
python -m pytest -q          # expect: 69 passed, 1 skipped (live test skips without key)
```

## 3. Configure

`config.yaml` (repo root) — defaults:

```yaml
provider: anthropic            # anthropic | openai | bedrock_converse | claude_cli
models:                        # per-role; roles: default, annotate, titles (plan_* use default)
  default: claude-sonnet-4-5
  annotate: claude-haiku-4-5
  titles: claude-haiku-4-5
batch_size: 30                 # LOs per annotate call
max_concurrency: 5             # parallel LLM calls
skill_mode_threshold: 300      # >N LOs → unit planning switches to skill-level rows
llm_timeout_seconds: 90
transport_retries: 3
```

Credentials per provider:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."            # provider: anthropic
$env:OPENAI_API_KEY    = "sk-..."                # provider: openai  (+ set OpenAI model ids in config.yaml)
$env:AWS_PROFILE = "..." ; $env:AWS_REGION = "us-east-1"   # provider: bedrock_converse (+ Bedrock model ids)
# provider: claude_cli → no key; uses the local `claude` CLI / Claude Code subscription
```

Non-Anthropic providers need matching model ids, e.g. `models: {default: gpt-4o, annotate: gpt-4o-mini, titles: gpt-4o-mini}`.

### Running on AWS Bedrock

Uses `langchain-aws` `ChatBedrockConverse` (already installed). Credentials come from the standard AWS
chain — env vars, `aws configure` profile, or an assumed role. The model must be enabled for your
account/region in the Bedrock console (Model access).

If your AWS access comes from SAML, configure AWS credentials first. The helper below accepts a
SAML assertion from `AWS_SAML_ASSERTION`, a local text file, or a hidden prompt; it does not store the
assertion in this repository. By default it writes the same AWS `default` profile as the standalone
AWS helper; `--profile` and `--region` are optional overrides.

```powershell
# optional: set the assertion in this shell instead of pasting it into the hidden prompt
$env:AWS_SAML_ASSERTION = "<base64-saml-response>"

python scripts\aws_saml_login.py --account-choice 3
$env:AWS_REGION = "us-east-1"
```

Available `--account-choice` values match the internal SAML roles used by the standalone AWS helper:
`1` paice-dev-nonprd, `2` itec-pearsonauthoringframework-nonprd, `3` contentmlresearch-sand,
`4` itec-pearsonauthoringframework-prd, `5` connexus-api-sand, `6` connexus-apiint-nonprod,
`7` connectionseducation-prod. For a different role, use `--account-id` and `--role-name` together.

```powershell
$env:AWS_REGION = "us-east-1"          # or AWS_DEFAULT_REGION
# credentials can come from the default profile, a named AWS_PROFILE, or AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY [/ AWS_SESSION_TOKEN]
```

`config.yaml`:

```yaml
provider: bedrock_converse
models:                                # Bedrock model IDs (check exact ids in your Bedrock console)
  default: us.anthropic.claude-sonnet-4-5-20250929-v1:0
  annotate: us.anthropic.claude-haiku-4-5-20251001-v1:0
  titles: us.anthropic.claude-haiku-4-5-20251001-v1:0
```

Run:

```powershell
python -m outline generate tests\fixtures\sample-input-43.json --provider bedrock_converse
# or without editing config.yaml, one model for all roles:
python -m outline generate tests\fixtures\sample-input-43.json --provider bedrock_converse --model us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

Notes: structured output uses Bedrock's Converse tool-calling — works with Claude models on Bedrock;
throttling (`ThrottlingException`) is retried automatically, auth/access errors are not (fix Model
access or credentials). Verified paths in code; live Bedrock smoke not yet run — first run should be
the 43-LO fixture.

## 4. Generate a course outline

```powershell
# offline smoke (no model, deterministic FakeLLM)
python -m outline generate tests\fixtures\sample-input-43.json --fake

# live via Claude Code subscription (recommended for testing; model alias sonnet|haiku|opus)
python -m outline generate tests\fixtures\sample-input-43.json --provider claude_cli --model sonnet

# live via API key (uses config.yaml models per role)
python -m outline generate tests\fixtures\sample-input-94.json --provider anthropic

# useful flags
#   --model X        override the model for ALL roles
#   --batch-size N   annotate batch size
#   --config PATH    alternate config.yaml
#   --out DIR        explicit output folder (default: timestamped under runs/)
#   --runs-dir DIR   root for timestamped run folders (default: runs)
```

Exit codes: `0` success · `2` finished but some LLM calls errored (see `report.json → errors`).

### Output — one folder per run

```
runs/<YYYYMMDD-HHMMSS>_<N>LOs_<course>_<provider>/
  input.json        request as received
  outline.json      DCIM course outline (the deliverable)
  report.json       metrics: calls, tokens, per-node, fallbacks, invariants, pacing, run_id
  enforcement.log   pack/min-4-merge decisions
  analysis.md       human-readable run analysis (verdict, structure tables, quality signals)
  comparison-vs-old-graph.md + old-graph-outline-<n>.json   (43/49/94 only)
```

Note on `claude_cli` token numbers: `prompt_tokens` includes Claude Code's own system prompt
(~20–40k cached per call). Judge `completion_tokens` and structure metrics, not prompt totals.

### Input format

```json
{ "course_title": "Test_Math", "grade_band": "MS", "subject_area": "Math",
  "minutes_per_lesson": 60, "lessons_per_week": 5, "course_duration_weeks": 36,
  "course_outline_progression": "SKILLS_BASED_PROGRESSION",
  "learning_objectives": [ {"learning_objective_urn": "urn:...", "objective": "..."} ],
  "user_prompt": null }
```

`course_outline_progression` ∈ `SKILLS_BASED_PROGRESSION | STANDARDS_DRIVEN_PROGRESSION |
THEME_BASED_PROGRESSION | CHRONOLOGICAL_PROGRESSION` (case-insensitive; standards mode enforces
input order in code). Ready-made progression variants: `runs\synthetic-inputs\input-43LOs-{theme,chrono,standards}.json`.

## 5. Tests

```powershell
python -m pytest -q                                   # full offline suite (unit + graph, FakeLLM)
python -m pytest tests\unit -q                        # rules/assemble/validate/llm/nodes only
python -m pytest tests\graph\test_end_to_end.py -q    # e2e incl. standards-order regression
python -m pytest tests\graph\test_scale.py -q         # 300 + 1000 LO scale (offline, ~2 s)
python -m pytest -m live                              # 1 real-provider smoke (needs ANTHROPIC_API_KEY)
```

## 6. Synthetic inputs & batch runs

```powershell
# build an N-LO input from the fixtures (unique uuid5 URNs)
python scripts\make_synthetic.py 500 runs\synthetic-inputs\input-synthetic-500LOs.json

# run a size ladder sequentially in the background (Git Bash)
bash runs/synthetic-inputs/batch2.sh                  # see batch*.sh for the pattern
```

## 7. Compare against the old Berlin graph

```powershell
python scripts\compare_old_new.py
# → refreshes runs\COMPARISON.md (summary, all sizes)
# → writes comparison-vs-old-graph.md + old-graph-outline-<n>.json inside the 43/49/94 run folders
# → extracts old SSE responses to clean JSON under runs\old-graph\
```

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `66 passed` becomes failures after edits | run `python -m pytest -q` from repo root with the venv active |
| CLI exit 2, `errors` in report | provider auth/limits; non-retryable errors are not retried by design |
| `WinError 206` in old run logs | fixed: prompts now go to `claude -p` via stdin; re-run affected sizes |
| `--provider openai` → model-not-found | set OpenAI model ids in `config.yaml` `models:` |
| fallback flags in `report.json → fallbacks` | model missed ids twice; outline is still valid — inspect the flagged LOs |
| find any run later | folders are `runs\<timestamp>_<N>LOs_...`; `report.json → run_id` matches |

## 9. Key documents

- `docs/DESIGN-Course-Outline-Generator-LangGraph.md` — the binding design
- `docs/TEAM-WALKTHROUGH-43LOs.md` — full logic with real 43-LO examples per agent type
- `docs/SESSION-CONTEXT.md` — current project state, results, decisions
- `docs/BUILD-GUIDE-Course-Outline-Generator.md` — from-scratch build + production notes
- Artifact "Course Outline Generator Rebuild" — TL-facing before/after brief
