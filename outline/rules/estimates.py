"""Word and time estimates from grade band x Bloom's tier."""

from outline.rules.grade_band import normalize

GRADE_WORD_LIMITS = {"K-2": 400, "3-5": 600, "MS": 2000, "HS": 2250}
GRADE_WORD_RANGES = {
    "K-2": (50, 200),
    "3-5": (50, 300),
    "MS": (200, 750),
    "HS": (300, 1000),
}
BLOOMS_TIME_RANGES = {
    "Foundational": (12, 18),
    "Intermediate": (15, 22),
    "Advanced": (20, 28),
}


def word_limit(grade_band: str) -> int:
    return GRADE_WORD_LIMITS[normalize(grade_band)]


def estimate_minutes(tier: str) -> int:
    low, high = BLOOMS_TIME_RANGES.get(tier, BLOOMS_TIME_RANGES["Foundational"])
    if tier == "Foundational":
        return low + 2
    if tier == "Intermediate":
        return (low + high) // 2
    return max(low, high - 2)


def estimate_words(grade_band: str, tier: str) -> int:
    low, high = GRADE_WORD_RANGES[normalize(grade_band)]
    span = high - low
    if tier == "Foundational":
        return low + max(1, span // 6)
    if tier == "Intermediate":
        return low + span // 2
    return high - max(1, span // 6)
