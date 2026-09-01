"""CLI: python -m outline generate INPUT.json [--provider ...] [--out out/] [--fake]"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from outline.config import load
from outline.graph import build_graph
from outline.llm import FakeLLM, make_llm
from outline.report import make_run_dir, write


async def _run(args) -> None:
    settings = load(args.config, provider=args.provider, batch_size=args.batch_size)
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
    app = build_graph(llm, settings)
    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    cfg = {
        "configurable": {
            "llm": llm,
            "settings": settings,
            "thread_id": f"run-{int(time.time())}",
        },
        "max_concurrency": settings.max_concurrency,
    }
    t0 = time.perf_counter()
    async for event in app.astream(
        {"raw_input": raw}, config=cfg, stream_mode="updates"
    ):
        for node, update in event.items():
            extra = ""
            if node == "ingest":
                extra = (
                    f"{len(update['los'])} objectives, {len(update['batches'])} batches"
                )
            elif node == "plan_parts":
                extra = f"{len(update['parts'])} units"
            elif node == "pack_and_merge":
                extra = f"{update['packed']['num_content_parts']} parts / {update['packed']['content_chapter_count']} chapters"
            print(f"[{time.perf_counter() - t0:6.1f}s] {node:15s} {extra}")
    final = await app.aget_state(cfg)
    provider = "fake" if args.fake else settings.provider
    if args.out:
        run_dir, run_id = Path(args.out), Path(args.out).name
    else:
        run_dir, run_id = make_run_dir(
            Path(args.runs_dir),
            raw.get("course_title", "course"),
            provider,
            n_los=len(raw.get("learning_objectives", [])),
        )
    rep = write(
        run_dir,
        final.values,
        provider,
        int((time.perf_counter() - t0) * 1000),
        input_payload=raw,
        run_id=run_id,
        settings=settings,
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
        "--model",
        default=None,
        help="override model id for ALL roles (e.g. sonnet, claude-sonnet-4-5)",
    )
    g.add_argument("--config", default="config.yaml")
    g.add_argument(
        "--out",
        default=None,
        help="explicit output folder (default: runs/<timestamp>_<course>_<provider>/)",
    )
    g.add_argument(
        "--runs-dir", default="runs", help="root folder for timestamped runs"
    )
    g.add_argument("--batch-size", type=int, default=None)
    g.add_argument("--fake", action="store_true", help="use FakeLLM (offline)")
    args = p.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
