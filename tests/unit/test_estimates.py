from outline.rules.estimates import word_limit, estimate_words, estimate_minutes


def test_minutes_by_tier():
    assert estimate_minutes("Foundational") == 14
    assert estimate_minutes("Intermediate") == 18
    assert estimate_minutes("Advanced") == 26


def test_words_ms_matches_golden():
    # golden 43-LO output: MS Foundational=291, Intermediate=475, Advanced=659
    assert estimate_words("MS", "Foundational") == 291
    assert estimate_words("MS", "Intermediate") == 475
    assert estimate_words("MS", "Advanced") == 659


def test_word_limit():
    assert word_limit("MS") == 2000
    assert word_limit("Grade 3") == 600
