from outline.rules.naming import skill_key, merge_part_names, uniquify_chapter_names


def test_skill_key_normalises():
    assert skill_key("Rules Of Inference") == skill_key("inference rules")
    assert skill_key("Logical Fallacies") == skill_key("logical fallacy")
    assert skill_key("Main Idea") != skill_key("Key Details")


def test_merge_part_names():
    assert merge_part_names("Logic", "Logic") == "Logic"
    assert merge_part_names("Logic and Proof", "Proof") == "Logic and Proof"
    assert (
        merge_part_names("Basic Skills", "Advanced Skills")
        == "Basic Skills & Advanced Skills"
    )
    assert (
        len(
            merge_part_names(
                "Cultural Context in Art", "Arts Analysis and Response"
            ).split()
        )
        <= 6
    )


def test_uniquify_uses_skill_differentiator():
    chapters = [
        {
            "chapter_name": "Fractions",
            "learning_objectives": [{"primary_skill": "Fraction Addition"}],
        },
        {
            "chapter_name": "Fractions",
            "learning_objectives": [{"primary_skill": "Fraction Denominators"}],
        },
        {
            "chapter_name": "Decimals",
            "learning_objectives": [{"primary_skill": "Decimals"}],
        },
    ]
    out = uniquify_chapter_names(chapters)
    names = [c["chapter_name"] for c in out]
    assert names[0] == "Fractions"
    assert names[1].startswith("Fractions - ") and "Denominators" in names[1]
    assert len(set(names)) == 3
