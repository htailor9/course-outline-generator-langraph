def test_golden_parses(golden43, input43):
    assert golden43["label"] == "project"
    assert golden43["total_parts"] == 10
    assert golden43["total_chapters"] == 76
    urns = [
        m["learning_objective_urn"]
        for p in golden43["children"]
        for c in p["children"]
        for m in c["children"]
        if m.get("learning_objective_urn")
    ]
    assert len(urns) == 43 and len(set(urns)) == 43
    assert set(urns) == {
        lo["learning_objective_urn"] for lo in input43["learning_objectives"]
    }


def test_inputs_load(input94, input123):
    assert len(input94["learning_objectives"]) == 94
    assert len(input123["learning_objectives"]) == 123
