"""Build an N-objective synthetic input from the fixture inputs (URNs re-minted, texts lightly varied)."""

import json
import sys
import uuid
from pathlib import Path

FIX = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
SOURCES = [
    "sample-input-43.json",
    "sample-input-49.json",
    "sample-input-94.json",
    "sample-input-123.json",
]


def main(n: int, out: Path) -> None:
    pool = []
    for name in SOURCES:
        pool.extend(
            json.loads((FIX / name).read_text(encoding="utf-8"))["learning_objectives"]
        )
    base = json.loads((FIX / "sample-input-94.json").read_text(encoding="utf-8"))
    los = []
    for i in range(n):
        src = pool[i % len(pool)]
        suffix = f" (variant {i // len(pool) + 1})" if i >= len(pool) else ""
        los.append(
            {
                "learning_objective_urn": f"urn:pearson:learninggoal:{uuid.uuid5(uuid.NAMESPACE_URL, f'syn-{i}')}",
                "objective": src["objective"] + suffix,
            }
        )
    weeks = max(base["course_duration_weeks"], (n * 2) // base["lessons_per_week"] + 8)
    data = {
        **base,
        "course_title": f"Synthetic_{n}",
        "course_duration_weeks": weeks,
        "learning_objectives": los,
    }
    data.pop("PearsonExtSSOSession", None)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(int(sys.argv[1]), Path(sys.argv[2]))
