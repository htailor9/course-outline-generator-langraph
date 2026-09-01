"""Deterministic Bloom's tier lookup: verb -> Foundational | Intermediate | Advanced."""

_FOUNDATIONAL = """add, approximate, articulate, associate, calculate, characterize, cite, clarify, classify, compare, compute, contrast, convert, defend, define, describe, detail, differentiate, discuss, distinguish, draw, duplicate, elaborate, enumerate, estimate, expand, explain, express, extend, extrapolate, factor, find, generalize, give original examples of, identify, index, indicate, infer, interact, interpolate, interpret, label, list, locate, match, name, outline, paraphrase, point, predict, quote, recall, recite, recognize, record, relate, repeat, reproduce, report, restate, rewrite, select, state, subtract, summarize, tabulate, tell, trace, translate, underline, write"""

_INTERMEDIATE = """acquire, adapt, advertise, allocate, alphabetize, analyze, apply, appraise, ascertain, assign, attain, attribute, audit, avoid, back up, blueprint, break down, capture, categorize, change, choose, confirm, construct, correlate, criticize, customize, debate, demonstrate, derive, detect, determine, diagnose, diagram, discriminate, dissect, document, dramatize, employ, examine, execute, exercise, experiment, expose, figure out, file, graph, group, handle, illustrate, implement, inspect, interconvert, investigate, inventory, layout, manage, manipulate, maximize, minimize, model, modify, operate, optimize, order, organize, perform, personalize, plot, point out, prepare, present, price, prioritize, process, produce, project, proofread, provide, query, round off, separate, sequence, show, simulate, simplify, sketch, solve, subdivide, subscribe, tabulate, test, train, transcribe, transform, use, utilize"""

_ADVANCED = """abstract, animate, appraise, argue, arrange, assemble, assess, budget, build, categorize, change, code, collect, combine, compile, compose, conclude, construct, convince, correspond, counsel, create, criticize, critique, cultivate, debate, debug, decide, depict, derive, design, develop, devise, dictate, discriminate, dispute, editorialize, enhance, evaluate, facilitate, format, formulate, generate, grade, hire, hypothesize, import, improve, incorporate, integrate, interface, invent, join, judge, justify, lecture, manage, measure, model, modify, network, organize, outline, plan, portray, predict, prepare, prescribe, produce, program, propose, rank, rate, rearrange, recommend, reconstruct, release, reorganize, revise, rewrite, score, set up, specify, support, summarize, validate, verify"""


def _split(s: str) -> list[str]:
    return [v.strip().lower() for v in s.split(",") if v.strip()]


VERB_TIER: dict[str, str] = {}
# Insert highest tier first so that lower tiers overwrite → lowest tier wins.
for _tier, _verbs in (
    ("Advanced", _ADVANCED),
    ("Intermediate", _INTERMEDIATE),
    ("Foundational", _FOUNDATIONAL),
):
    for _v in _split(_verbs):
        VERB_TIER[_v] = _tier


def tier_for(verb: str | None) -> str:
    if not verb:
        return "Foundational"
    key = " ".join(verb.strip().lower().split())
    if key in VERB_TIER:
        return VERB_TIER[key]
    first = key.split(" ")[0]
    return VERB_TIER.get(first, "Foundational")
