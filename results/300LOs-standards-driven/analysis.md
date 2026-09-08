# Run analysis — 20260905-142318_300LOs_Synthetic300-Standards_claude_cli

Generated 2026-09-05T14:23:18 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 419.3s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Synthetic300_Standards |
| grade_band | MS |
| subject_area | Mathematics |
| progression | STANDARDS_DRIVEN_PROGRESSION |
| learning objectives | 300 |
| calendar | 5/wk × 128 wk = 640 lesson days |
| minutes_per_lesson | 45 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **129** (top: Equivalent Expressions ×11, Absolute Value ×10, Fraction Division ×9, Measures Of Center ×9, Opposite Numbers ×7, Statistical Questions ×7, Variables ×6, Inequality Solutions ×6, Coordinate Geometry ×6, Nets And Surface Area ×6)

## 3. Output structure

- Parts: **21** (1 overview + 18 content + 2 semester) · Chapters: **377** · Modules: 358 · LO modules: 300
- Content estimate: 115084 words · 8377 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic300_Standards Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Logic and Combinatorics | 16 | 12 | 15 | 12 | 5332 | 392 |
| 3 | understand | Recursive Sequences and Graph Algorithms | 16 | 12 | 15 | 12 | 5516 | 396 |
| 4 | understand | Voting and Fair Division | 16 | 12 | 15 | 12 | 5516 | 400 |
| 5 | understand | Discrete Computing Foundations | 11 | 7 | 10 | 7 | 3509 | 318 |
| 6 | understand | Ratios Rates and Number Operations | 23 | 19 | 22 | 19 | 7001 | 478 |
| 7 | understand | Rational Numbers and Coordinate Plane | 23 | 19 | 22 | 19 | 6817 | 474 |
| 8 | understand | Statistical Measures and Distributions | 26 | 22 | 25 | 22 | 6402 | 488 |
| 9 | understand | Coordinate Plane Reinforcement Practice | 21 | 17 | 20 | 17 | 6051 | 442 |
| 10 | understand | Signed Numbers and Factoring Review | 25 | 21 | 24 | 21 | 7767 | 510 |
| 11 | understand | Expressions and Exponent Rules | 17 | 13 | 16 | 13 | 7647 | 486 |
| 12 | understand | Algebraic Vocabulary and Relationships | 27 | 23 | 26 | 23 | 8165 | 542 |
| 13 | understand | Surface Area and Expression Practice | 19 | 15 | 18 | 15 | 6389 | 446 |
| 14 | understand | Equations and Variable Dependencies | 29 | 25 | 28 | 25 | 9483 | 586 |
| 15 | understand | Polygon Area and Volume Geometry | 20 | 16 | 19 | 16 | 6128 | 436 |
| 16 | understand | Ratio Tables and Unit Conversion | 21 | 17 | 20 | 17 | 6787 | 462 |
| 17 | understand | Data Displays and Statistical Summaries | 22 | 18 | 21 | 18 | 6342 | 468 |
| 18 | understand | Fraction Division and Number Line Practice | 15 | 11 | 14 | 11 | 3753 | 346 |
| 19 | understand | Signed Quantities and Rational Order | 25 | 21 | 24 | 21 | 6479 | 482 |
| 20 | semester | Synthetic300_Standards Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 21 | semester | Synthetic300_Standards Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Arguments and Inference | 1 | 475 | 18 |  | Premises And Conclusions |
| 2 | 3 | Arguments and Inference - Rules | 1 | 475 | 18 |  | Modus Ponens And Tollens |
| 2 | 4 | Fallacies and Validity | 1 | 291 | 14 |  | Common Logical Fallacies |
| 2 | 5 | Fallacies and Validity - Argument | 1 | 659 | 26 |  | Truth Table Validity |
| 2 | 6 | Quantifiers and Counterexamples | 1 | 475 | 18 |  | Universal And Existential Quantifiers |
| 2 | 7 | Quantifiers and Counterexamples (2) | 1 | 475 | 18 |  | Disproving With Counterexamples |
| 2 | 8 | Fundamental Counting Principles | 1 | 475 | 18 |  | Multiplication Counting Principle |
| 2 | 9 | Fundamental Counting Principles - Permutations | 1 | 291 | 14 |  | Permutation Formula Arrangements |
| 2 | 10 | Fundamental Counting Principles - Combinations | 1 | 291 | 14 |  | Combination Formula Selections |
| 2 | 11 | Advanced Counting Strategies | 1 | 475 | 18 |  | Repetition In Arrangements |
| 2 | 12 | Advanced Counting Strategies - Inclusion-Exclusion Principle | 1 | 475 | 18 |  | Inclusion-Exclusion Principle |
| 2 | 13 | Advanced Counting Strategies - Technique Selection | 1 | 475 | 18 |  | Choosing Counting Techniques |
| 3 | 2 | Recursive Sequence Basics | 1 | 291 | 14 |  | Sequence Definitions and Initial Conditions |
| 3 | 3 | Recursive Sequence Basics - Sequences | 1 | 291 | 14 |  | Arithmetic and Geometric Term Calculation |
| 3 | 4 | Applied Recursive Concepts | 1 | 475 | 18 |  | Fibonacci Sequence Modeling |
| 3 | 5 | Applied Recursive Concepts - Algorithms | 1 | 475 | 18 |  | Factorial and Combinatorial Algorithms |
| 3 | 6 | Applied Recursive Concepts - Sequence Convergence | 1 | 475 | 18 |  | Convergence Analysis Using Limits |
| 3 | 7 | Applied Recursive Concepts - Modeling | 1 | 475 | 18 |  | Population Growth and Investment Models |
| 3 | 8 | Weighted Graph Algorithms | 1 | 475 | 18 |  | Dijkstra's Shortest Path Algorithm |
| 3 | 9 | Weighted Graph Algorithms - Minimum Spanning | 1 | 475 | 18 |  | Kruskal's Minimum Spanning Tree |
| 3 | 10 | Weighted Graph Algorithms - Network Flow | 1 | 475 | 18 |  | Ford-Fulkerson Network Flow |
| 3 | 11 | Graph Optimization Problems | 1 | 475 | 18 |  | Solving the Traveling Salesperson Problem |
| 3 | 12 | Graph Optimization Problems - Coloring | 1 | 475 | 18 |  | Graph Coloring for Scheduling |
| 3 | 13 | Network Reliability Analysis | 1 | 659 | 26 |  | Network Connectivity and Critical Paths |
| 4 | 2 | Voting Power and Methods | 1 | 291 | 14 |  | Banzhaf Power Index Calculation |
| 4 | 3 | Voting Power and Methods - Arrow'S Impossibility | 1 | 475 | 18 |  | Arrow's Impossibility Theorem |
| 4 | 4 | Voting Power and Methods (3) | 1 | 475 | 18 |  | Plurality Borda And Runoff Voting |
| 4 | 5 | Apportionment and Fairness | 1 | 475 | 18 |  | Hamilton Jefferson Webster Methods |
| 4 | 6 | Apportionment and Fairness - Voting Criteria | 1 | 659 | 26 |  | Fairness Criteria In Voting |
| 4 | 7 | Fair Division Foundations | 1 | 291 | 14 |  | Shapley-Shubik Power Index |
| 4 | 8 | Fair Division Foundations - Divider-Chooser Method | 1 | 475 | 18 |  | Divider-Chooser Fair Division |
| 4 | 9 | Fair Division Foundations - Lone-Divider Method | 1 | 475 | 18 |  | Lone-Divider Proportional Division |
| 4 | 10 | Fair Division Procedures | 1 | 475 | 18 |  | Last-Diminisher Fair Share Method |
| 4 | 11 | Fair Division Procedures - Adjusted Winner | 1 | 291 | 14 |  | Adjusted Winner Procedure |
| 4 | 12 | Fair Division Evaluation | 1 | 475 | 18 |  | Choosing Fair Division Algorithms |
| 4 | 13 | Fair Division Evaluation - Fairness Criteria | 1 | 659 | 26 |  | Proportionality And Envy-Freeness |
| 5 | 2 | Number Systems and Logic | 1 | 291 | 14 |  | Number Base Conversion |
| 5 | 3 | Number Systems and Logic - Boolean Algebra | 1 | 475 | 18 |  | Boolean Expression Simplification |
| 5 | 4 | Number Systems and Logic - Truth Tables | 1 | 659 | 26 |  | Truth Table Construction |
| 5 | 5 | Data Integrity and Compression | 1 | 475 | 18 |  | Error Detection Codes |
| 5 | 6 | Data Integrity and Compression (2) | 1 | 475 | 18 |  | Data Compression Ratios |
| 5 | 7 | Algorithms and Cryptography | 1 | 659 | 26 |  | Algorithmic Efficiency Analysis |
| 5 | 8 | Algorithms and Cryptography - Cryptographic Methods | 1 | 475 | 18 |  | Caesar Cipher Encryption |
| 6 | 2 | Ratios and Unit Rates | 1 | 291 | 14 |  | Ratio Notation Forms |
| 6 | 3 | Ratios and Unit Rates - Ratio Language | 1 | 291 | 14 |  | Ratio Comparison Language |
| 6 | 4 | Ratios and Unit Rates (3) | 1 | 291 | 14 |  | Unit Rate Calculation |
| 6 | 5 | Ratios and Unit Rates (4) | 1 | 291 | 14 |  | Unit Rate Description |
| 6 | 6 | Ratio Reasoning Applications | 1 | 475 | 18 |  | Percent Problem Solving |
| 6 | 7 | Ratio Reasoning Applications - Measurement Conversion | 1 | 475 | 18 |  | Measurement Unit Conversion |
| 6 | 8 | Ratio Reasoning Applications - Equivalent Ratios | 1 | 475 | 18 |  | Equivalent Ratio Problems |
| 6 | 9 | Dividing Fractions | 1 | 475 | 18 |  | Fraction Division Situations |
| 6 | 10 | Dividing Fractions - Fraction Division | 1 | 475 | 18 |  | Fraction Quotient Solutions |
| 6 | 11 | Dividing Whole Numbers | 1 | 291 | 14 |  | Whole Number Division Algorithm |
| 6 | 12 | Dividing Whole Numbers - Number Division | 1 | 475 | 18 |  | Whole Number Division Applications |
| 6 | 13 | Decimal Operations | 1 | 291 | 14 |  | Decimal Addition Algorithm |
| 6 | 14 | Decimal Operations - Subtraction | 1 | 291 | 14 |  | Decimal Subtraction Algorithm |
| 6 | 15 | Decimal Operations - Multiplication | 1 | 291 | 14 |  | Decimal Multiplication Algorithm |
| 6 | 16 | Decimal Operations - Division | 1 | 291 | 14 |  | Decimal Division Algorithm |
| 6 | 17 | Factoring Whole Numbers | 1 | 291 | 14 |  | Greatest Common Factor Identification |
| 6 | 18 | Factoring Whole Numbers - Distributive Property | 1 | 475 | 18 |  | Distributive Property Factoring |
| 6 | 19 | Factoring Whole Numbers (3) | 1 | 291 | 14 |  | Factored Sum Expressions |
| 6 | 20 | Factoring Whole Numbers - Prime Factorization | 1 | 475 | 18 |  | Prime Factorization Method |
| 7 | 2 | Signed Rational Contexts | 1 | 475 | 18 |  | Opposite Direction Quantities |
| 7 | 3 | Signed Rational Contexts - Numbers Context | 1 | 291 | 14 |  | Rational Number Representation |
| 7 | 4 | Opposite Numbers | 1 | 291 | 14 |  | Number Line Opposite Pairs |
| 7 | 5 | Opposite Numbers (2) | 1 | 291 | 14 |  | Equidistant Opposite Numbers |
| 7 | 6 | Rational Values And Zero | 1 | 475 | 18 |  | Rational Numbers In Real Life |
| 7 | 7 | Rational Values And Zero - Context | 1 | 291 | 14 |  | Zero As Reference Point |
| 7 | 8 | Quadrants And Reflections | 1 | 291 | 14 |  | Coordinate Quadrant Identification |
| 7 | 9 | Quadrants And Reflections - Coordinate | 1 | 291 | 14 |  | X-Axis Reflection Pairs |
| 7 | 10 | Quadrants And Reflections (3) | 1 | 291 | 14 |  | Y-Axis Reflection Pairs |
| 7 | 11 | Graphing And Distance | 1 | 475 | 18 |  | Four-Quadrant Graphing |
| 7 | 12 | Graphing And Distance - Coordinate Plane | 1 | 291 | 14 |  | Horizontal And Vertical Distance |
| 7 | 13 | Graphing And Distance (3) | 1 | 475 | 18 |  | Coordinate Distance Word Problems |
| 7 | 14 | Absolute Value Basics | 1 | 291 | 14 |  | Absolute Value Definition |
| 7 | 15 | Absolute Value Basics (2) | 1 | 291 | 14 |  | Calculating Absolute Value |
| 7 | 16 | Absolute Value Basics (3) | 1 | 475 | 18 |  | Absolute Value Word Problems |
| 7 | 17 | Comparing And Ordering Rationals | 1 | 291 | 14 |  | Comparing Rational Numbers |
| 7 | 18 | Comparing And Ordering Rationals - Rational Number | 1 | 475 | 18 |  | Ordering Rational Numbers |
| 7 | 19 | Absolute Value Applications | 1 | 291 | 14 |  | Comparing Absolute Values |
| 7 | 20 | Absolute Value Applications - Rational Number | 1 | 475 | 18 |  | Rational Number Problem Solving |
| 8 | 2 | Statistical Question Basics | 1 | 291 | 14 |  | Statistical Question Examples |
| 8 | 3 | Statistical Question Basics - Questions | 1 | 291 | 14 |  | Non-Statistical Question Examples |
| 8 | 4 | Statistical Question Basics (3) | 1 | 291 | 14 |  | Justifying Statistical Questions |
| 8 | 5 | Central Tendency Measures | 1 | 291 | 14 |  | Mean Median Mode Calculation |
| 8 | 6 | Central Tendency Measures - Center | 1 | 291 | 14 |  | Choosing Best Measure Of Center |
| 8 | 7 | Central Tendency Measures (3) | 1 | 291 | 14 |  | Interpreting Center In Context |
| 8 | 8 | Variability And Distribution | 1 | 291 | 14 |  | Interpreting Range And IQR |
| 8 | 9 | Variability And Distribution - Data | 1 | 291 | 14 |  | Describing Center And Spread |
| 8 | 10 | Distribution Shape And Context | 1 | 291 | 14 |  | Identifying Distribution Shape |
| 8 | 11 | Distribution Shape And Context - Data Graph | 1 | 291 | 14 |  | Identifying Unusual Data Features |
| 8 | 12 | Distribution Shape And Context - Data Interpretation | 1 | 291 | 14 |  | Interpreting Data Set Context |
| 8 | 13 | Center Value Calculations | 1 | 291 | 14 |  | Calculating Mean Median Mode |
| 8 | 14 | Center Value Calculations - Measures | 1 | 291 | 14 |  | Comparing Measures Of Center |
| 8 | 15 | Center Value Calculations (3) | 1 | 291 | 14 |  | Interpreting Measures Of Center |
| 8 | 16 | Spread And Variability Review | 1 | 291 | 14 |  | Interpreting Variability Measures |
| 8 | 17 | Spread And Variability Review - Center | 1 | 291 | 14 |  | Summarizing Center And Spread |
| 8 | 18 | Shape Features And Context | 1 | 291 | 14 |  | Classifying Distribution Shape |
| 8 | 19 | Shape Features And Context - Data Graph | 1 | 291 | 14 |  | Spotting Unusual Data Features |
| 8 | 20 | Shape Features And Context - Data Interpretation | 1 | 291 | 14 |  | Analyzing Data Set Context |
| 8 | 21 | Statistical Question Practice | 1 | 291 | 14 |  | Writing Statistical Questions |
| 8 | 22 | Statistical Question Practice - Questions | 1 | 291 | 14 |  | Writing Non-Statistical Questions |
| 8 | 23 | Statistical Question Practice (3) | 1 | 291 | 14 |  | Explaining Statistical Questions |
| 9 | 2 | Comparing Rational Numbers | 1 | 291 | 14 |  | Comparing Rational Numbers With Symbols |
| 9 | 3 | Comparing Rational Numbers - Number Comparison | 1 | 475 | 18 |  | Ordering Rational Number Sets |
| 9 | 4 | Comparing Rational Numbers - Absolute Value | 1 | 291 | 14 |  | Comparing Absolute Value Distances |
| 9 | 5 | Comparing Rational Numbers (4) | 1 | 475 | 18 |  | Real-World Rational Comparisons |
| 9 | 6 | Absolute Value Concepts | 1 | 291 | 14 |  | Meaning of Absolute Value |
| 9 | 7 | Absolute Value Concepts (2) | 1 | 291 | 14 |  | Calculating Absolute Value |
| 9 | 8 | Absolute Value Concepts (3) | 1 | 475 | 18 |  | Absolute Value in Context |
| 9 | 9 | Reflections and Quadrants | 1 | 291 | 14 |  | Reflections Across the Y-Axis |
| 9 | 10 | Reflections and Quadrants - Coordinate | 1 | 291 | 14 |  | Reflections Across the X-Axis |
| 9 | 11 | Reflections and Quadrants - Coordinate Plane | 1 | 291 | 14 |  | Identifying Coordinate Plane Quadrants |
| 9 | 12 | Graphing and Distance | 1 | 475 | 18 |  | Graphing Points in Four Quadrants |
| 9 | 13 | Graphing and Distance - Coordinate Distances | 1 | 291 | 14 |  | Distances Between Shared Coordinates |
| 9 | 14 | Graphing and Distance (3) | 1 | 475 | 18 |  | Real-World Coordinate Distance Problems |
| 9 | 15 | Opposite Numbers | 1 | 291 | 14 |  | Identifying Opposite Numbers |
| 9 | 16 | Opposite Numbers (2) | 1 | 291 | 14 |  | Opposite Numbers Equal Distance |
| 9 | 17 | Rational Numbers in Context | 1 | 475 | 18 |  | Rational Numbers in Real Contexts |
| 9 | 18 | Rational Numbers in Context (2) | 1 | 291 | 14 |  | Zero in Real-World Situations |
| 10 | 2 | Signed Number Concepts | 1 | 475 | 18 |  | Positive Negative Direction |
| 10 | 3 | Signed Number Concepts - Numbers | 1 | 291 | 14 |  | Signed Rational Quantities |
| 10 | 4 | Decimal Arithmetic Skills | 1 | 291 | 14 |  | Adding Decimals |
| 10 | 5 | Decimal Arithmetic Skills - Subtraction | 1 | 291 | 14 |  | Subtracting Decimals |
| 10 | 6 | Decimal Arithmetic Skills - Multiplication | 1 | 291 | 14 |  | Multiplying Decimals |
| 10 | 7 | Decimal Arithmetic Skills - Division | 1 | 291 | 14 |  | Dividing Decimals |
| 10 | 8 | Factors and Division | 1 | 475 | 18 |  | Prime Factorization |
| 10 | 9 | Factors and Division - Whole Number | 1 | 291 | 14 |  | Whole Number Division |
| 10 | 10 | Factors and Division (3) | 1 | 475 | 18 |  | Dividing Multi-Digit Numbers |
| 10 | 11 | Greatest Common Factor | 1 | 291 | 14 |  | Finding GCF in Sums |
| 10 | 12 | Greatest Common Factor (2) | 1 | 475 | 18 |  | Distributive Property Factoring |
| 10 | 13 | Greatest Common Factor (3) | 1 | 291 | 14 |  | Factored Expression Form |
| 10 | 14 | Fraction Division Skills | 1 | 475 | 18 |  | Identifying Fraction Division |
| 10 | 15 | Fraction Division Skills (2) | 1 | 475 | 18 |  | Dividing Fractions |
| 10 | 16 | Ratio and Percent Reasoning | 1 | 291 | 14 |  | Ratio Notation Forms |
| 10 | 17 | Ratio and Percent Reasoning - Language | 1 | 291 | 14 |  | Ratio Language |
| 10 | 18 | Ratio and Percent Reasoning - Problems | 1 | 475 | 18 |  | Percent Problem Solving |
| 10 | 19 | Ratio and Rate Applications | 1 | 475 | 18 |  | Measurement Conversion |
| 10 | 20 | Ratio and Rate Applications - Equivalent Ratios | 1 | 475 | 18 |  | Equivalent Ratio Problems |
| 10 | 21 | Ratio and Rate Applications - Unit | 1 | 291 | 14 |  | Calculating Unit Rates |
| 10 | 22 | Ratio and Rate Applications (4) | 1 | 291 | 14 |  | Describing Unit Rates |
| 11 | 2 | Equivalence Reasoning | 1 | 475 | 18 |  | Testing Expression Equivalence |
| 11 | 3 | Equivalence Reasoning - Equivalent Expressions | 1 | 659 | 26 |  | Justifying Expression Equivalence |
| 11 | 4 | Expression Properties | 1 | 659 | 26 |  | Commutative Property Expressions |
| 11 | 5 | Expression Properties - Equivalent Expressions | 1 | 659 | 26 |  | Associative Property Expressions |
| 11 | 6 | Expression Properties (3) | 1 | 659 | 26 |  | Distributive Property Expressions |
| 11 | 7 | Inverse and Identity | 1 | 659 | 26 |  | Inverse Property Expressions |
| 11 | 8 | Inverse and Identity - Equivalent Expressions | 1 | 659 | 26 |  | Identity Property Expressions |
| 11 | 9 | Exponent Expressions | 1 | 291 | 14 |  | Writing Exponent Expressions |
| 11 | 10 | Exponent Expressions - Exponents | 1 | 659 | 26 |  | Evaluating Exponent Expressions |
| 11 | 11 | Exponent Expressions - Whole Number | 1 | 291 | 14 |  | Comparing Exponent Values |
| 11 | 12 | Order of Operations | 1 | 659 | 26 |  | Absolute Value Operations |
| 11 | 13 | Order of Operations (2) | 1 | 659 | 26 |  | Exponents In Operation Order |
| 11 | 14 | Order of Operations (3) | 1 | 659 | 26 |  | Mixed Order Of Operations |
| 12 | 2 | Algebraic Expression Vocabulary | 1 | 291 | 14 |  | Identifying Expression Terms |
| 12 | 3 | Algebraic Expression Vocabulary (2) | 1 | 291 | 14 |  | Identifying Coefficients |
| 12 | 4 | Algebraic Expression Vocabulary (3) | 1 | 291 | 14 |  | Identifying Expression Factors |
| 12 | 5 | Algebraic Expression Vocabulary (4) | 1 | 291 | 14 |  | Sums Products And Quotients |
| 12 | 6 | Variable Interpretation | 1 | 291 | 14 |  | Interpreting Unknown Variables |
| 12 | 7 | Variable Interpretation - Variables | 1 | 291 | 14 |  | Variable Value Constraints |
| 12 | 8 | Writing Algebraic Expressions | 1 | 291 | 14 |  | Translating Verbal Statements To Expressions |
| 12 | 9 | Writing Algebraic Expressions (2) | 1 | 291 | 14 |  | Expressions For Real-World Relationships |
| 12 | 10 | Tables And Graphs | 1 | 659 | 26 |  | Input-Output Tables |
| 12 | 11 | Tables And Graphs (2) | 1 | 659 | 26 |  | Graphing Variable Relationships |
| 12 | 12 | Equations And Substitution | 1 | 291 | 14 |  | Writing Equations From Relationships |
| 12 | 13 | Equations And Substitution - Equation Solutions | 1 | 475 | 18 |  | Verifying Equation Solutions |
| 12 | 14 | Equations And Substitution - Inequality Solutions | 1 | 475 | 18 |  | Verifying Inequality Solutions |
| 12 | 15 | Interpreting Solution Meaning | 1 | 291 | 14 |  | Equation Solution Meaning |
| 12 | 16 | Interpreting Solution Meaning - Inequality Solutions | 1 | 291 | 14 |  | Inequality Solution Meaning |
| 12 | 17 | Inequality Solution Sets | 1 | 291 | 14 |  | Graphing Inequality Solutions |
| 12 | 18 | Inequality Solution Sets - Solutions | 1 | 291 | 14 |  | Infinite Solution Sets |
| 12 | 19 | Polygon Perimeter And Area | 1 | 291 | 14 |  | Perimeter Of Coordinate Polygons |
| 12 | 20 | Polygon Perimeter And Area - Coordinate Geometry | 1 | 291 | 14 |  | Area Of Coordinate Polygons |
| 12 | 21 | Missing Rectangle Vertices | 1 | 475 | 18 |  | Vertices With Shared X-Coordinates |
| 12 | 22 | Missing Rectangle Vertices - Coordinate Geometry | 1 | 475 | 18 |  | Vertices With Shared Y-Coordinates |
| 12 | 23 | Horizontal Vertical Side Lengths | 1 | 291 | 14 |  | Horizontal Side Length |
| 12 | 24 | Horizontal Vertical Side Lengths - Coordinate Geometry | 1 | 291 | 14 |  | Vertical Side Length |
| 13 | 2 | Rectangular Prism Volume | 1 | 291 | 14 |  | Prism Volume Formula Lwh |
| 13 | 3 | Rectangular Prism Volume (2) | 1 | 291 | 14 |  | Prism Volume Base Height |
| 13 | 4 | Rectangular Prism Volume (3) | 1 | 291 | 14 |  | Comparing Prism Volumes |
| 13 | 5 | Area Decomposition Methods | 1 | 291 | 14 |  | Decomposing Irregular Polygons |
| 13 | 6 | Area Decomposition Methods (2) | 1 | 659 | 26 |  | Composing Polygon Shapes |
| 13 | 7 | Area Decomposition Methods (3) | 1 | 475 | 18 |  | Real-World Area Composition |
| 13 | 8 | Surface Area From Nets | 1 | 659 | 26 |  | Building 3D Nets |
| 13 | 9 | Surface Area From Nets (2) | 1 | 291 | 14 |  | Calculating Surface Area From Nets |
| 13 | 10 | Surface Area From Nets (3) | 1 | 475 | 18 |  | Applying Surface Area Problems |
| 13 | 11 | Equivalent Expression Properties | 1 | 475 | 18 |  | Commutative Property Expressions |
| 13 | 12 | Equivalent Expression Properties - Expressions | 1 | 475 | 18 |  | Associative Property Expressions |
| 13 | 13 | Equivalent Expression Properties (3) | 1 | 475 | 18 |  | Distributive Property Expressions |
| 13 | 14 | Equivalent Expression Properties (4) | 1 | 291 | 14 |  | Testing Expression Equivalence |
| 13 | 15 | Exponent Expression Evaluation | 1 | 291 | 14 |  | Writing Exponent Expressions |
| 13 | 16 | Exponent Expression Evaluation - Exponents | 1 | 659 | 26 |  | Evaluating Exponent Expressions |
| 14 | 2 | Evaluating Expressions | 1 | 291 | 14 |  | Substitute Values Into Expressions |
| 14 | 3 | Evaluating Expressions - Expression Evaluation | 1 | 659 | 26 |  | Order Of Operations Evaluation |
| 14 | 4 | Evaluating Expressions (3) | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 14 | 5 | Expression Parts And Writing | 1 | 291 | 14 |  | Naming Expression Parts |
| 14 | 6 | Expression Parts And Writing - Vocabulary | 1 | 291 | 14 |  | Grouping Expression Parts |
| 14 | 7 | Expression Parts And Writing - Expressions | 1 | 291 | 14 |  | Writing Algebraic Expressions |
| 14 | 8 | Writing And Solving Equations | 1 | 291 | 14 |  | Writing Addition Equations |
| 14 | 9 | Writing And Solving Equations - One-Step | 1 | 291 | 14 |  | Writing Multiplication Equations |
| 14 | 10 | Writing And Solving Equations (3) | 1 | 475 | 18 |  | Solving Addition Equations |
| 14 | 11 | Writing And Solving Equations (4) | 1 | 475 | 18 |  | Solving Multiplication Equations |
| 14 | 12 | Checking Equation Solutions | 1 | 291 | 14 |  | Meaning Of Equation Solutions |
| 14 | 13 | Checking Equation Solutions (2) | 1 | 475 | 18 |  | Testing Equation Solutions |
| 14 | 14 | Checking Equation Solutions (3) | 1 | 475 | 18 |  | Testing Inequality Solutions |
| 14 | 15 | Understanding Variables | 1 | 475 | 18 |  | Variables For Unknown Quantities |
| 14 | 16 | Understanding Variables (2) | 1 | 291 | 14 |  | Writing Expressions With Variables |
| 14 | 17 | Understanding Variables (3) | 1 | 291 | 14 |  | Variables As Unknown Numbers |
| 14 | 18 | Understanding Variables (4) | 1 | 291 | 14 |  | Variables Over A Number Set |
| 14 | 19 | Writing And Graphing Inequalities | 1 | 291 | 14 |  | Writing Simple Inequalities |
| 14 | 20 | Writing And Graphing Inequalities - Inequality Solutions | 1 | 291 | 14 |  | Infinite Inequality Solutions |
| 14 | 21 | Writing And Graphing Inequalities (3) | 1 | 291 | 14 |  | Graphing Inequalities On Number Lines |
| 14 | 22 | Independent Dependent Relationships | 1 | 475 | 18 |  | Variables In Changing Relationships |
| 14 | 23 | Independent Dependent Relationships - Variables | 1 | 291 | 14 |  | Equations For Dependent Variables |
| 14 | 24 | Independent Dependent Relationships (3) | 1 | 475 | 18 |  | Dependent Variables In Tables |
| 14 | 25 | Graphing Variable Relationships | 1 | 475 | 18 |  | Dependent Variables In Graphs |
| 14 | 26 | Graphing Variable Relationships - Dependent Independent | 1 | 291 | 14 |  | Linking Tables Graphs Equations |
| 15 | 2 | Coordinate Plane Polygons | 1 | 291 | 14 |  | Plotting Polygon Vertices |
| 15 | 3 | Coordinate Plane Polygons (2) | 1 | 291 | 14 |  | Coordinate Side Lengths |
| 15 | 4 | Coordinate Plane Polygons (3) | 1 | 475 | 18 |  | Coordinate Polygon Applications |
| 15 | 5 | Triangle And Quadrilateral Area | 1 | 291 | 14 |  | Right Triangle Area |
| 15 | 6 | Triangle And Quadrilateral Area - Shapes | 1 | 291 | 14 |  | General Triangle Area |
| 15 | 7 | Triangle And Quadrilateral Area (3) | 1 | 291 | 14 |  | Quadrilateral Area Methods |
| 15 | 8 | Composite Polygon Area | 1 | 291 | 14 |  | Decomposing Polygons For Area |
| 15 | 9 | Composite Polygon Area - Shapes | 1 | 475 | 18 |  | Composite Shape Applications |
| 15 | 10 | Rectangular Prism Volume | 1 | 291 | 14 |  | Unit Cube Volume Packing |
| 15 | 11 | Rectangular Prism Volume - Prisms | 1 | 475 | 18 |  | Cube Packing Versus Edge Product |
| 15 | 12 | Rectangular Prism Volume (3) | 1 | 475 | 18 |  | Volume Via Length Width Height |
| 15 | 13 | Prism Volume Applications | 1 | 475 | 18 |  | Volume Using Base Times Height |
| 15 | 14 | Prism Volume Applications - Rectangular Prisms | 1 | 475 | 18 |  | Prism Volume Word Problems |
| 15 | 15 | Nets And Surface Area | 1 | 475 | 18 |  | Constructing 3D Nets |
| 15 | 16 | Nets And Surface Area (2) | 1 | 291 | 14 |  | Surface Area From Nets |
| 15 | 17 | Nets And Surface Area (3) | 1 | 475 | 18 |  | Surface Area Applications |
| 16 | 2 | Ratio Fundamentals | 1 | 291 | 14 |  | Ratios As Comparisons |
| 16 | 3 | Ratio Fundamentals - Ratios | 1 | 475 | 18 |  | Describing Ratios In Words |
| 16 | 4 | Ratio Fundamentals (3) | 1 | 291 | 14 |  | Ratio Notation |
| 16 | 5 | Unit Rate Fundamentals | 1 | 291 | 14 |  | Defining Unit Rates |
| 16 | 6 | Unit Rate Fundamentals - Rates | 1 | 291 | 14 |  | Calculating Unit Rates |
| 16 | 7 | Unit Rate Fundamentals (3) | 1 | 475 | 18 |  | Rate Language In Context |
| 16 | 8 | Percent Reasoning | 1 | 291 | 14 |  | Finding Percent Of A Quantity |
| 16 | 9 | Percent Reasoning - Problems | 1 | 475 | 18 |  | Finding The Whole From Percent |
| 16 | 10 | Building Ratio Tables | 1 | 659 | 26 |  | Creating Equivalent Ratio Tables |
| 16 | 11 | Building Ratio Tables (2) | 1 | 291 | 14 |  | Missing Values In Ratio Tables |
| 16 | 12 | Ratio Table Applications | 1 | 475 | 18 |  | Graphing Ratio Table Pairs |
| 16 | 13 | Ratio Table Applications - Comparison | 1 | 291 | 14 |  | Comparing Ratios With Tables |
| 16 | 14 | Applying Unit Rates | 1 | 475 | 18 |  | Unit Pricing Problems |
| 16 | 15 | Applying Unit Rates - Rate | 1 | 475 | 18 |  | Constant Speed Problems |
| 16 | 16 | Unit Conversion Methods | 1 | 291 | 14 |  | Converting Measurement Units |
| 16 | 17 | Unit Conversion Methods (2) | 1 | 475 | 18 |  | Unit Conversion In Multiplication |
| 16 | 18 | Unit Conversion Methods (3) | 1 | 475 | 18 |  | Unit Conversion In Division |
| 17 | 2 | Introduction to Statistical Measures | 1 | 291 | 14 |  | Identifying Statistical Questions |
| 17 | 3 | Introduction to Statistical Measures - Center | 1 | 291 | 14 |  | Measures of Center Overview |
| 17 | 4 | Introduction to Statistical Measures - Variability | 1 | 291 | 14 |  | Measures of Variability Overview |
| 17 | 5 | Data Distribution Characteristics | 1 | 291 | 14 |  | Data Distributions in Statistics |
| 17 | 6 | Data Distribution Characteristics (2) | 1 | 291 | 14 |  | Center of a Distribution |
| 17 | 7 | Data Distribution Characteristics (3) | 1 | 291 | 14 |  | Spread of a Distribution |
| 17 | 8 | Data Distribution Characteristics (4) | 1 | 291 | 14 |  | Shape of a Distribution |
| 17 | 9 | Displaying Numerical Data | 1 | 659 | 26 |  | Creating Dot Plots |
| 17 | 10 | Displaying Numerical Data - Histograms | 1 | 659 | 26 |  | Creating Histograms |
| 17 | 11 | Displaying Numerical Data - Box Plots | 1 | 659 | 26 |  | Creating Box Plots |
| 17 | 12 | Calculating Data Measures | 1 | 291 | 14 |  | Attributes of Statistical Investigations |
| 17 | 13 | Calculating Data Measures - Center | 1 | 291 | 14 |  | Calculating Median and Mean |
| 17 | 14 | Calculating Data Measures - Variability | 1 | 291 | 14 |  | Calculating IQR and MAD |
| 17 | 15 | Distribution Patterns and Deviations | 1 | 291 | 14 |  | Describing Distribution Patterns |
| 17 | 16 | Distribution Patterns and Deviations - Data | 1 | 291 | 14 |  | Identifying Data Deviations |
| 17 | 17 | Selecting Statistical Summaries | 1 | 291 | 14 |  | Choosing Measures of Center |
| 17 | 18 | Selecting Statistical Summaries - Measures Variability | 1 | 291 | 14 |  | Choosing Measures of Variability |
| 17 | 19 | Selecting Statistical Summaries (3) | 1 | 291 | 14 |  | Reporting Sample Size |
| 18 | 2 | Fraction Division Basics | 1 | 291 | 14 |  | Meaning of Fraction Quotients |
| 18 | 3 | Fraction Division Basics (2) | 1 | 291 | 14 |  | Dividing Fractions Algorithm |
| 18 | 4 | Fraction Division Basics (3) | 1 | 475 | 18 |  | Fraction Division Word Problems |
| 18 | 5 | Fraction Division Models | 1 | 475 | 18 |  | Fraction Division Visual Models |
| 18 | 6 | Fraction Division Models (2) | 1 | 291 | 14 |  | Equations for Fraction Division |
| 18 | 7 | Coordinate Plane Distances | 1 | 475 | 18 |  | Graphing Four-Quadrant Points |
| 18 | 8 | Coordinate Plane Distances - Distance | 1 | 291 | 14 |  | Horizontal Coordinate Distance |
| 18 | 9 | Coordinate Plane Distances (3) | 1 | 291 | 14 |  | Vertical Coordinate Distance |
| 18 | 10 | Number Line Positioning | 1 | 291 | 14 |  | Horizontal Number Line Placement |
| 18 | 11 | Number Line Positioning - Position | 1 | 291 | 14 |  | Vertical Number Line Placement |
| 18 | 12 | Number Line Positioning - Coordinate Plane | 1 | 291 | 14 |  | Plotting Coordinate Pairs |
| 19 | 2 | Opposite Numbers | 1 | 291 | 14 |  | Opposite Signs On Number Line |
| 19 | 3 | Opposite Numbers (2) | 1 | 291 | 14 |  | Double Opposite Property |
| 19 | 4 | Opposite Numbers (3) | 1 | 291 | 14 |  | Zero As Its Own Opposite |
| 19 | 5 | Coordinate Plane Signs | 1 | 291 | 14 |  | Identifying Quadrants From Signs |
| 19 | 6 | Coordinate Plane Signs - Quadrant Identification | 1 | 291 | 14 |  | Signs Determining Quadrant Location |
| 19 | 7 | Coordinate Plane Signs - Reflections Across | 1 | 291 | 14 |  | Points Differing By Sign |
| 19 | 8 | Coordinate Plane Signs (4) | 1 | 291 | 14 |  | Reflections Across Coordinate Axes |
| 19 | 9 | Number Line Comparisons | 1 | 291 | 14 |  | Absolute Value Versus Order |
| 19 | 10 | Number Line Comparisons - Inequality | 1 | 291 | 14 |  | Inequality As Number Line Position |
| 19 | 11 | Number Line Comparisons (3) | 1 | 291 | 14 |  | Locating Numbers From Inequalities |
| 19 | 12 | Number Line Comparisons (4) | 1 | 291 | 14 |  | Farther Left Or Right |
| 19 | 13 | Absolute Value Magnitude | 1 | 291 | 14 |  | Defining Absolute Value |
| 19 | 14 | Absolute Value Magnitude (2) | 1 | 291 | 14 |  | Calculating Absolute Value |
| 19 | 15 | Absolute Value Magnitude (3) | 1 | 291 | 14 |  | Magnitude Of Positive Quantities |
| 19 | 16 | Absolute Value Magnitude (4) | 1 | 291 | 14 |  | Magnitude Of Negative Quantities |
| 19 | 17 | Rational Number Order | 1 | 291 | 14 |  | Writing Rational Order Statements |
| 19 | 18 | Rational Number Order (2) | 1 | 291 | 14 |  | Interpreting Rational Order Statements |
| 19 | 19 | Rational Number Order (3) | 1 | 291 | 14 |  | Explaining Rational Order Relationships |
| 19 | 20 | Signed Number Quantities | 1 | 291 | 14 |  | Signed Numbers As Directions |
| 19 | 21 | Signed Number Quantities (2) | 1 | 475 | 18 |  | Positive Numbers In Context |
| 19 | 22 | Signed Number Quantities (3) | 1 | 475 | 18 |  | Negative Numbers In Context |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 377 |
| fill ratio | 59% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=377 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 18 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 47 |
| prompt tokens | 1935023 |
| completion tokens | 129988 |
| max single prompt | 102485 |
| tokens per LO | 6883.4 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 221702 |
| plan_chapters | 18 | 778052 |
| plan_parts | 1 | 102485 |
| titles | 18 | 832784 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 22528 | 2595 | 33406 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 22427 | 2873 | 36313 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 22515 | 2523 | 33187 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 22536 | 2697 | 35227 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 22408 | 2702 | 35303 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 22408 | 2727 | 28653 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 22397 | 2313 | 24287 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 21170 | 1098 | 17069 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 22221 | 2479 | 26240 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 21092 | 2749 | 28940 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 102485 | 13192 | 105549 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 22432 | 2723 | 33685 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 47484 | 3076 | 38329 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 50273 | 5748 | 64797 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 45958 | 1883 | 29926 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 47829 | 3200 | 34030 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 48084 | 3176 | 36550 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 22939 | 2933 | 36121 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 22692 | 2689 | 33886 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 48045 | 3987 | 43813 | 1 |
| 21 | plan_chapters | P10 | claude-sonnet-5 | 45688 | 2039 | 23498 | 1 |
| 22 | plan_chapters | P11 | claude-sonnet-5 | 48108 | 3929 | 41294 | 1 |
| 23 | plan_chapters | P12 | claude-sonnet-5 | 45794 | 2184 | 25987 | 1 |
| 24 | plan_chapters | P13 | claude-sonnet-5 | 47521 | 3248 | 33028 | 1 |
| 25 | plan_chapters | P14 | claude-sonnet-5 | 45978 | 2188 | 28198 | 1 |
| 26 | plan_chapters | P15 | claude-sonnet-5 | 46773 | 3322 | 34423 | 1 |
| 27 | plan_chapters | P16 | claude-sonnet-5 | 48522 | 4090 | 43367 | 1 |
| 28 | plan_chapters | P17 | claude-sonnet-5 | 46259 | 2002 | 26409 | 1 |
| 29 | plan_chapters | P18 | claude-sonnet-5 | 47673 | 3614 | 36781 | 1 |
| 30 | titles | 2 | claude-sonnet-5 | 45637 | 1091 | 18887 | 1 |
| 31 | titles | 3 | claude-sonnet-5 | 46312 | 1931 | 24938 | 1 |
| 32 | titles | 4 | claude-sonnet-5 | 46116 | 1522 | 22755 | 1 |
| 33 | titles | 5 | claude-sonnet-5 | 44890 | 849 | 17330 | 1 |
| 34 | titles | 6 | claude-sonnet-5 | 46925 | 1968 | 26543 | 1 |
| 35 | titles | 7 | claude-sonnet-5 | 46764 | 3672 | 34618 | 1 |
| 36 | titles | 8 | claude-sonnet-5 | 46976 | 2454 | 29376 | 1 |
| 37 | titles | 9 | claude-sonnet-5 | 45668 | 1690 | 21915 | 1 |
| 38 | titles | 10 | claude-sonnet-5 | 46314 | 2059 | 23932 | 1 |
| 39 | titles | 11 | claude-sonnet-5 | 46070 | 1652 | 21643 | 1 |
| 40 | titles | 12 | claude-sonnet-5 | 46872 | 2250 | 25454 | 1 |
| 41 | titles | 13 | claude-sonnet-5 | 43485 | 1335 | 22221 | 1 |
| 42 | titles | 14 | claude-sonnet-5 | 47512 | 2058 | 27121 | 1 |
| 43 | titles | 15 | claude-sonnet-5 | 48995 | 3990 | 44092 | 1 |
| 44 | titles | 16 | claude-sonnet-5 | 45193 | 1489 | 21573 | 1 |
| 45 | titles | 17 | claude-sonnet-5 | 47193 | 2431 | 29481 | 1 |
| 46 | titles | 18 | claude-sonnet-5 | 45275 | 1166 | 21556 | 1 |
| 47 | titles | 19 | claude-sonnet-5 | 46587 | 2402 | 29957 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 287 |
| avg words per title | 3.48 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Logic and Combinatorics' - 12 understand chapters OK
FINAL: Part 'Recursive Sequences and Graph Algorithms' - 12 understand chapters OK
FINAL: Part 'Voting and Fair Division' - 12 understand chapters OK
FINAL: Part 'Discrete Computing Foundations' - 7 understand chapters OK
FINAL: Part 'Ratios Rates and Number Operations' - 19 understand chapters OK
FINAL: Part 'Rational Numbers and Coordinate Plane' - 19 understand chapters OK
FINAL: Part 'Statistical Measures and Distributions' - 22 understand chapters OK
FINAL: Part 'Coordinate Plane Reinforcement Practice' - 17 understand chapters OK
FINAL: Part 'Signed Numbers and Factoring Review' - 21 understand chapters OK
FINAL: Part 'Expressions and Exponent Rules' - 13 understand chapters OK
FINAL: Part 'Algebraic Vocabulary and Relationships' - 23 understand chapters OK
FINAL: Part 'Surface Area and Expression Practice' - 15 understand chapters OK
FINAL: Part 'Equations and Variable Dependencies' - 25 understand chapters OK
FINAL: Part 'Polygon Area and Volume Geometry' - 16 understand chapters OK
FINAL: Part 'Ratio Tables and Unit Conversion' - 17 understand chapters OK
FINAL: Part 'Data Displays and Statistical Summaries' - 18 understand chapters OK
FINAL: Part 'Fraction Division and Number Line Practice' - 11 understand chapters OK
FINAL: Part 'Signed Quantities and Rational Order' - 21 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
