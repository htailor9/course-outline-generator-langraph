# Run analysis — 20260901-111038_43LOs_Test-Math-UserPrompt_claude_cli

Generated 2026-09-01T11:10:38 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 205.2s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Test_Math_UserPrompt |
| grade_band | MS |
| subject_area | Math |
| progression | SKILLS_BASED_PROGRESSION |
| learning objectives | 43 |
| calendar | 5/wk × 36 wk = 180 lesson days |
| minutes_per_lesson | 60 |
| chapter word limit | 2000 |
| user_prompt | Prefer fewer, broader units: aim for exactly 3 units. Every unit name must be at most 3 words. Lesson names should emphasise real-world applications. |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 6, Foundational 9, Intermediate 28
- Unique primary skills: **40** (top: Recursive Sequences ×2, Voting Power Indices ×2, Voting Fairness Criteria ×2, Logical Arguments ×1, Rules Of Inference ×1, Logical Fallacies ×1, Argument Validity ×1, Quantifiers ×1, Counterexamples ×1, Multiplication Principle ×1)

## 3. Output structure

- Parts: **6** (1 overview + 3 content + 2 semester) · Chapters: **36** · Modules: 56 · LO modules: 43
- Content estimate: 19873 words · 1806 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Test_Math_UserPrompt Course Overview | 1 | 0 | 2 | 0 | 0 | 60 |
| 2 | understand | Logic And Counting | 10 | 6 | 18 | 15 | 6757 | 510 |
| 3 | understand | Sequences And Networks | 10 | 6 | 15 | 12 | 5516 | 456 |
| 4 | understand | Fairness And Information | 11 | 7 | 19 | 16 | 7600 | 540 |
| 5 | semester | Test_Math_UserPrompt Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |
| 6 | semester | Test_Math_UserPrompt Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 120 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Counting Real-World Choices | 3 | 1057 | 46 |  | Counting Everyday Outcomes; Ordering Contest Winners; Choosing Team Combinations |
| 2 | 3 | Building Persuasive Arguments | 3 | 1241 | 50 |  | Building Logical Arguments; Drawing Logical Conclusions; Spotting Argument Fallacies |
| 2 | 4 | Proving And Disproving Claims | 2 | 950 | 36 |  | Quantifying Mathematical Statements; Disproving False Claims |
| 2 | 5 | Solving Tricky Counting Problems | 3 | 1425 | 54 |  | Counting Passwords With Repetition; Counting Overlapping Groups; Selecting Counting Strategies |
| 2 | 6 | Coding With Binary Logic | 2 | 766 | 32 |  | Converting Computer Number Systems; Simplifying Digital Logic |
| 2 | 7 | Truth Tables In Action | 2 | 1318 | 52 |  | Checking Argument Validity; Constructing Truth Tables |
| 3 | 2 | Savings Growth Sequences | 2 | 582 | 28 |  | Recursive Savings Formulas; Compound Growth Calculations |
| 3 | 3 | Nature And Counting Patterns | 2 | 950 | 36 |  | Fibonacci Patterns In Nature; Recursive Counting Algorithms |
| 3 | 4 | Predicting Real-World Trends | 2 | 950 | 36 |  | Long-Term Trend Convergence; Modeling Population And Investment Growth |
| 3 | 5 | Optimizing City Networks | 3 | 1425 | 54 |  | Shortest Route Planning; Minimum Cost Network Design; Maximum Traffic Flow Analysis |
| 3 | 6 | Delivery Routes And Scheduling | 2 | 950 | 36 |  | Optimizing Delivery Routes; Conflict-Free Shift Scheduling |
| 3 | 7 | Power Grid Reliability | 1 | 659 | 26 |  | Power Grid Failure Analysis |
| 4 | 2 | Measuring Voting Power | 2 | 582 | 28 |  | Banzhaf Power Index; Coalition Influence Measurement |
| 4 | 3 | Dividing Between Two Parties | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 4 | 4 | Determining Election Outcomes | 3 | 1425 | 54 |  | Arrow's Impossibility Theorem; Comparing Election Methods; Apportioning Legislative Seats |
| 4 | 5 | Dividing Among Groups | 3 | 1425 | 54 |  | Lone-Divider Method; Last-Diminisher Method; Choosing Fair Division Methods |
| 4 | 6 | Managing Digital Information | 2 | 950 | 36 |  | Detecting Data Errors; Data Compression Ratios |
| 4 | 7 | Managing Digital Information - Algorithmic Efficiency | 2 | 1134 | 44 |  | Comparing Algorithm Efficiency; Encrypting Data With Ciphers |
| 4 | 8 | Evaluating Fair Outcomes | 2 | 1318 | 52 |  | Voting Fairness Criteria; Fair Division Criteria |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 180 |
| total_chapters | 36 |
| fill ratio | 20% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=36 is below the lesson-day target range (171-189) for total_lesson_days=180. Course is under-filled.
- Structure check: 3 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 9 |
| prompt tokens | 352452 |
| completion tokens | 39437 |
| max single prompt | 54715 |
| tokens per LO | 9113.7 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 2 | 42142 |
| plan_chapters | 3 | 126292 |
| plan_parts | 1 | 47842 |
| titles | 3 | 136176 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 21385 | 2851 | 26979 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 20757 | 1146 | 16200 | 1 |
| 3 | plan_parts |  | claude-sonnet-5 | 47842 | 3991 | 42407 | 1 |
| 4 | plan_chapters | P1 | claude-sonnet-5 | 54715 | 10682 | 112162 | 1 |
| 5 | plan_chapters | P2 | claude-sonnet-5 | 49134 | 5401 | 61113 | 1 |
| 6 | plan_chapters | P3 | claude-sonnet-5 | 22443 | 10113 | 106429 | 1 |
| 7 | titles | 2 | claude-sonnet-5 | 45365 | 1913 | 23290 | 1 |
| 8 | titles | 3 | claude-sonnet-5 | 44505 | 1373 | 19521 | 1 |
| 9 | titles | 4 | claude-sonnet-5 | 46306 | 1967 | 23509 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 43 |
| distinct titles | 43 |
| avg words per title | 3.16 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Logic And Counting' - 6 understand chapters OK
FINAL: Part 'Sequences And Networks' - 6 understand chapters OK
FINAL: Part 'Fairness And Information' - 7 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
