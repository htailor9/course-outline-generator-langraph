from hypothesis import given, settings, strategies as st

from outline.rules.structure import build_structure

COURSE = {"grade_band": "MS", "minutes_per_lesson": 60}
BUDGET = {"word_limit": 2000, "total_lesson_days": 180}


def make_los(n, chapter_of=lambda i: f"Ch{i // 3}", tier_of=lambda i: "Intermediate"):
    return {
        f"L{i}": {
            "id": f"L{i}",
            "urn": f"urn:{i}",
            "text": f"Objective {i}",
            "idx": i,
            "primary_skill": f"Skill {i // 3}",
            "tier": tier_of(i),
            "chapter": chapter_of(i),
            "rank": i // 3 + 1,
        }
        for i in range(n)
    }


def all_urns(packed):
    return [
        lo["urn"]
        for p in packed["parts"]
        for c in p["chapters"]
        for lo in c["learning_objectives"]
    ]


def test_basic_shape_and_numbering():
    los = make_los(24)
    parts = [
        {"part_name": "Unit A", "ids": [f"L{i}" for i in range(12)]},
        {"part_name": "Unit B", "ids": [f"L{i}" for i in range(12, 24)]},
    ]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert [p["part_number"] for p in packed["parts"]] == [2, 3]
    assert packed["parts"][0]["chapters"][0]["chapter_number"] == 2
    assert packed["parts"][0]["chapters"][0]["chapter_type"] == "understand"
    assert packed["num_content_parts"] == 2
    assert packed["content_chapter_count"] == sum(
        len(p["chapters"]) for p in packed["parts"]
    )
    assert (
        packed["total_chapter_count"] == 1 + packed["content_chapter_count"] + 4 * 2 + 4
    )
    assert packed["validation"]["valid"] is True
    assert packed["validation"]["total_placed_los"] == 24
    lo = packed["parts"][0]["chapters"][0]["learning_objectives"][0]
    assert lo["estimated_word_count"] == 475 and lo["estimated_time_minutes"] == 18
    assert lo["lo_text"] == "Objective 0" and lo["blooms_level"] == "Intermediate"


def test_undersized_part_is_merged():
    los = make_los(15)
    parts = [
        {"part_name": "Small", "ids": ["L0", "L1", "L2"]},
        {"part_name": "Big", "ids": [f"L{i}" for i in range(3, 15)]},
    ]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert packed["num_content_parts"] == 1
    assert "MERGE" in packed["enforcement_log"]


def test_rank_orders_chapters_within_part():
    los = make_los(6, chapter_of=lambda i: "Early" if i >= 3 else "Late")
    for i in range(6):
        los[f"L{i}"]["rank"] = 1 if i >= 3 else 2
    packed = build_structure(
        COURSE, BUDGET, los, [{"part_name": "P", "ids": [f"L{i}" for i in range(6)]}]
    )
    assert packed["parts"][0]["chapters"][0]["chapter_name"] == "Early"


def test_duplicate_input_urn_honoured_by_count():
    los = make_los(4)
    los["L1"]["urn"] = "urn:dup"
    los["L0"]["urn"] = "urn:dup"
    parts = [{"part_name": "P", "ids": ["L0", "L1", "L2", "L3"]}]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert packed["validation"]["valid"] is True
    assert packed["validation"]["duplicate_urns"] == []
    assert packed["validation"]["total_placed_los"] == 4
    placed = all_urns(packed)
    assert placed.count("urn:dup") == 2


@settings(max_examples=40, deadline=None)
@given(n=st.integers(1, 120), seed=st.integers(0, 10_000))
def test_property_urns_preserved_and_limits(n, seed):
    import random

    rnd = random.Random(seed)
    tiers = ["Foundational", "Intermediate", "Advanced"]
    los = make_los(
        n,
        chapter_of=lambda i: f"Ch{rnd.randint(0, max(1, n // 4))}",
        tier_of=lambda i: rnd.choice(tiers),
    )
    ids = list(los)
    k = max(1, n // rnd.randint(3, 12))
    parts = [
        {"part_name": f"Unit {j}", "ids": ids[j * k : (j + 1) * k]}
        for j in range((n + k - 1) // k)
    ]
    packed = build_structure(COURSE, BUDGET, los, parts)
    assert sorted(all_urns(packed)) == sorted(lo["urn"] for lo in los.values())
    for p in packed["parts"]:
        for c in p["chapters"]:
            assert c["chapter_estimated_time_minutes"] <= 60
            assert c["chapter_estimated_word_count"] <= 2000
            assert 1 <= len(c["learning_objectives"]) <= 4
    sizes = [len(p["chapters"]) for p in packed["parts"]]
    assert all(s >= 4 for s in sizes) or (len(sizes) <= 2 and sum(sizes) < 4)


def test_duplicate_lesson_names_uniquified_within_part():
    """Standards-style: same chapter base name in separate rank buckets must not duplicate."""
    los = make_los(
        8, chapter_of=lambda i: "Core Ideas", tier_of=lambda i: "Foundational"
    )
    for i in range(8):
        los[f"L{i}"]["rank"] = i + 1  # every LO its own bucket, same base name
        los[f"L{i}"]["primary_skill"] = f"Skill {i}"
    packed = build_structure(
        COURSE, BUDGET, los, [{"part_name": "P", "ids": [f"L{i}" for i in range(8)]}]
    )
    for p in packed["parts"]:
        names = [c["chapter_name"].casefold() for c in p["chapters"]]
        assert len(names) == len(set(names)), names


def test_duplicate_part_names_uniquified():
    los = make_los(24)
    parts = [
        {"part_name": "Core Concepts", "ids": [f"L{i}" for i in range(12)]},
        {"part_name": "Core Concepts", "ids": [f"L{i}" for i in range(12, 24)]},
    ]
    packed = build_structure(COURSE, BUDGET, los, parts)
    names = [p["part_name"].casefold() for p in packed["parts"]]
    assert len(names) == len(set(names)), names
