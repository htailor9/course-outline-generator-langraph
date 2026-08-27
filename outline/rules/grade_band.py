"""Normalise raw grade-band strings to K-2 | 3-5 | MS | HS."""


def normalize(grade_band: str | None) -> str:
    if not grade_band:
        return "3-5"
    raw = grade_band.strip().lower()
    if raw in ("k-2", "3-5", "ms", "hs"):
        return {"k-2": "K-2", "3-5": "3-5", "ms": "MS", "hs": "HS"}[raw]
    if any(k in raw for k in ["k-2", "k_2", "k2", "kindergarten", "grade 1", "grade 2", "grade1", "grade2"]):
        return "K-2"
    if any(k in raw for k in ["3-5", "3_5", "grade 3", "grade 4", "grade 5", "grade3", "grade4", "grade5", "elem"]):
        return "3-5"
    if any(k in raw for k in ["ms", "middle", "6-8", "6_8", "k6-8", "grade 6", "grade 7", "grade 8", "grade6", "grade7", "grade8"]):
        return "MS"
    if any(k in raw for k in ["hs", "high", "9-12", "9_12", "grade 9", "grade 10", "grade 11", "grade 12", "grade9", "grade10", "grade11", "grade12"]):
        return "HS"
    return "3-5"
