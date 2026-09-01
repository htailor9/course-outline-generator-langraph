# Run analysis — 20260827-203356_43LOs_Test-Math_claude_cli

Generated 2026-08-27T20:33:56 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 186.2s

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
- Unique primary skills: **39** (top: Truth Tables ×2, Recursive Sequences ×2, Voting Power Indices ×2, Voting Fairness Criteria ×2, Logical Arguments ×1, Rules Of Inference ×1, Logical Fallacies ×1, Quantifiers ×1, Counterexamples ×1, Multiplication Principle ×1)

## 3. Output structure

- Parts: **7** (1 overview + 4 content + 2 semester) · Chapters: **46** · Modules: 59 · LO modules: 43
- Content estimate: 19873 words · 2046 minutes across understand chapters
- Min-4 merges applied: 3

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Logical Reasoning And Argumentation | 8 | 4 | 10 | 7 | 3509 | 378 |
| 3 | understand | Counting Combinatorics & Number Systems | 11 | 7 | 15 | 12 | 5332 | 452 |
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
| 3 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Permutations Of Distinct Objects; Combinations Of Distinct Objects |
| 3 | 3 | Multiplication And Repetition | 2 | 950 | 36 |  | Multiplication Principle Basics; Arrangements With Repetition |
| 3 | 4 | Combining Counting Techniques | 2 | 950 | 36 |  | Inclusion-Exclusion Principle; Choosing Counting Techniques |
| 3 | 5 | Number Base Systems | 1 | 291 | 14 |  | Number Base Conversion |
| 3 | 6 | Boolean Logic And Parity | 2 | 950 | 36 |  | Boolean Algebra Simplification; Error-Detection Codes |
| 3 | 7 | Compression And Cryptography | 2 | 950 | 36 |  | Data Compression Ratios; Caesar Cipher Encryption |
| 3 | 8 | Algorithmic Complexity Analysis | 1 | 659 | 26 |  | Algorithmic Efficiency Analysis |
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
| total_chapters | 46 |
| fill ratio | 26% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=46 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 4 content parts; all parts >= 4 understand chapters: True.
- Merges applied: 3 (see enforcement_log).

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 14 |
| prompt tokens | 583179 |
| completion tokens | 29928 |
| max single prompt | 69862 |
| tokens per LO | 14258.3 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 2 | 41864 |
| plan_chapters | 7 | 341964 |
| plan_parts | 1 | 21090 |
| titles | 4 | 178261 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 21246 | 2360 | 26534 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 20618 | 1116 | 16778 | 1 |
| 3 | plan_parts |  | claude-sonnet-5 | 21090 | 6633 | 64230 | 1 |
| 4 | plan_chapters | P1 | claude-sonnet-5 | 45129 | 1677 | 27764 | 1 |
| 5 | plan_chapters | P2 | claude-sonnet-5 | 46218 | 2968 | 41319 | 1 |
| 6 | plan_chapters | P3 | claude-sonnet-5 | 44890 | 1510 | 30318 | 1 |
| 7 | plan_chapters | P4 | claude-sonnet-5 | 46036 | 2753 | 39891 | 1 |
| 8 | plan_chapters | P5 | claude-sonnet-5 | 45284 | 1844 | 36443 | 1 |
| 9 | plan_chapters | P6 | claude-sonnet-5 | 44545 | 1808 | 23691 | 1 |
| 10 | plan_chapters | P7 | claude-sonnet-5 | 69862 | 2866 | 37685 | 1 |
| 11 | titles | 2 | claude-sonnet-5 | 44014 | 754 | 18971 | 1 |
| 12 | titles | 3 | claude-sonnet-5 | 43815 | 806 | 19411 | 1 |
| 13 | titles | 4 | claude-sonnet-5 | 44919 | 1190 | 21575 | 1 |
| 14 | titles | 5 | claude-sonnet-5 | 45513 | 1643 | 27179 | 1 |

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
MERGE: Part 'Counting And Combinatorics' (3 chapters) merged with 'Number Systems And Information Theory' (4 chapters)
RESULT: Part 'Counting Combinatorics & Number Systems' now has 7 chapters
MERGE: Part 'Sequences And Recursive Processes' (3 chapters) merged with 'Graph Theory And Networks' (3 chapters)
RESULT: Part 'Sequences Recursive & Graph Theory' now has 6 chapters
MERGE: Part 'Fair Division Methods' (3 chapters) merged with 'Voting Theory And Social Choice' (5 chapters)
RESULT: Part 'Voting Theory & Fair Division' now has 8 chapters
FINAL: Part 'Logical Reasoning And Argumentation' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics & Number Systems' - 7 understand chapters OK
FINAL: Part 'Sequences Recursive & Graph Theory' - 6 understand chapters OK
FINAL: Part 'Voting Theory & Fair Division' - 8 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
