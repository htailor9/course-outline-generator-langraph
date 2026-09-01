# Run analysis — 20260901-172548_43LOs_Test-Math-regen-Counting-Combinatorics-N_claude_cli

Generated 2026-09-01T17:25:48 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 126.2s

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
| user_prompt | make lesson names more application-focused |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 6, Foundational 9, Intermediate 28
- Unique primary skills: **39** (top: Truth Tables ×2, Recursive Sequences ×2, Voting Power Indices ×2, Voting Fairness Criteria ×2, Logical Arguments ×1, Rules Of Inference ×1, Logical Fallacies ×1, Quantifiers ×1, Counterexamples ×1, Multiplication Principle ×1)

## 3. Output structure

- Parts: **7** (1 overview + 4 content + 2 semester) · Chapters: **45** · Modules: 59 · LO modules: 43
- Content estimate: 19873 words · 2046 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Logical Reasoning And Argumentation | 8 | 4 | 10 | 7 | 3509 | 378 |
| 3 | understand | Counting Combinatorics & Number Systems | 10 | 6 | 15 | 12 | 5332 | 452 |
| 4 | understand | Sequences Recursive & Graph Theory | 10 | 6 | 15 | 12 | 5516 | 456 |
| 5 | understand | Voting Theory & Fair Division | 12 | 8 | 15 | 12 | 5516 | 460 |
| 6 | semester | Test_Math Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 7 | semester | Test_Math Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Logical Fallacies | 1 | 291 | 14 |  | Spotting Logical Fallacies |
| 2 | 3 | Valid Arguments | 2 | 950 | 36 |  | Symbolic Argument Construction; Modus Ponens And Tollens |
| 2 | 4 | Quantifiers And Counterexamples | 2 | 950 | 36 |  | Universal And Existential Quantifiers; Constructing Counterexamples |
| 2 | 5 | Truth Tables | 2 | 1318 | 52 |  | Evaluating Argument Validity; Designing Truth Tables |
| 3 | 2 | Rankings Teams And Codes | 3 | 873 | 42 |  | Ranking Contest Winners; Selecting Team Rosters; Digital Data Encoding |
| 3 | 3 | Passwords And License Plates | 2 | 950 | 36 |  | Counting License Plate Options; Password Combination Counting |
| 3 | 4 | Solving Mixed Counting Problems | 2 | 950 | 36 |  | Overlapping Set Membership; Choosing Counting Strategies |
| 3 | 5 | Detecting Errors In Data | 2 | 950 | 36 |  | Simplifying Logic Circuits; Detecting Data Transmission Errors |
| 3 | 6 | Compressing And Encrypting Data | 2 | 950 | 36 |  | Calculating File Compression Ratios; Encrypting Messages With Ciphers |
| 3 | 7 | Optimizing Algorithm Performance | 1 | 659 | 26 |  | Comparing Algorithm Runtime Efficiency |
| 4 | 2 | Recursive Sequence Basics | 2 | 582 | 28 |  | Defining Recursive Sequences; Calculating Sequence Terms |
| 4 | 3 | Fibonacci And Recursive Algorithms | 2 | 950 | 36 |  | Fibonacci Modeling Applications; Recursive Algorithm Implementation |
| 4 | 4 | Convergence And Modeling | 2 | 950 | 36 |  | Sequence Convergence Analysis; Modeling Growth With Recursion |
| 4 | 5 | Graph Optimization Algorithms | 3 | 1425 | 54 |  | Dijkstra's Shortest Path; Kruskal's Minimum Spanning Tree; Ford-Fulkerson Max Flow |
| 4 | 6 | Combinatorial Graph Problems | 2 | 950 | 36 |  | Traveling Salesperson Algorithms; Graph Coloring Scheduling |
| 4 | 7 | Network Reliability Analysis | 1 | 659 | 26 |  | Network Connectivity Evaluation |
| 5 | 2 | Voting Power Indices | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 5 | 3 | Voting Methods | 1 | 475 | 18 |  | Plurality Borda And Runoff |
| 5 | 4 | Apportionment Methods | 1 | 475 | 18 |  | Hamilton Jefferson Webster Methods |
| 5 | 5 | Arrow's Impossibility Theorem | 1 | 475 | 18 |  | Limits Of Voting Systems |
| 5 | 6 | Evaluating Fairness Criteria | 1 | 659 | 26 |  | Assessing Voting Fairness Standards |
| 5 | 7 | Two-Party Fair Division | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 5 | 8 | Multi-Party Division Methods | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 5 | 9 | Fair Division Applications | 2 | 1134 | 44 |  | Selecting Fair Division Algorithms; Proportionality And Envy-Freeness |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 45 |
| fill ratio | 25% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=45 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 4 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 2 |
| prompt tokens | 98949 |
| completion tokens | 11256 |
| max single prompt | 53360 |
| tokens per LO | 2562.9 |

| node | calls | prompt tokens |
| --- | --- | --- |
| plan_chapters | 1 | 53360 |
| titles | 1 | 45589 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | plan_chapters | P2 | claude-sonnet-5 | 53360 | 9526 | 105243 | 1 |
| 2 | titles | 3 | claude-sonnet-5 | 45589 | 1730 | 20991 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 43 |
| distinct titles | 43 |
| avg words per title | 3.23 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Logical Reasoning And Argumentation' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics & Number Systems' - 6 understand chapters OK
FINAL: Part 'Sequences Recursive & Graph Theory' - 6 understand chapters OK
FINAL: Part 'Voting Theory & Fair Division' - 8 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
