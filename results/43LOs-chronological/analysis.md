# Run analysis — 20260831-113702_43LOs_Test-Math-Chrono_claude_cli

Generated 2026-08-31T11:37:02 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 72.0s

## Verdict

- ✅ all invariants passed
- ⚠ fallbacks used: {'annotate_fallback': 43, 'plan_parts_fallback': 43, 'plan_chapters_fallback': 43, 'titles_fallback': 43}
- ❌ LLM errors: 5
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Test_Math_Chrono |
| grade_band | MS |
| subject_area | Math |
| progression | CHRONOLOGICAL_PROGRESSION |
| learning objectives | 43 |
| calendar | 5/wk × 36 wk = 180 lesson days |
| minutes_per_lesson | 60 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 6, Foundational 9, Intermediate 28
- Unique primary skills: **43** (top: Valid Logical Arguments ×1, Rules Inference Including ×1, Logical Fallacies Arguments ×1, Validity Deductive Arguments ×1, Quantifiers Including Universal ×1, Counterexamples Disprove Invalid ×1, Multiplication Principle Calculate ×1, Permutations Distinct Objects ×1, Combinations Distinct Objects ×1, Counting Problems Involving ×1)

## 3. Output structure

- Parts: **4** (1 overview + 1 content + 2 semester) · Chapters: **52** · Modules: 50 · LO modules: 43
- Content estimate: 19873 words · 1326 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math_Chrono Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Test_Math_Chrono Core Concepts | 47 | 43 | 46 | 43 | 19873 | 1026 |
| 3 | semester | Test_Math_Chrono Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 4 | semester | Test_Math_Chrono Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Between Different Number | 1 | 291 | 14 |  | Between Different Number: Convert |
| 2 | 3 | Combinations Distinct Objects | 1 | 291 | 14 |  | Combinations Distinct Objects: Calculate |
| 2 | 4 | Fair Shares Using | 1 | 291 | 14 |  | Fair Shares Using: Calculate |
| 2 | 5 | Logical Fallacies Arguments | 1 | 291 | 14 |  | Logical Fallacies Arguments: Identify |
| 2 | 6 | Permutations Distinct Objects | 1 | 291 | 14 |  | Permutations Distinct Objects: Calculate |
| 2 | 7 | Recursive Sequences Using | 1 | 291 | 14 |  | Recursive Sequences Using: Define |
| 2 | 8 | Shapley-Shubik Power Index | 1 | 291 | 14 |  | Shapley-Shubik Power Index: Calculate |
| 2 | 9 | Terms Recursive Sequences | 1 | 291 | 14 |  | Terms Recursive Sequences: Calculate |
| 2 | 10 | Voting Power Indices | 1 | 291 | 14 |  | Voting Power Indices: Calculate |
| 2 | 11 | Apportionment Methods Such | 1 | 475 | 18 |  | Apportionment Methods Such: Analyze |
| 2 | 12 | Arrow'S Impossibility Theorem | 1 | 475 | 18 |  | Arrow'S Impossibility Theorem: Apply |
| 2 | 13 | Boolean Algebra Operations | 1 | 475 | 18 |  | Boolean Algebra Operations: Apply |
| 2 | 14 | Convergence Behavior Recursive | 1 | 475 | 18 |  | Convergence Behavior Recursive: Analyze |
| 2 | 15 | Counterexamples Disprove Invalid | 1 | 475 | 18 |  | Counterexamples Disprove Invalid: Construct |
| 2 | 16 | Counting Problems Involving | 1 | 475 | 18 |  | Counting Problems Involving: Solve |
| 2 | 17 | Counting Scenarios Determine | 1 | 475 | 18 |  | Counting Scenarios Determine: Analyze |
| 2 | 18 | Cryptographic Methods Including | 1 | 475 | 18 |  | Cryptographic Methods Including: Apply |
| 2 | 19 | Data Compression Techniques | 1 | 475 | 18 |  | Data Compression Techniques: Analyze |
| 2 | 20 | Different Voting Methods | 1 | 475 | 18 |  | Different Voting Methods: Implement |
| 2 | 21 | Dijkstra'S Algorithm Find | 1 | 475 | 18 |  | Dijkstra'S Algorithm Find: Apply |
| 2 | 22 | Divider-Chooser Method Divide | 1 | 475 | 18 |  | Divider-Chooser Method Divide: Apply |
| 2 | 23 | Error-Detection Codes Such | 1 | 475 | 18 |  | Error-Detection Codes Such: Implement |
| 2 | 24 | Fibonacci Sequence Properties | 1 | 475 | 18 |  | Fibonacci Sequence Properties: Apply |
| 2 | 25 | Graph Coloring Algorithms | 1 | 475 | 18 |  | Graph Coloring Algorithms: Apply |
| 2 | 26 | Inclusion-Exclusion Principle Determine | 1 | 475 | 18 |  | Inclusion-Exclusion Principle Determine: Apply |
| 2 | 27 | Kruskal'S Algorithm Determine | 1 | 475 | 18 |  | Kruskal'S Algorithm Determine: Implement |
| 2 | 28 | Last-Diminisher Method Ensure | 1 | 475 | 18 |  | Last-Diminisher Method Ensure: Execute |
| 2 | 29 | Lone-Divider Method Achieve | 1 | 475 | 18 |  | Lone-Divider Method Achieve: Implement |
| 2 | 30 | Multiplication Principle Calculate | 1 | 475 | 18 |  | Multiplication Principle Calculate: Apply |
| 2 | 31 | Network Flow Problems | 1 | 475 | 18 |  | Network Flow Problems: Analyze |
| 2 | 32 | Quantifiers Including Universal | 1 | 475 | 18 |  | Quantifiers Including Universal: Apply |
| 2 | 33 | Real-World Phenomena Using | 1 | 475 | 18 |  | Real-World Phenomena Using: Model |
| 2 | 34 | Real-World Scenarios Determine | 1 | 475 | 18 |  | Real-World Scenarios Determine: Analyze |
| 2 | 35 | Recursive Algorithms Solve | 1 | 475 | 18 |  | Recursive Algorithms Solve: Implement |
| 2 | 36 | Rules Inference Including | 1 | 475 | 18 |  | Rules Inference Including: Apply |
| 2 | 37 | Traveling Salesperson Problem | 1 | 475 | 18 |  | Traveling Salesperson Problem: Solve |
| 2 | 38 | Valid Logical Arguments | 1 | 475 | 18 |  | Valid Logical Arguments: Construct |
| 2 | 39 | Algorithmic Efficiency Comparing | 1 | 659 | 26 |  | Algorithmic Efficiency Comparing: Evaluate |
| 2 | 40 | Fairness Proposed Divisions | 1 | 659 | 26 |  | Fairness Proposed Divisions: Evaluate |
| 2 | 41 | Network Reliability Calculating | 1 | 659 | 26 |  | Network Reliability Calculating: Evaluate |
| 2 | 42 | Truth Tables Represent | 1 | 659 | 26 |  | Truth Tables Represent: Design |
| 2 | 43 | Validity Deductive Arguments | 1 | 659 | 26 |  | Validity Deductive Arguments: Evaluate |
| 2 | 44 | Voting Systems Against | 1 | 659 | 26 |  | Voting Systems Against: Evaluate |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 52 |
| fill ratio | 29% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=52 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 1 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 0 |
| prompt tokens | 0 |
| completion tokens | 0 |
| max single prompt | 0 |
| tokens per LO | 0.0 |

| node | calls | prompt tokens |
| --- | --- | --- |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 43 |
| distinct titles | 43 |
| avg words per title | 4.0 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | {'annotate_fallback': 43, 'plan_parts_fallback': 43, 'plan_chapters_fallback': 43, 'titles_fallback': 43} |
| soft invariant failures | none |
| LLM errors | structured output failed for AnnotateOut: success; structured output failed for AnnotateOut: success; structured output failed for PartsOut: success; structured output failed for ChaptersOut: success; structured output failed for TitlesOut: success |

## 7. Enforcement log

```
FINAL: Part 'Test_Math_Chrono Core Concepts' - 43 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
