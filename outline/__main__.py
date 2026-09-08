"""CLI: python -m outline generate INPUT.json | regenerate RUN_DIR --unit ... [--fake]

Thin transport wrapper over outline.service — printing, flags and exit codes live here;
orchestration lives in service.py (shared with the REST API).
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from outline.config import load
from outline.llm import FakeLLM, make_llm
from outline.service import run_generation, run_regeneration


def _settings_and_llm(args):
    settings = load(
        args.config,
        provider=args.provider,
        batch_size=getattr(args, "batch_size", None),
    )
    if args.provider == "claude_cli" and not args.model:
        settings.models = {
            "default": "sonnet",
            "annotate": "sonnet",
            "titles": "sonnet",
        }
    if args.model:
        settings.models = {
            "default": args.model,
            "annotate": args.model,
            "titles": args.model,
        }
    llm = FakeLLM() if args.fake else make_llm(settings)
    provider = "fake" if args.fake else settings.provider
    settings.provider = provider
    return settings, llm


async def _run(args) -> None:
    settings, llm = _settings_and_llm(args)
    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    t0 = time.perf_counter()

    def printer(node: str, update: dict) -> None:
        extra = ""
        if node == "ingest":
            extra = f"{len(update['los'])} objectives, {len(update['batches'])} batches"
        elif node == "plan_parts":
            extra = f"{len(update['parts'])} units"
        elif node == "pack_and_merge":
            extra = (
                f"{update['packed']['num_content_parts']} parts / "
                f"{update['packed']['content_chapter_count']} chapters"
            )
        print(f"[{time.perf_counter() - t0:6.1f}s] {node:15s} {extra}")

    run_dir, rep = await run_generation(
        raw,
        settings,
        llm,
        runs_dir=Path(args.runs_dir),
        out=Path(args.out) if args.out else None,
        progress=printer,
    )
    print(
        json.dumps(
            {
                k: rep[k]
                for k in (
                    "n_los",
                    "llm_calls",
                    "prompt_tokens",
                    "completion_tokens",
                    "max_prompt_tokens",
                    "fallbacks",
                    "validation",
                )
            },
            indent=2,
        )
    )
    print(
        f"run folder: {run_dir}  (input.json, outline.json, report.json, enforcement.log, analysis.md)"
    )
    if rep["errors"]:
        for err in rep["errors"]:
            print(err)
        sys.exit(2)


async def _regen(args) -> None:
    settings, llm = _settings_and_llm(args)
    run_dir, rep = await run_regeneration(
        Path(args.run_dir),
        args.unit,
        args.lesson,
        args.prompt,
        settings,
        llm,
        runs_dir=Path(args.runs_dir),
    )
    print(
        json.dumps(
            {k: rep[k] for k in ("n_los", "llm_calls", "fallbacks", "validation")},
            indent=2,
        )
    )
    print(f"regenerated -> {run_dir}  (+ regeneration.md)")
    if rep["errors"]:
        for err in rep["errors"]:
            print(err)
        sys.exit(2)


def main() -> None:
    p = argparse.ArgumentParser(prog="outline")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("input")
    g.add_argument(
        "--provider",
        default=None,
        choices=["anthropic", "openai", "bedrock_converse", "claude_cli"],
        help="claude_cli = headless `claude -p` using the local Claude Code subscription (no API key)",
    )
    g.add_argument(
        "--model", default=None, help="override model id for ALL roles (e.g. sonnet)"
    )
    g.add_argument("--config", default="config.yaml")
    g.add_argument(
        "--out",
        default=None,
        help="explicit output folder (default: runs/<timestamp>.../)",
    )
    g.add_argument(
        "--runs-dir", default="runs", help="root folder for timestamped runs"
    )
    g.add_argument("--batch-size", type=int, default=None)
    g.add_argument("--fake", action="store_true", help="use FakeLLM (offline)")

    r = sub.add_parser(
        "regenerate", help="regenerate a prior run: --unit all | N [--lesson M]"
    )
    r.add_argument(
        "run_dir", help="prior run folder (contains input.json + outline.json)"
    )
    r.add_argument(
        "--unit",
        required=True,
        help="content-unit number (1-based), exact unit name, or 'all' for full-course "
        "regeneration with the previous outline passed as context",
    )
    r.add_argument(
        "--lesson",
        default=None,
        help="regenerate ONLY this lesson's module titles (number or exact name) within --unit; "
        "not combinable with --unit all",
    )
    r.add_argument(
        "--prompt",
        default=None,
        help="user guidance (priority) for the regenerated scope",
    )
    r.add_argument(
        "--provider",
        default=None,
        choices=["anthropic", "openai", "bedrock_converse", "claude_cli"],
    )
    r.add_argument("--model", default=None)
    r.add_argument("--config", default="config.yaml")
    r.add_argument("--runs-dir", default="runs")
    r.add_argument("--fake", action="store_true", help="use FakeLLM (offline)")

    args = p.parse_args()
    asyncio.run(_regen(args) if args.cmd == "regenerate" else _run(args))


if __name__ == "__main__":
    main()
