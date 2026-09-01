# Run analysis — 20260901-173405_43LOs_Test-Math-regen-full_claude_cli

Generated 2026-09-01T17:34:05 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 182.8s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Test_Math |
| grade_band | MS |
| subject_area | Math |
| progression | SKILLS_BASED_PROGRESSION |
| learning objectives | 43 |
| calendar | 5/wk × 36 wk = 180 lesson days |
| minutes_per_lesson | 60 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 6, Foundational 9, Intermediate 28
- Unique primary skills: **40** (top: Truth Tables ×2, Recursive Sequences ×2, Voting Power Indices ×2, Valid Arguments ×1, Rules Of Inference ×1, Logical Fallacies ×1, Quantifiers ×1, Counterexamples ×1, Multiplication Principle ×1, Permutations ×1)

## 3. Output structure

- Parts: **7** (1 overview + 4 content + 2 semester) · Chapters: **44** · Modules: 59 · LO modules: 43
- Content estimate: 19873 words · 2046 minutes across understand chapters
- Min-4 merges applied: 3

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Logical Reasoning Foundations | 8 | 4 | 9 | 6 | 2850 | 352 |
| 3 | understand | Counting Combinatorics & Recursive Sequences | 10 | 6 | 15 | 12 | 4964 | 440 |
| 4 | understand | Number Systems And Digital Computing | 8 | 4 | 10 | 7 | 3509 | 378 |
| 5 | understand | Graph Network & Fair Division | 13 | 9 | 21 | 18 | 8550 | 576 |
| 6 | semester | Test_Math Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 7 | semester | Test_Math Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Identifying Logical Fallacies | 1 | 291 | 14 |  | Types Of Logical Fallacies |
| 2 | 3 | Valid Arguments And Inference | 2 | 950 | 36 |  | Symbolic Argument Construction; Modus Ponens And Tollens |
| 2 | 4 | Quantifiers And Counterexamples | 2 | 950 | 36 |  | Universal And Existential Quantifiers; Disproving With Counterexamples |
| 2 | 5 | Truth Tables And Validity | 1 | 659 | 26 |  | Evaluating Argument Validity |
| 3 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Calculating Permutations; Calculating Combinations |
| 3 | 3 | Multiplication And Repetition | 2 | 950 | 36 |  | Multiplication Principle; Arrangements With Repetition |
| 3 | 4 | Combining Counting Techniques | 2 | 950 | 36 |  | Inclusion-Exclusion Principle; Choosing Counting Methods |
| 3 | 5 | Recursive Sequence Basics | 2 | 582 | 28 |  | Defining Recursive Sequences; Arithmetic And Geometric Sequences |
| 3 | 6 | Fibonacci And Recursive Algorithms | 2 | 950 | 36 |  | Fibonacci Sequence Applications; Recursive Algorithm Design |
| 3 | 7 | Convergence And Modeling | 2 | 950 | 36 |  | Sequence Convergence Analysis; Modeling With Recursion |
| 4 | 2 | Number Base Systems | 1 | 291 | 14 |  | Converting Number Bases |
| 4 | 3 | Boolean Logic And Error Detection | 2 | 950 | 36 |  | Simplifying Boolean Expressions; Error-Detection Codes |
| 4 | 4 | Data Security And Compression | 2 | 950 | 36 |  | Data Compression Ratios; Cryptographic Encryption Methods |
| 4 | 5 | Logic Verification And Efficiency | 2 | 1318 | 52 |  | Truth Table Construction; Algorithmic Complexity Analysis |
| 5 | 2 | Weighted Graph Algorithms | 3 | 1425 | 54 |  | Dijkstra's Shortest Path; Kruskal's Minimum Spanning Tree; Ford-Fulkerson Max Flow |
| 5 | 3 | Combinatorial Graph Problems | 2 | 950 | 36 |  | Traveling Salesperson Algorithms; Graph Coloring Scheduling |
| 5 | 4 | Network Reliability Analysis | 1 | 659 | 26 |  | Connectivity And Critical Paths |
| 5 | 5 | Voting Power Indices | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 5 | 6 | Voting Methods And Limits | 2 | 950 | 36 |  | Arrow's Impossibility Theorem; Plurality Borda And Runoff |
| 5 | 7 | Apportionment And Fairness | 2 | 1134 | 44 |  | Hamilton Jefferson Webster Methods; Voting Fairness Criteria |
| 5 | 8 | Basic Division Methods | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 5 | 9 | Proportional Division Methods | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 5 | 10 | Fair Division Assessment | 2 | 1134 | 44 |  | Selecting Division Algorithms; Evaluating Division Fairness |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 44 |
| fill ratio | 24% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=44 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 4 content parts; all parts >= 4 understand chapters: True.
- Merges applied: 3 (see enforcement_log).

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 14 |
| prompt tokens | 599254 |
| completion tokens | 32254 |
| max single prompt | 68898 |
| tokens per LO | 14686.2 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 2 | 42822 |
| plan_chapters | 7 | 320549 |
| plan_parts | 1 | 51498 |
| titles | 4 | 184385 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 21725 | 2130 | 19888 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 21097 | 1057 | 13152 | 1 |
| 3 | plan_parts |  | claude-sonnet-5 | 51498 | 7179 | 67920 | 1 |
| 4 | plan_chapters | P1 | claude-sonnet-5 | 45755 | 1475 | 22615 | 1 |
| 5 | plan_chapters | P2 | claude-sonnet-5 | 45962 | 1486 | 24246 | 1 |
| 6 | plan_chapters | P3 | claude-sonnet-5 | 68898 | 1686 | 24211 | 1 |
| 7 | plan_chapters | P4 | claude-sonnet-5 | 47428 | 2957 | 36614 | 1 |
| 8 | plan_chapters | P5 | claude-sonnet-5 | 45311 | 1804 | 25725 | 1 |
| 9 | plan_chapters | P6 | claude-sonnet-5 | 21164 | 4290 | 47732 | 1 |
| 10 | plan_chapters | P7 | claude-sonnet-5 | 46031 | 2324 | 28910 | 1 |
| 11 | titles | 2 | claude-sonnet-5 | 45225 | 1033 | 16864 | 1 |
| 12 | titles | 3 | claude-sonnet-5 | 46370 | 1602 | 22359 | 1 |
| 13 | titles | 4 | claude-sonnet-5 | 45207 | 976 | 15951 | 1 |
| 14 | titles | 5 | claude-sonnet-5 | 47583 | 2255 | 24475 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 43 |
| distinct titles | 43 |
| avg words per title | 3.0 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
MERGE: Part 'Counting And Combinatorics Techniques' (3 chapters) merged with 'Recursive Sequences And Modeling' (3 chapters)
RESULT: Part 'Counting Combinatorics & Recursive Sequences' now has 6 chapters
MERGE: Part 'Graph And Network Algorithms' (3 chapters) merged with 'Voting Theory And Apportionment' (3 chapters)
RESULT: Part 'Graph Network & Voting Theory' now has 6 chapters
MERGE: Part 'Fair Division Methods' (3 chapters) merged with 'Graph Network & Voting Theory' (6 chapters)
RESULT: Part 'Graph Network & Fair Division' now has 9 chapters
FINAL: Part 'Logical Reasoning Foundations' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics & Recursive Sequences' - 6 understand chapters OK
FINAL: Part 'Number Systems And Digital Computing' - 4 understand chapters OK
FINAL: Part 'Graph Network & Fair Division' - 9 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
