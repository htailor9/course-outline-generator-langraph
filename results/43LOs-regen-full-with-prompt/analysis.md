# Run analysis — 20260901-173100_43LOs_Test-Math-regen-full_claude_cli

Generated 2026-09-01T17:31:00 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 210.2s

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
| user_prompt | broader, real-world themed units |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 6, Foundational 9, Intermediate 28
- Unique primary skills: **35** (top: Fair Division ×5, Truth Tables ×2, Recursive Sequences ×2, Voting Power Indices ×2, Fairness Criteria ×2, Valid Arguments ×1, Rules Of Inference ×1, Logical Fallacies ×1, Quantifiers ×1, Counterexamples ×1)

## 3. Output structure

- Parts: **7** (1 overview + 4 content + 2 semester) · Chapters: **43** · Modules: 59 · LO modules: 43
- Content estimate: 19873 words · 2046 minutes across understand chapters
- Min-4 merges applied: 2

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Critical Thinking And Persuasion | 8 | 4 | 9 | 6 | 2850 | 352 |
| 3 | understand | Counting Combinatorics & Codes Ciphers | 10 | 6 | 16 | 13 | 5991 | 478 |
| 4 | understand | Growth Patterns & Networks Route | 10 | 6 | 15 | 12 | 5516 | 456 |
| 5 | understand | Elections And Fair Sharing | 10 | 6 | 15 | 12 | 5516 | 460 |
| 6 | semester | Test_Math Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 7 | semester | Test_Math Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Spotting Faulty Arguments | 1 | 291 | 14 |  | Logical Fallacy Types |
| 2 | 3 | Building Valid Arguments | 2 | 950 | 36 |  | Symbolic Argument Construction; Modus Ponens And Tollens |
| 2 | 4 | Universal Claims And Exceptions | 2 | 950 | 36 |  | Universal And Existential Quantifiers; Constructing Logical Counterexamples |
| 2 | 5 | Testing Argument Validity | 1 | 659 | 26 |  | Truth Table Validity Testing |
| 3 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Ordered Arrangement Counting; Unordered Selection Counting |
| 3 | 3 | Real-World Counting Strategies | 3 | 1425 | 54 |  | Multiplication Principle Applications; Repetition-Based Arrangements; Inclusion-Exclusion Set Counting |
| 3 | 4 | Real-World Counting Strategies - Technique Selection | 1 | 475 | 18 |  | Choosing Counting Methods |
| 3 | 5 | Digital Logic Foundations | 3 | 1425 | 58 |  | Binary Octal Hex Conversion; Boolean Expression Simplification; Truth Table Construction |
| 3 | 6 | Data Transmission Essentials | 2 | 950 | 36 |  | Parity And Check Digits; Data Compression Ratios |
| 3 | 7 | Cryptographic Security Analysis | 2 | 1134 | 44 |  | Algorithmic Time-Space Complexity; Caesar Cipher Encryption |
| 4 | 2 | Recursive Sequence Foundations | 2 | 582 | 28 |  | Recursive Sequence Definitions; Arithmetic And Geometric Terms |
| 4 | 3 | Fibonacci And Recursive Algorithms | 2 | 950 | 36 |  | Fibonacci Modeling Applications; Recursive Factorial Algorithms |
| 4 | 4 | Convergence And Growth Modeling | 2 | 950 | 36 |  | Sequence Convergence Analysis; Modeling Growth With Recursion |
| 4 | 5 | Efficient Network Design | 2 | 950 | 36 |  | Dijkstra's Shortest Path; Kruskal's Minimum Spanning Tree |
| 4 | 6 | Routing And Scheduling Challenges | 2 | 950 | 36 |  | Traveling Salesperson Strategies; Graph Coloring Scheduling |
| 4 | 7 | Network Flow And Reliability | 2 | 1134 | 44 |  | Ford-Fulkerson Max Flow; Network Reliability Analysis |
| 5 | 2 | Voting Power Indices | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 5 | 3 | Two-Party Fair Division | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 5 | 4 | Multi-Party Division Methods | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 5 | 5 | Voting And Apportionment Methods | 2 | 950 | 36 |  | Comparing Voting Methods; Legislative Apportionment Methods |
| 5 | 6 | Voting Fairness Criteria | 2 | 1134 | 44 |  | Arrow's Impossibility Theorem; Evaluating Fairness Criteria |
| 5 | 7 | Fair Division Applications | 2 | 1134 | 44 |  | Choosing Fair Division Algorithms; Proportionality And Envy-Freeness |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 43 |
| fill ratio | 24% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=43 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 4 content parts; all parts >= 4 understand chapters: True.
- Merges applied: 2 (see enforcement_log).

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 13 |
| prompt tokens | 539179 |
| completion tokens | 35872 |
| max single prompt | 53748 |
| tokens per LO | 13373.3 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 2 | 42998 |
| plan_chapters | 6 | 260113 |
| plan_parts | 1 | 53748 |
| titles | 4 | 182320 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 21813 | 2752 | 24006 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 21185 | 1153 | 15989 | 1 |
| 3 | plan_parts |  | claude-sonnet-5 | 53748 | 9289 | 86704 | 1 |
| 4 | plan_chapters | P1 | claude-sonnet-5 | 22361 | 1034 | 17397 | 1 |
| 5 | plan_chapters | P2 | claude-sonnet-5 | 46764 | 2159 | 29056 | 1 |
| 6 | plan_chapters | P3 | claude-sonnet-5 | 48567 | 3685 | 44480 | 1 |
| 7 | plan_chapters | P4 | claude-sonnet-5 | 46518 | 2164 | 29250 | 1 |
| 8 | plan_chapters | P5 | claude-sonnet-5 | 46117 | 2510 | 34534 | 1 |
| 9 | plan_chapters | P6 | claude-sonnet-5 | 49786 | 5670 | 60577 | 1 |
| 10 | titles | 2 | claude-sonnet-5 | 44736 | 1149 | 18040 | 1 |
| 11 | titles | 3 | claude-sonnet-5 | 45704 | 1457 | 19394 | 1 |
| 12 | titles | 4 | claude-sonnet-5 | 46253 | 1351 | 17549 | 1 |
| 13 | titles | 5 | claude-sonnet-5 | 45627 | 1499 | 21375 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 43 |
| distinct titles | 43 |
| avg words per title | 3.12 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
MERGE: Part 'Counting And Combinatorics' (3 chapters) merged with 'Codes Ciphers And Data Security' (3 chapters)
RESULT: Part 'Counting Combinatorics & Codes Ciphers' now has 6 chapters
MERGE: Part 'Growth Patterns And Predictions' (3 chapters) merged with 'Networks And Route Optimization' (3 chapters)
RESULT: Part 'Growth Patterns & Networks Route' now has 6 chapters
FINAL: Part 'Critical Thinking And Persuasion' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics & Codes Ciphers' - 6 understand chapters OK
FINAL: Part 'Growth Patterns & Networks Route' - 6 understand chapters OK
FINAL: Part 'Elections And Fair Sharing' - 6 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
