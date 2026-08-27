from outline.rules.blooms import tier_for
from outline.rules.grade_band import normalize


def test_lowest_tier_wins_for_duplicate_verbs():
    assert tier_for("compare") == "Foundational"     # in Foundational and elsewhere
    assert tier_for("analyze") == "Intermediate"
    assert tier_for("design") == "Advanced"
    assert tier_for("Summarize") == "Foundational"   # case-insensitive; also in Advanced list
    assert tier_for("categorize") == "Intermediate"  # Intermediate and Advanced → Intermediate


def test_unknown_verb_defaults_foundational():
    assert tier_for("zork") == "Foundational"
    assert tier_for("") == "Foundational"


def test_multiword_verbs():
    assert tier_for("figure out") == "Intermediate"
    assert tier_for("set up") == "Advanced"


def test_grade_band_normalize():
    assert normalize("MS") == "MS"
    assert normalize("Grade 6") == "MS"
    assert normalize("k-2") == "K-2"
    assert normalize("Grade 4") == "3-5"
    assert normalize("9-12") == "HS"
    assert normalize("") == "3-5"
