import copy
from outline.validate.invariants import check


def urns_of(inp):
    return [lo["learning_objective_urn"] for lo in inp["learning_objectives"]]


def test_golden_is_valid(golden43, input43):
    assert check(golden43, urns_of(input43)) == []


def test_detects_missing_and_duplicate_urn(golden43, input43):
    bad = copy.deepcopy(golden43)
    mod = bad["children"][1]["children"][1]["children"][0]
    mod["learning_objective_urn"] = bad["children"][1]["children"][2]["children"][0][
        "learning_objective_urn"
    ]
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("LO_COVERAGE") for e in errs)


def test_detects_min4_violation(golden43, input43):
    bad = copy.deepcopy(golden43)
    part = bad["children"][1]
    part["children"] = (
        [c for c in part["children"] if c["type"] != "understand"][:1]
        + [c for c in part["children"] if c["type"] == "understand"][:3]
        + [c for c in part["children"] if c["type"] in ("apply", "review", "test")]
    )
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("MIN4") for e in errs)


def test_detects_duplicate_titles_and_bad_sums(golden43, input43):
    bad = copy.deepcopy(golden43)
    ch = bad["children"][1]["children"][1]
    ch["chapter_estimated_word_count"] = 1
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("SUMS") for e in errs)
    bad2 = copy.deepcopy(golden43)
    for p in bad2["children"]:
        for c in p["children"]:
            if c["type"] == "understand" and len(c["children"]) >= 1:
                c["children"][0]["title"]["en"] = c["title"]["en"]
                break
    assert any(e.startswith("TITLES") for e in check(bad2, urns_of(input43)))


def test_detects_bad_semesters(golden43, input43):
    bad = copy.deepcopy(golden43)
    bad["children"][-1]["type"] = "understand"
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("SEMESTERS") for e in errs)

    bad2 = copy.deepcopy(golden43)
    bad2["children"][2]["type"] = "semester"
    errs2 = check(bad2, urns_of(input43))
    assert any(e.startswith("SEMESTERS") for e in errs2)


def test_detects_limits_violation(golden43, input43):
    bad = copy.deepcopy(golden43)
    for p in bad["children"]:
        if p["type"] != "understand":
            continue
        for c in p["children"]:
            if c["type"] == "understand":
                c["chapter_estimated_time_minutes"] = 999
                break
        break
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("LIMITS") for e in errs)


def test_detects_order_violations(golden43, input43):
    bad = copy.deepcopy(golden43)
    bad["children"][1]["children"][1]["chapter_number"] = 99
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("ORDER") for e in errs)

    bad2 = copy.deepcopy(golden43)
    for p in bad2["children"]:
        if p["type"] == "understand" and len(p["children"]) > 0:
            for c in p["children"]:
                if len(c["children"]) > 0:
                    c["children"][0]["module_number"] = 5
                    break
            break
    errs2 = check(bad2, urns_of(input43))
    assert any(e.startswith("ORDER") for e in errs2)


def test_detects_duplicate_unit_and_lesson_names(golden43, input43):
    bad = copy.deepcopy(golden43)
    bad["children"][2]["title"]["en"] = bad["children"][1]["title"][
        "en"
    ]  # two units same name
    errs = check(bad, urns_of(input43))
    assert any(e.startswith("NAMES duplicate unit") for e in errs)
    bad2 = copy.deepcopy(golden43)
    chs = [c for c in bad2["children"][1]["children"] if c["type"] == "understand"]
    chs[1]["title"]["en"] = chs[0]["title"]["en"]  # two lessons same name in unit
    assert any(
        e.startswith("NAMES duplicate lesson") for e in check(bad2, urns_of(input43))
    )
