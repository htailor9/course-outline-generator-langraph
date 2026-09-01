"""Compare new-pipeline runs against old Berlin graph responses and each other.

Usage: python scripts/compare_runs.py  (scans runs/*claude_cli*, berlin-tool-node/tool-response-*.txt)
Writes runs/COMPARISON.md
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from conftest import parse_sse  # noqa: E402

sys.path.insert(0, str(ROOT))
from outline.validate.invariants import check  # noqa: E402

OLD = {
    43: ROOT / "berlin-tool-node/tool-response-43-lg-new.txt",
    49: ROOT / "berlin-tool-node/tool-response-49-lgs-new.txt",
    94: ROOT / "berlin-tool-node/tool-response-94-lgs-new.txt",
}
OLD_TOKENS = {  # from llmlogs-*.json (prompt, completion) per node, measured earlier
    43: {
        "calls": 4,
        "prompt": 5658 + 5488 + 22373 + 17441,
        "completion": 3507 + 6091 + 13883 + 13603,
    },
    94: {
        "calls": 4,
        "prompt": 8554 + 9159 + 43708 + 15523,
        "completion": 7382 + 12765 + 11965 + 135,
    },
}


def summarize(outline: dict, input_urns: list[str]) -> dict:
    parts = outline.get("children", [])
    content = [p for p in parts if p.get("type") == "understand"]
    und = [c for p in content for c in p["children"] if c["type"] == "understand"]
    titles = [m["title"]["en"] for c in und for m in c["children"]]
    placed = [
        m.get("learning_objective_urn")
        for p in parts
        for c in p["children"]
        for m in c["children"]
        if m.get("learning_objective_urn")
    ]
    errs = check(outline, input_urns) if parts else ["NO OUTLINE"]
    return {
        "status": outline.get("status", "ok"),
        "parts_total": outline.get("total_parts"),
        "content_parts": len(content),
        "chapters_total": outline.get("total_chapters"),
        "understand_chapters": len(und),
        "min_understand_per_part": min(
            (
                sum(1 for c in p["children"] if c["type"] == "understand")
                for p in content
            ),
            default=0,
        ),
        "los_placed": len(placed),
        "los_unique": len(set(placed)),
        "los_expected": len(input_urns),
        "missing": len(set(input_urns) - set(placed)),
        "duplicates": sum(1 for u, n in Counter(placed).items() if n > 1),
        "titles_distinct": f"{len(set(t.casefold() for t in titles))}/{len(titles)}",
        "avg_title_words": (
            round(sum(len(t.split()) for t in titles) / len(titles), 2) if titles else 0
        ),
        "pacing_overrun": outline.get("pacing_overrun"),
        "invariant_failures": len(errs),
        "failures": errs[:3],
    }


def main() -> None:
    rows = []
    # old graph
    for n, path in OLD.items():
        inp = json.loads(
            (ROOT / f"tests/fixtures/sample-input-{n}.json").read_text(encoding="utf-8")
        )
        urns = [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]
        try:
            old = parse_sse(path)
        except Exception as exc:  # noqa: BLE001
            old = {"status": f"unparseable: {exc}"}
        s = (
            summarize(old, urns)
            if old.get("children")
            else {"status": old.get("status") or old.get("error_detail", "failed")[:80]}
        )
        s.update({"system": "OLD Berlin graph", "n_los": n, **OLD_TOKENS.get(n, {})})
        rows.append(s)
    # new runs
    for d in sorted((ROOT / "runs").glob("*_claude_cli")):
        rep = json.loads((d / "report.json").read_text(encoding="utf-8"))
        outline = json.loads((d / "outline.json").read_text(encoding="utf-8"))
        inp = json.loads((d / "input.json").read_text(encoding="utf-8"))
        urns = [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]
        s = summarize(outline, urns)
        s.update(
            {
                "system": "NEW LangGraph",
                "n_los": rep["n_los"],
                "calls": rep["llm_calls"],
                "prompt": rep["prompt_tokens"],
                "completion": rep["completion_tokens"],
                "max_prompt": rep["max_prompt_tokens"],
                "wall_s": round(rep["wall_ms"] / 1000),
                "fallbacks": rep["fallbacks"],
                "run": d.name,
            }
        )
        rows.append(s)
    rows.sort(key=lambda r: (r["n_los"], r["system"]))

    cols = [
        "n_los",
        "system",
        "status",
        "content_parts",
        "understand_chapters",
        "min_understand_per_part",
        "los_placed",
        "los_expected",
        "missing",
        "duplicates",
        "titles_distinct",
        "avg_title_words",
        "pacing_overrun",
        "invariant_failures",
        "calls",
        "completion",
        "max_prompt",
        "wall_s",
        "fallbacks",
    ]
    md = [
        "# Old Berlin graph vs new LangGraph pipeline",
        "",
        "Old token numbers are from `llmlogs-*.json`; new `prompt` totals include Claude Code CLI system-prompt overhead (~20–40k cached tokens per call) and are not comparable — compare `completion` (what the model had to write) and `max_prompt` instead.",
        "",
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for r in rows:
        md.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    md += ["", "## Notes", ""]
    for r in rows:
        if r.get("failures"):
            md.append(f"- {r['n_los']} {r['system']}: {r['failures']}")
    (ROOT / "runs/COMPARISON.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
