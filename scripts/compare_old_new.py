"""Extract old Berlin-graph responses to clean JSON and compare with new-pipeline runs, per LO.

Usage: python scripts/compare_old_new.py
Writes:
  runs/old-graph/outline-<n>.json      clean JSON extracted from berlin-tool-node/tool-response-*.txt
  runs/old-graph/outline-<n>.error.json when the old run failed
  runs/COMPARISON-<n>.md               structural + per-LO side-by-side (old vs latest new run for that input)
  runs/COMPARISON.md                   summary table across all sizes
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT))
from conftest import parse_sse  # noqa: E402
from outline.validate.invariants import check  # noqa: E402

OLD = {
    43: "tool-response-43-lg-new.txt",
    49: "tool-response-49-lgs-new.txt",
    94: "tool-response-94-lgs-new.txt",
}
OLD_TOKENS = {
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


def lo_index(outline: dict) -> dict[str, dict]:
    """urn -> {part, chapter, title, words, minutes}"""
    idx = {}
    for p in outline.get("children", []):
        for c in p["children"]:
            for m in c["children"]:
                u = m.get("learning_objective_urn")
                if u:
                    idx[u] = {
                        "part": p["title"]["en"],
                        "part_no": p["part_number"],
                        "chapter": c["title"]["en"],
                        "ch_no": c["chapter_number"],
                        "title": m["title"]["en"],
                        "words": m.get("estimated_word_count"),
                        "minutes": m.get("estimated_time_minutes"),
                        "skill": m.get("primary_skill"),
                        "tier": m.get("blooms_level"),
                    }
    return idx


def structure(outline: dict, urns: list[str]) -> dict:
    parts = outline.get("children", [])
    content = [p for p in parts if p.get("type") == "understand"]
    und = [c for p in content for c in p["children"] if c["type"] == "understand"]
    per_part = [
        sum(1 for c in p["children"] if c["type"] == "understand") for p in content
    ]
    idx = lo_index(outline)
    placed = list(idx)
    errs = check(outline, urns) if parts else ["NO OUTLINE"]
    return {
        "content_parts": len(content),
        "understand_chapters": len(und),
        "understand_per_part": per_part,
        "min_per_part": min(per_part, default=0),
        "los_per_chapter_avg": round(len(placed) / len(und), 2) if und else 0,
        "single_lo_chapters": sum(1 for c in und if len(c["children"]) == 1),
        "los_placed": len(placed),
        "missing": sorted(set(urns) - set(placed)),
        "total_parts": outline.get("total_parts"),
        "total_chapters": outline.get("total_chapters"),
        "pacing_overrun": outline.get("pacing_overrun"),
        "invariant_failures": errs,
        "part_names": [p["title"]["en"] for p in content],
        "chapter_names": [c["title"]["en"] for c in und],
    }


def latest_new_run(n: int) -> Path | None:
    cands = []
    for d in (ROOT / "runs").glob("*_claude_cli"):
        rep = json.loads((d / "report.json").read_text(encoding="utf-8"))
        if rep["n_los"] == n:
            cands.append(d)
    return sorted(cands)[-1] if cands else None


def md_table(headers, rows):
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
    return "\n".join(out)


def compare_one(n: int, old: dict, new_dir: Path | None, inp: dict) -> list[str]:
    urns = [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]
    text = {
        lo["learning_objective_urn"]: lo["objective"]
        for lo in inp["learning_objectives"]
    }
    old_ok = bool(old.get("children"))
    so = structure(old, urns) if old_ok else None
    new = (
        json.loads((new_dir / "outline.json").read_text(encoding="utf-8"))
        if new_dir
        else None
    )
    rep = (
        json.loads((new_dir / "report.json").read_text(encoding="utf-8"))
        if new_dir
        else None
    )
    sn = structure(new, urns) if new else None

    md = [f"# {n} LOs — old Berlin graph vs new LangGraph pipeline", ""]
    md += [
        f"- Input: `{inp['course_title']}` · {inp['grade_band']} · {inp['subject_area']} · {inp['course_outline_progression']}",
        f"- Old response: `berlin-tool-node/{OLD[n]}` → `runs/old-graph/outline-{n}.json`"
        + (
            ""
            if old_ok
            else f" — **FAILED**: {old.get('error_detail', old.get('status'))}"
        ),
        f"- New run: `{new_dir.name if new_dir else '(not run yet)'}`",
        "",
    ]
    md += ["## Structure", ""]
    rows = []
    keys = [
        ("content parts", "content_parts"),
        ("understand chapters", "understand_chapters"),
        ("understand per part", "understand_per_part"),
        ("min understand per part", "min_per_part"),
        ("avg LOs per chapter", "los_per_chapter_avg"),
        ("single-LO chapters", "single_lo_chapters"),
        ("LOs placed", "los_placed"),
        ("missing LOs", "missing"),
        ("total_parts", "total_parts"),
        ("total_chapters", "total_chapters"),
        ("pacing overrun", "pacing_overrun"),
        ("invariant failures", "invariant_failures"),
    ]
    for label, k in keys:
        ov = so.get(k) if so else "—"
        nv = sn.get(k) if sn else "—"
        if k == "missing":
            ov = len(ov) if isinstance(ov, list) else ov
            nv = len(nv) if isinstance(nv, list) else nv
        if k == "invariant_failures":
            ov = len(ov) if isinstance(ov, list) else ov
            nv = len(nv) if isinstance(nv, list) else nv
        rows.append([label, ov, nv])
    ot = OLD_TOKENS.get(n, {})
    rows += [
        ["LLM calls", ot.get("calls", "—"), rep["llm_calls"] if rep else "—"],
        [
            "completion tokens (model output)",
            ot.get("completion", "—"),
            rep["completion_tokens"] if rep else "—",
        ],
        [
            "largest single prompt (own tokens)",
            "22k–44k (planner forward)",
            (rep["max_prompt_tokens"] if rep else "—"),
        ],
        ["fallbacks", "n/a", rep["fallbacks"] if rep else "—"],
        ["wall time (s)", "n/a", round(rep["wall_ms"] / 1000) if rep else "—"],
    ]
    md += [md_table(["metric", "OLD", "NEW"], rows), ""]
    if so and so["invariant_failures"]:
        md += [
            "Old-graph invariant failures:",
            *[f"- {e}" for e in so["invariant_failures"][:12]],
            "",
        ]
    if sn and sn["invariant_failures"]:
        md += [
            "New-graph invariant failures:",
            *[f"- {e}" for e in sn["invariant_failures"][:12]],
            "",
        ]

    md += [
        "## Unit (part) names",
        "",
        md_table(
            ["#", "OLD", "NEW"],
            [
                [
                    i + 1,
                    (so["part_names"][i] if so and i < len(so["part_names"]) else ""),
                    (sn["part_names"][i] if sn and i < len(sn["part_names"]) else ""),
                ]
                for i in range(
                    max(
                        len(so["part_names"]) if so else 0,
                        len(sn["part_names"]) if sn else 0,
                    )
                )
            ],
        ),
        "",
    ]

    oi = lo_index(old) if old_ok else {}
    ni = lo_index(new) if new else {}
    md += [
        "## Per-LO placement and titles",
        "",
        "Same LO, old vs new: which unit/chapter it landed in and the module title generated.",
        "",
    ]
    rows = []
    moved = 0
    for i, u in enumerate(urns, 1):
        o, nw = oi.get(u), ni.get(u)
        rows.append(
            [
                i,
                text[u][:70],
                (o or {}).get("part", "—"),
                (o or {}).get("chapter", "—"),
                (o or {}).get("title", "—"),
                (nw or {}).get("part", "—"),
                (nw or {}).get("chapter", "—"),
                (nw or {}).get("title", "—"),
                (nw or {}).get("tier", "—"),
            ]
        )
    md += [
        md_table(
            [
                "#",
                "objective",
                "OLD unit",
                "OLD chapter",
                "OLD title",
                "NEW unit",
                "NEW chapter",
                "NEW title",
                "NEW tier",
            ],
            rows,
        ),
        "",
    ]
    if oi and ni:
        same_title = sum(
            1
            for u in urns
            if u in oi
            and u in ni
            and oi[u]["title"].casefold() == ni[u]["title"].casefold()
        )
        md += [
            "## Title agreement",
            "",
            f"- identical module titles old vs new: {same_title}/{len(urns)} (differences are expected — both are valid phrasings; judge quality, not equality)",
            "",
        ]
    return md


def main() -> None:
    (ROOT / "runs/old-graph").mkdir(parents=True, exist_ok=True)
    summary = []
    for n, fname in OLD.items():
        inp = json.loads(
            (ROOT / f"tests/fixtures/sample-input-{n}.json").read_text(encoding="utf-8")
        )
        try:
            old = parse_sse(ROOT / "berlin-tool-node" / fname)
        except Exception as exc:  # noqa: BLE001
            old = {"status": "unparseable", "error_detail": str(exc)}
        target = (
            ROOT
            / f"runs/old-graph/outline-{n}{'' if old.get('children') else '.error'}.json"
        )
        target.write_text(
            json.dumps(old, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        new_dir = latest_new_run(n)
        md = compare_one(n, old, new_dir, inp)
        if new_dir:  # comparison + old JSON live inside the run folder they compare
            (new_dir / "comparison-vs-old-graph.md").write_text(
                "\n".join(md), encoding="utf-8"
            )
            (new_dir / f"old-graph-outline-{n}.json").write_text(
                json.dumps(old, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        else:
            (ROOT / f"runs/COMPARISON-{n}.md").write_text(
                "\n".join(md), encoding="utf-8"
            )
        urns = [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]
        so = structure(old, urns) if old.get("children") else None
        sn = (
            structure(
                json.loads((new_dir / "outline.json").read_text(encoding="utf-8")), urns
            )
            if new_dir
            else None
        )
        summary.append(
            [
                n,
                "OLD",
                "failed" if not so else "ok",
                so and so["content_parts"],
                so and so["understand_chapters"],
                so and so["min_per_part"],
                so and so["los_placed"],
                so and len(so["missing"]),
                so and len(so["invariant_failures"]),
            ]
        )
        summary.append(
            [
                n,
                "NEW",
                "ok" if sn else "not run",
                sn and sn["content_parts"],
                sn and sn["understand_chapters"],
                sn and sn["min_per_part"],
                sn and sn["los_placed"],
                sn and len(sn["missing"]),
                sn and len(sn["invariant_failures"]),
            ]
        )
        print(
            f"compared {n}: -> {new_dir.name + '/comparison-vs-old-graph.md' if new_dir else f'runs/COMPARISON-{n}.md'}; {target.name}"
        )
    # new-only sizes
    for d in sorted((ROOT / "runs").glob("*_claude_cli")):
        rep = json.loads((d / "report.json").read_text(encoding="utf-8"))
        if rep["n_los"] in OLD:
            continue
        inp = json.loads((d / "input.json").read_text(encoding="utf-8"))
        urns = [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]
        sn = structure(
            json.loads((d / "outline.json").read_text(encoding="utf-8")), urns
        )
        summary.append(
            [
                rep["n_los"],
                "NEW",
                "ok",
                sn["content_parts"],
                sn["understand_chapters"],
                sn["min_per_part"],
                sn["los_placed"],
                len(sn["missing"]),
                len(sn["invariant_failures"]),
            ]
        )
    summary.sort(key=lambda r: (r[0], r[1]))
    out = [
        "# Summary — old Berlin graph vs new pipeline",
        "",
        md_table(
            [
                "LOs",
                "system",
                "status",
                "content parts",
                "understand chapters",
                "min/part",
                "LOs placed",
                "missing",
                "invariant failures",
            ],
            [[("" if v is None else v) for v in r] for r in summary],
        ),
        "",
        "Per-size detail: `<run folder>/comparison-vs-old-graph.md` (+ `old-graph-outline-<n>.json`) inside each 43/49/94 run folder. Old outputs as clean JSON also in `old-graph/`.",
    ]
    (ROOT / "runs/COMPARISON.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
