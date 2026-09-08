# Run analysis — 20260908-151422_25LOs_Test-Math-25_claude_cli

Generated 2026-09-08T15:16:05 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 102.6s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Test_Math_25 |
| grade_band | MS |
| subject_area | Math |
| progression | SKILLS_BASED_PROGRESSION |
| learning objectives | 25 |
| calendar | 5/wk × 36 wk = 180 lesson days |
| minutes_per_lesson | 60 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 2, Foundational 6, Intermediate 17
- Unique primary skills: **24** (top: Recursive Sequences ×2, Logical Argument Construction ×1, Rules Of Inference ×1, Logical Fallacies ×1, Deductive Argument Validity ×1, Quantifiers ×1, Counterexamples ×1, Multiplication Principle ×1, Permutations ×1, Combinations ×1)

## 3. Output structure

- Parts: **6** (1 overview + 3 content + 2 semester) · Chapters: **31** · Modules: 38 · LO modules: 25
- Content estimate: 11139 words · 1462 minutes across understand chapters
- Min-4 merges applied: 2

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math_25 Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Logical Reasoning And Argumentation | 8 | 4 | 9 | 6 | 2850 | 352 |
| 3 | understand | Combinatorics Counting & Voting Power | 8 | 4 | 10 | 7 | 2773 | 354 |
| 4 | understand | Recursive Sequences & Graph Algorithms | 10 | 6 | 15 | 12 | 5516 | 456 |
| 5 | semester | Test_Math_25 Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 6 | semester | Test_Math_25 Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Logical Fallacies | 1 | 291 | 14 |  | Identifying Common Fallacies |
| 2 | 3 | Argument Construction | 2 | 950 | 36 |  | Symbolic Argument Construction; Applying Rules Of Inference |
| 2 | 4 | Quantifiers And Counterexamples | 2 | 950 | 36 |  | Using Mathematical Quantifiers; Disproving Claims With Counterexamples |
| 2 | 5 | Deductive Argument Validity | 1 | 659 | 26 |  | Truth Tables For Validity |
| 3 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Ordered Arrangements With Permutations; Unordered Selections With Combinations |
| 3 | 3 | Applied Counting Techniques | 3 | 1425 | 54 |  | Multiplication Principle For Outcomes; Arrangements With Repetition; Inclusion-Exclusion For Set Counting |
| 3 | 4 | Applied Counting Techniques - Technique Selection | 1 | 475 | 18 |  | Choosing The Right Counting Method |
| 3 | 5 | Banzhaf Power Index | 1 | 291 | 14 |  | Weighted Voting Power Calculations |
| 4 | 2 | Recursive Sequence Basics | 2 | 582 | 28 |  | Defining Recursive Sequences; Arithmetic And Geometric Terms |
| 4 | 3 | Fibonacci And Algorithmic Recursion | 2 | 950 | 36 |  | Fibonacci Modeling; Recursive Factorial Algorithms |
| 4 | 4 | Sequence Convergence And Modeling | 2 | 950 | 36 |  | Convergence Of Sequences; Modeling Growth And Investments |
| 4 | 5 | Shortest Paths And Trees | 2 | 950 | 36 |  | Dijkstra's Shortest Path; Kruskal's Spanning Tree |
| 4 | 6 | Flow And Routing Problems | 2 | 950 | 36 |  | Ford-Fulkerson Max Flow; Traveling Salesperson Strategies |
| 4 | 7 | Coloring And Reliability | 2 | 1134 | 44 |  | Graph Coloring Scheduling; Network Reliability Analysis |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 31 |
| fill ratio | 17% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=31 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 3 content parts; all parts >= 4 understand chapters: True.
- Merges applied: 2 (see enforcement_log).

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 10 |
| prompt tokens | 334624 |
| completion tokens | 16020 |
| max single prompt | 51909 |
| tokens per LO | 14025.8 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 1 | 15283 |
| plan_chapters | 5 | 186448 |
| plan_parts | 1 | 34495 |
| titles | 3 | 98398 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 15283 | 933 | 14818 | 1 |
| 2 | plan_parts |  | claude-sonnet-5 | 34495 | 3108 | 35445 | 1 |
| 3 | plan_chapters | P1 | claude-sonnet-5 | 51909 | 2339 | 34406 | 1 |
| 4 | plan_chapters | P2 | claude-sonnet-5 | 34546 | 2543 | 34628 | 1 |
| 5 | plan_chapters | P3 | claude-sonnet-5 | 31840 | 198 | 14955 | 1 |
| 6 | plan_chapters | P4 | claude-sonnet-5 | 34273 | 2525 | 35165 | 1 |
| 7 | plan_chapters | P5 | claude-sonnet-5 | 33880 | 1903 | 32251 | 1 |
| 8 | titles | 2 | claude-sonnet-5 | 32484 | 750 | 16161 | 1 |
| 9 | titles | 3 | claude-sonnet-5 | 32819 | 906 | 16960 | 1 |
| 10 | titles | 4 | claude-sonnet-5 | 33095 | 815 | 15953 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 25 |
| distinct titles | 25 |
| avg words per title | 3.44 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
MERGE: Part 'Combinatorics And Counting Methods' (3 chapters) merged with 'Voting Power Indices' (1 chapters)
RESULT: Part 'Combinatorics Counting & Voting Power' now has 4 chapters
MERGE: Part 'Recursive Sequences And Patterns' (3 chapters) merged with 'Graph Algorithms And Optimization' (3 chapters)
RESULT: Part 'Recursive Sequences & Graph Algorithms' now has 6 chapters
FINAL: Part 'Logical Reasoning And Argumentation' - 4 understand chapters OK
FINAL: Part 'Combinatorics Counting & Voting Power' - 4 understand chapters OK
FINAL: Part 'Recursive Sequences & Graph Algorithms' - 6 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
