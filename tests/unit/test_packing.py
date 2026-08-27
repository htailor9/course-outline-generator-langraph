from outline.rules.packing import pack_chapters


def lo(words, mins, chap="C", skill="S"):
    return {"estimated_word_count": words, "estimated_time_minutes": mins,
            "source_chapter_name": chap, "primary_skill": skill, "urn": f"u{words}{mins}"}


def test_splits_on_time_limit():
    chapters = pack_chapters([lo(100, 30), lo(100, 30), lo(100, 30)], word_limit=2000, minute_limit=60)
    assert [len(c["learning_objectives"]) for c in chapters] == [2, 1]
    assert chapters[0]["chapter_estimated_time_minutes"] == 60


def test_splits_on_density_4():
    chapters = pack_chapters([lo(10, 1) for _ in range(9)], word_limit=2000, minute_limit=60)
    assert [len(c["learning_objectives"]) for c in chapters] == [4, 4, 1]


def test_module_numbers_reset_per_chapter():
    chapters = pack_chapters([lo(10, 1) for _ in range(5)], word_limit=2000, minute_limit=60)
    assert [m["module_number"] for m in chapters[0]["learning_objectives"]] == [1, 2, 3, 4]
    assert chapters[1]["learning_objectives"][0]["module_number"] == 1


def test_chapter_name_from_sources():
    chapters = pack_chapters([lo(10, 1, "A"), lo(10, 1, "B")], word_limit=2000, minute_limit=60)
    assert chapters[0]["chapter_name"] == "A and B"
