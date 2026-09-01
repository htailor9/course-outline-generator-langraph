"""Deterministic naming helpers (ported from course_outline_structure_service.py)."""

import re
from collections import OrderedDict

MAX_PART_NAME_WORDS = 6
STOP_WORDS = {
    "a",
    "an",
    "the",
    "of",
    "in",
    "for",
    "to",
    "by",
    "on",
    "with",
    "from",
    "that",
    "this",
    "their",
    "its",
    "and",
    "or",
    "is",
    "are",
    "be",
    "been",
    "being",
    "was",
    "were",
    "will",
    "can",
    "could",
    "should",
    "would",
    "may",
    "might",
    "has",
    "have",
    "had",
    "do",
    "does",
    "did",
    "using",
    "use",
    "related",
    "concept",
    "concepts",
}
_CONJ = {"and", "or", "the", "of", "in", "for", "to", "a"}


def _singular(w: str) -> str:
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 3 and w.endswith("es") and not w.endswith("ses"):
        return w[:-2] if w[:-2].endswith(("sh", "ch", "x")) else w[:-1]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def skill_key(skill: str) -> str:
    words = re.findall(r"[a-z0-9]+", (skill or "").lower())
    words = [_singular(w) for w in words if w not in STOP_WORDS]
    return " ".join(sorted(words)) or (skill or "").strip().lower()


def chapter_base_name(bucket: list[dict]) -> str:
    names = list(OrderedDict.fromkeys(lo["source_chapter_name"] for lo in bucket))
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} and Related Concepts"


def merge_part_names(first: str, second: str) -> str:
    if first == second:
        return first
    if second.lower() in first.lower():
        return first
    if first.lower() in second.lower():
        return second
    wa, wb = first.split(), second.split()
    while len(wa) > 1 and wa[-1].lower() in _CONJ:
        wa.pop()
    while len(wb) > 1 and wb[-1].lower() in _CONJ:
        wb.pop()
    combined = f"{' '.join(wa)} & {' '.join(wb)}"
    if len(combined.split()) <= MAX_PART_NAME_WORDS:
        return combined
    sa = " ".join([w for w in wa if w.lower() not in _CONJ][:2])
    sb = " ".join([w for w in wb if w.lower() not in _CONJ][:2])
    return f"{sa} & {sb}"


def _differentiator(chapter_los: list[dict], base_name: str) -> str:
    base = {w.lower() for w in base_name.split()}
    novel: list[str] = []
    for lo in chapter_los:
        for word in (lo.get("primary_skill") or "").split():
            clean = word.strip(".,;:()")
            if (
                clean.lower() not in base
                and clean.lower() not in STOP_WORDS
                and clean.title() not in novel
            ):
                novel.append(clean.title())
    return " ".join(novel[:2])


def uniquify_part_names(parts: list[dict]) -> list[dict]:
    """Make duplicate part (unit) names unique across the course, mirroring chapter uniquification:
    prefer a skill-word differentiator from the part's own LOs, fall back to a numeric suffix.
    """
    from collections import Counter

    counts = Counter(p["part_name"].strip().casefold() for p in parts)
    seen: dict[str, int] = {}
    used: set[str] = set()
    for p in parts:
        name = p["part_name"]
        key = name.strip().casefold()
        if counts[key] <= 1 and key not in used:
            used.add(key)
            continue
        occ = seen.get(key, 0) + 1
        seen[key] = occ
        if occ == 1 and key not in used:
            used.add(key)
            continue
        los = [
            lo for c in p.get("chapters", []) for lo in c.get("learning_objectives", [])
        ]
        diff = _differentiator(los, base_name=name)
        new = f"{name} - {diff}" if diff else f"{name} ({max(occ, 2)})"
        n = 2
        while new.strip().casefold() in used:
            n += 1
            new = f"{name} ({n})"
        p["part_name"] = new
        used.add(new.strip().casefold())
    return parts


def uniquify_chapter_names(chapters: list[dict]) -> list[dict]:
    # All comparisons casefolded — "Multi Digit" and "Multi digit" are the same name.
    counts: dict[str, int] = {}
    for c in chapters:
        key = c["chapter_name"].strip().casefold()
        counts[key] = counts.get(key, 0) + 1
    seen: dict[str, int] = {}
    used: set[str] = set()
    for c in chapters:
        name = c["chapter_name"]
        key = name.strip().casefold()
        if counts[key] <= 1 and key not in used:
            used.add(key)
            continue
        occ = seen.get(key, 0) + 1
        seen[key] = occ
        if occ == 1 and key not in used:
            used.add(key)
            continue
        diff = _differentiator(c.get("learning_objectives", []), name)
        new = f"{name} - {diff}" if diff else f"{name} ({max(occ, 2)})"
        if new.strip().casefold() in used:
            new = f"{name} ({max(occ, 2)})"
        n = 2
        while new.strip().casefold() in used:
            n += 1
            new = f"{name} ({n})"
        c["chapter_name"] = new
        used.add(new.strip().casefold())
    return chapters
