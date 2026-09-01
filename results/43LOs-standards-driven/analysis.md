# Run analysis — 20260831-154750_43LOs_Test-Math-Standards_claude_cli

Generated 2026-08-31T15:47:50 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 146.7s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Test_Math_Standards |
| grade_band | MS |
| subject_area | Math |
| progression | STANDARDS_DRIVEN_PROGRESSION |
| learning objectives | 43 |
| calendar | 5/wk × 36 wk = 180 lesson days |
| minutes_per_lesson | 60 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 6, Foundational 9, Intermediate 28
- Unique primary skills: **36** (top: Fair Division ×5, Truth Tables ×2, Recursive Sequences ×2, Voting Power Indices ×2, Logical Arguments ×1, Rules Of Inference ×1, Logical Fallacies ×1, Quantifiers ×1, Counterexamples ×1, Multiplication Principle ×1)

## 3. Output structure

- Parts: **10** (1 overview + 7 content + 2 semester) · Chapters: **76** · Modules: 68 · LO modules: 43
- Content estimate: 19873 words · 2766 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math_Standards Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Logic And Reasoning Foundations | 10 | 6 | 9 | 6 | 2850 | 352 |
| 3 | understand | Combinatorics And Counting Methods | 10 | 6 | 9 | 6 | 2482 | 340 |
| 4 | understand | Recursive Sequences And Algorithms | 10 | 6 | 9 | 6 | 2482 | 340 |
| 5 | understand | Graph Theory And Network Algorithms | 10 | 6 | 9 | 6 | 3034 | 356 |
| 6 | understand | Voting Theory And Apportionment | 10 | 6 | 9 | 6 | 2666 | 348 |
| 7 | understand | Fair Division And Fairness Criteria | 10 | 6 | 9 | 6 | 2850 | 352 |
| 8 | understand | Number Systems And Information Theory | 11 | 7 | 10 | 7 | 3509 | 378 |
| 9 | semester | Test_Math_Standards Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 10 | semester | Test_Math_Standards Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Logical Arguments And Inference | 1 | 475 | 18 |  | Constructing Valid Arguments |
| 2 | 3 | Logical Arguments And Inference | 1 | 475 | 18 |  | Applying Modus Ponens Tollens |
| 2 | 4 | Evaluating Argument Validity | 1 | 291 | 14 |  | Spotting Logical Fallacies |
| 2 | 5 | Evaluating Argument Validity | 1 | 659 | 26 |  | Truth Tables For Validity |
| 2 | 6 | Quantifiers And Counterexamples | 1 | 475 | 18 |  | Using Quantifiers In Statements |
| 2 | 7 | Quantifiers And Counterexamples | 1 | 475 | 18 |  | Disproving Claims With Counterexamples |
| 3 | 2 | Fundamental Counting Methods | 1 | 475 | 18 |  | Multiplication Principle For Counting |
| 3 | 3 | Fundamental Counting Methods | 1 | 291 | 14 |  | Permutations Of Ordered Arrangements |
| 3 | 4 | Fundamental Counting Methods | 1 | 291 | 14 |  | Combinations For Unordered Selections |
| 3 | 5 | Advanced Counting Strategies | 1 | 475 | 18 |  | Counting Arrangements With Repetition |
| 3 | 6 | Advanced Counting Strategies | 1 | 475 | 18 |  | Inclusion-Exclusion Principle For Sets |
| 3 | 7 | Advanced Counting Strategies | 1 | 475 | 18 |  | Selecting Counting Techniques |
| 4 | 2 | Recursive Sequence Basics | 1 | 291 | 14 |  | Defining Recursive Sequences |
| 4 | 3 | Recursive Sequence Basics | 1 | 291 | 14 |  | Arithmetic And Geometric Terms |
| 4 | 4 | Fibonacci And Algorithms | 1 | 475 | 18 |  | Fibonacci Modeling Problems |
| 4 | 5 | Fibonacci And Algorithms | 1 | 475 | 18 |  | Recursive Factorial Algorithms |
| 4 | 6 | Convergence And Modeling | 1 | 475 | 18 |  | Analyzing Sequence Convergence |
| 4 | 7 | Convergence And Modeling | 1 | 475 | 18 |  | Modeling Growth And Investments |
| 5 | 2 | Path And Flow Algorithms | 1 | 475 | 18 |  | Dijkstra's Shortest Path |
| 5 | 3 | Path And Flow Algorithms | 1 | 475 | 18 |  | Kruskal's Minimum Spanning Tree |
| 5 | 4 | Path And Flow Algorithms | 1 | 475 | 18 |  | Ford-Fulkerson Max Flow |
| 5 | 5 | Advanced Graph Problems | 1 | 475 | 18 |  | Traveling Salesperson Heuristics |
| 5 | 6 | Advanced Graph Problems | 1 | 475 | 18 |  | Graph Coloring Scheduling |
| 5 | 7 | Advanced Graph Problems | 1 | 659 | 26 |  | Network Reliability Analysis |
| 6 | 2 | Weighted Voting Power | 1 | 291 | 14 |  | Banzhaf Power Index Calculation |
| 6 | 3 | Voting Systems And Apportionment | 1 | 475 | 18 |  | Arrow's Impossibility Theorem |
| 6 | 4 | Voting Systems And Apportionment | 1 | 475 | 18 |  | Plurality Borda Runoff Methods |
| 6 | 5 | Voting Systems And Apportionment | 1 | 475 | 18 |  | Hamilton Jefferson Webster Apportionment |
| 6 | 6 | Fairness Criteria Evaluation | 1 | 659 | 26 |  | Majority Condorcet Fairness Criteria |
| 6 | 7 | Coalition Power Analysis | 1 | 291 | 14 |  | Shapley-Shubik Power Index |
| 7 | 2 | Fair Division Methods | 1 | 475 | 18 |  | Divider-Chooser Method |
| 7 | 3 | Fair Division Methods | 1 | 475 | 18 |  | Lone-Divider Method |
| 7 | 4 | Fair Division Methods | 1 | 475 | 18 |  | Last-Diminisher Method |
| 7 | 5 | Fair Division Methods | 1 | 291 | 14 |  | Adjusted Winner Procedure |
| 7 | 6 | Evaluating Fair Divisions | 1 | 475 | 18 |  | Choosing Division Methods |
| 7 | 7 | Evaluating Fair Divisions | 1 | 659 | 26 |  | Proportionality And Envy-Freeness |
| 8 | 2 | Number Systems And Logic | 1 | 291 | 14 |  | Binary Octal Hex Conversion |
| 8 | 3 | Number Systems And Logic | 1 | 475 | 18 |  | Boolean Expression Simplification |
| 8 | 4 | Number Systems And Logic | 1 | 659 | 26 |  | Truth Table Construction |
| 8 | 5 | Data Encoding Techniques | 1 | 475 | 18 |  | Parity Bits And Check Digits |
| 8 | 6 | Data Encoding Techniques | 1 | 475 | 18 |  | Compression Ratio Analysis |
| 8 | 7 | Algorithmic Security Methods | 1 | 659 | 26 |  | Time And Space Complexity |
| 8 | 8 | Algorithmic Security Methods | 1 | 475 | 18 |  | Caesar Cipher Encryption |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 76 |
| fill ratio | 42% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=76 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 7 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 17 |
| prompt tokens | 720304 |
| completion tokens | 28490 |
| max single prompt | 47266 |
| tokens per LO | 17413.8 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 2 | 43170 |
| plan_chapters | 7 | 321839 |
| plan_parts | 1 | 46943 |
| titles | 7 | 308352 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 21305 | 2373 | 24845 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 21865 | 1053 | 15495 | 1 |
| 3 | plan_parts |  | claude-sonnet-5 | 46943 | 3383 | 36829 | 1 |
| 4 | plan_chapters | P1 | claude-sonnet-5 | 47162 | 3640 | 45347 | 1 |
| 5 | plan_chapters | P2 | claude-sonnet-5 | 44917 | 1258 | 20424 | 1 |
| 6 | plan_chapters | P3 | claude-sonnet-5 | 45420 | 1857 | 27023 | 1 |
| 7 | plan_chapters | P4 | claude-sonnet-5 | 47266 | 3644 | 47336 | 1 |
| 8 | plan_chapters | P5 | claude-sonnet-5 | 45721 | 2017 | 31894 | 1 |
| 9 | plan_chapters | P6 | claude-sonnet-5 | 45480 | 1977 | 26221 | 1 |
| 10 | plan_chapters | P7 | claude-sonnet-5 | 45873 | 2302 | 27468 | 1 |
| 11 | titles | 2 | claude-sonnet-5 | 44028 | 597 | 14714 | 1 |
| 12 | titles | 3 | claude-sonnet-5 | 44346 | 857 | 16834 | 1 |
| 13 | titles | 4 | claude-sonnet-5 | 44240 | 893 | 17476 | 1 |
| 14 | titles | 5 | claude-sonnet-5 | 43979 | 572 | 14533 | 1 |
| 15 | titles | 6 | claude-sonnet-5 | 44354 | 817 | 17099 | 1 |
| 16 | titles | 7 | claude-sonnet-5 | 44095 | 633 | 12705 | 1 |
| 17 | titles | 8 | claude-sonnet-5 | 43310 | 617 | 15704 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 43 |
| distinct titles | 43 |
| avg words per title | 3.4 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Logic And Reasoning Foundations' - 6 understand chapters OK
FINAL: Part 'Combinatorics And Counting Methods' - 6 understand chapters OK
FINAL: Part 'Recursive Sequences And Algorithms' - 6 understand chapters OK
FINAL: Part 'Graph Theory And Network Algorithms' - 6 understand chapters OK
FINAL: Part 'Voting Theory And Apportionment' - 6 understand chapters OK
FINAL: Part 'Fair Division And Fairness Criteria' - 6 understand chapters OK
FINAL: Part 'Number Systems And Information Theory' - 7 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
