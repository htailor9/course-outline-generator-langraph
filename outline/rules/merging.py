"""Merge undersized parts until every part has >= 4 understand chapters (or the 2-part exception)."""

import copy

from outline.rules.naming import merge_part_names, uniquify_chapter_names

MINIMUM_UNDERSTAND_CHAPTERS = 4


def _best_adjacent(parts: list[dict], index: int) -> int | None:
    cands: list[tuple[int, int]] = []
    if index > 0:
        cands.append((index - 1, len(parts[index - 1]["chapters"])))
    if index < len(parts) - 1:
        cands.append((index + 1, len(parts[index + 1]["chapters"])))
    if not cands:
        return None
    cands.sort(key=lambda c: (c[1], -c[0]))
    return cands[0][0]


def _merge(parts: list[dict], src: int, dst: int) -> list[dict]:
    first, second = sorted([src, dst])
    a, b = parts[first], parts[second]
    merged = {
        "part_name": merge_part_names(a["part_name"], b["part_name"]),
        "chapters": uniquify_chapter_names(
            copy.deepcopy(a["chapters"]) + copy.deepcopy(b["chapters"])
        ),
    }
    return [
        merged if i == first else copy.deepcopy(p)
        for i, p in enumerate(parts)
        if i != second
    ]


def enforce_min_4(parts: list[dict]) -> tuple[list[dict], list[str]]:
    log: list[str] = []
    parts = copy.deepcopy(parts)
    changed = True
    while changed:
        changed = False
        for i, p in enumerate(parts):
            n = len(p["chapters"])
            if n >= MINIMUM_UNDERSTAND_CHAPTERS:
                continue
            adj = _best_adjacent(parts, i)
            if adj is None:
                log.append(
                    f"WARNING: Part '{p['part_name']}' has {n} chapters and no adjacent part."
                )
                continue
            if (
                len(parts) == 2
                and n + len(parts[adj]["chapters"]) < MINIMUM_UNDERSTAND_CHAPTERS
            ):
                log.append(
                    f"EXCEPTION: Part '{p['part_name']}' has {n} chapters; combined pair would still have "
                    f"{n + len(parts[adj]['chapters'])} chapters (< 4). Accepted as-is."
                )
                continue
            log.append(
                f"MERGE: Part '{p['part_name']}' ({n} chapters) merged with '{parts[adj]['part_name']}' "
                f"({len(parts[adj]['chapters'])} chapters)"
            )
            parts = _merge(parts, i, adj)
            m = min(i, adj)
            log.append(
                f"RESULT: Part '{parts[m]['part_name']}' now has {len(parts[m]['chapters'])} chapters"
            )
            changed = True
            break
    for p in parts:
        n = len(p["chapters"])
        log.append(
            f"FINAL: Part '{p['part_name']}' - {n} understand chapters {'OK' if n >= 4 else 'WARNING'}"
        )
    return parts, log
