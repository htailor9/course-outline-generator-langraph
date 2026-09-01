from outline.rules.merging import enforce_min_4


def part(name, n):
    return {
        "part_name": name,
        "chapters": [
            {
                "chapter_name": f"{name} {i}",
                "learning_objectives": [{"urn": f"{name}-{i}"}],
            }
            for i in range(n)
        ],
    }


def counts(parts):
    return [len(p["chapters"]) for p in parts]


def test_matrix_1_multiple_merges():
    parts, log = enforce_min_4(
        [part("A", 3), part("B", 3), part("C", 3), part("D", 3), part("E", 4)]
    )
    assert counts(parts) == [6, 6, 4]
    assert any(l.startswith("MERGE") for l in log)


def test_matrix_2_single_merge_large_course():
    parts, _ = enforce_min_4(
        [part(n, c) for n, c in zip("ABCDEFGH", [4, 5, 3, 4, 6, 4, 5, 4])]
    )
    assert counts(parts) == [4, 5, 7, 6, 4, 5, 4]


def test_matrix_3_noop_when_valid():
    parts, log = enforce_min_4([part(n, 4) for n in "ABCDEF"])
    assert counts(parts) == [4] * 6
    assert all(l.startswith("FINAL") for l in log)


def test_matrix_4_two_part_exception():
    parts, log = enforce_min_4([part("A", 1), part("B", 2)])
    assert counts(parts) == [1, 2]
    assert any(l.startswith("EXCEPTION") for l in log)


def test_matrix_5_two_parts_merge_when_combined_ge_4():
    parts, _ = enforce_min_4([part("A", 2), part("B", 2)])
    assert counts(parts) == [4]


def test_matrix_6_best_adjacent_is_smallest():
    parts, _ = enforce_min_4([part("A", 2), part("B", 2), part("C", 8)])
    assert counts(parts) == [4, 8]


def test_urns_preserved_and_order_kept():
    src = [part("A", 3), part("B", 5)]
    parts, _ = enforce_min_4(src)
    urns = [
        lo["urn"]
        for p in parts
        for c in p["chapters"]
        for lo in c["learning_objectives"]
    ]
    assert urns == [f"A-{i}" for i in range(3)] + [f"B-{i}" for i in range(5)]
    assert parts[0]["part_name"] == "A & B"
