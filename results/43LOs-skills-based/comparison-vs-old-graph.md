# 43 LOs — old Berlin graph vs new LangGraph pipeline

- Input: `Test_Math` · MS · Math · SKILLS_BASED_PROGRESSION
- Old response: `berlin-tool-node/tool-response-43-lg-new.txt` → `runs/old-graph/outline-43.json`
- New run: `20260827-203356_43LOs_Test-Math_claude_cli`

## Structure

| metric | OLD | NEW |
| --- | --- | --- |
| content parts | 7 | 4 |
| understand chapters | 43 | 25 |
| understand per part | [6, 6, 6, 6, 6, 6, 7] | [4, 7, 6, 8] |
| min understand per part | 6 | 4 |
| avg LOs per chapter | 1.0 | 1.72 |
| single-LO chapters | 43 | 8 |
| LOs placed | 43 | 43 |
| missing LOs | 0 | 0 |
| total_parts | 10 | 7 |
| total_chapters | 76 | 46 |
| pacing overrun | False | False |
| invariant failures | 0 | 0 |
| LLM calls | 4 | 14 |
| completion tokens (model output) | 37084 | 29928 |
| largest single prompt (own tokens) | 22k–44k (planner forward) | 69862 |
| fallbacks | n/a | {} |
| wall time (s) | n/a | 186 |

## Unit (part) names

| # | OLD | NEW |
| --- | --- | --- |
| 1 | Logic and Proof | Logical Reasoning And Argumentation |
| 2 | Counting and Combinatorics | Counting Combinatorics & Number Systems |
| 3 | Recursion and Sequences | Sequences Recursive & Graph Theory |
| 4 | Graph Algorithms | Voting Theory & Fair Division |
| 5 | Voting and Apportionment |  |
| 6 | Fair Division |  |
| 7 | Discrete Structures in Computing |  |

## Per-LO placement and titles

Same LO, old vs new: which unit/chapter it landed in and the module title generated.

| # | objective | OLD unit | OLD chapter | OLD title | NEW unit | NEW chapter | NEW title | NEW tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Construct valid logical arguments using premises and conclusions in sy | Logic and Proof | Symbolic Arguments | Symbolic Premises and Conclusions | Logical Reasoning And Argumentation | Valid Arguments | Symbolic Argument Construction | Intermediate |
| 2 | Apply rules of inference including modus ponens and modus tollens to d | Logic and Proof | Inference Rules | Modus Ponens and Modus Tollens | Logical Reasoning And Argumentation | Valid Arguments | Modus Ponens And Tollens | Intermediate |
| 3 | Identify logical fallacies in arguments including ad hominem, straw ma | Logic and Proof | Argument Fallacies | Logical Fallacy Identification | Logical Reasoning And Argumentation | Logical Fallacies | Spotting Logical Fallacies | Foundational |
| 4 | Evaluate the validity of deductive arguments using truth tables and lo | Logic and Proof | Deductive Validity | Truth Tables for Validity | Logical Reasoning And Argumentation | Truth Tables | Evaluating Argument Validity | Advanced |
| 5 | Apply quantifiers including universal and existential quantifiers to e | Logic and Proof | Quantified Statements | Universal and Existential Quantifiers | Logical Reasoning And Argumentation | Quantifiers And Counterexamples | Universal And Existential Quantifiers | Intermediate |
| 6 | Construct counterexamples to disprove invalid logical statements or co | Logic and Proof | Counterexample Reasoning | Counterexample Construction | Logical Reasoning And Argumentation | Quantifiers And Counterexamples | Constructing Counterexamples | Intermediate |
| 7 | Apply the multiplication principle to calculate the number of outcomes | Counting and Combinatorics | Multiplication Principle | Multiplication Principle Outcomes | Counting Combinatorics & Number Systems | Multiplication And Repetition | Multiplication Principle Basics | Intermediate |
| 8 | Calculate permutations of distinct objects using the formula nPr = n!/ | Counting and Combinatorics | Permutations | Permutation Formula nPr | Counting Combinatorics & Number Systems | Permutations And Combinations | Permutations Of Distinct Objects | Foundational |
| 9 | Calculate combinations of distinct objects using the formula nCr = n!/ | Counting and Combinatorics | Combinations | Combination Formula nCr | Counting Combinatorics & Number Systems | Permutations And Combinations | Combinations Of Distinct Objects | Foundational |
| 10 | Solve counting problems involving arrangements with repetition using e | Counting and Combinatorics | Counting With Repetition | Repetition Counting Exponents | Counting Combinatorics & Number Systems | Multiplication And Repetition | Arrangements With Repetition | Intermediate |
| 11 | Apply the inclusion-exclusion principle to determine the number of ele | Counting and Combinatorics | Inclusion-Exclusion | Inclusion-Exclusion for Sets | Counting Combinatorics & Number Systems | Combining Counting Techniques | Inclusion-Exclusion Principle | Intermediate |
| 12 | Analyze counting scenarios to determine which counting technique is mo | Counting and Combinatorics | Technique Selection | Choosing Counting Techniques | Counting Combinatorics & Number Systems | Combining Counting Techniques | Choosing Counting Techniques | Intermediate |
| 13 | Define recursive sequences using explicit formulas and initial conditi | Recursion and Sequences | Recursive Definitions | Recursive Sequence Definitions | Sequences Recursive & Graph Theory | Recursive Sequence Basics | Defining Recursive Sequences | Foundational |
| 14 | Calculate terms of recursive sequences including arithmetic and geomet | Recursion and Sequences | Recursive Terms | Computing Recursive Terms | Sequences Recursive & Graph Theory | Recursive Sequence Basics | Calculating Sequence Terms | Foundational |
| 15 | Apply the Fibonacci sequence and its properties to solve modeling prob | Recursion and Sequences | Fibonacci Modeling | Fibonacci Modeling Applications | Sequences Recursive & Graph Theory | Fibonacci And Recursive Algorithms | Fibonacci Modeling Applications | Intermediate |
| 16 | Implement recursive algorithms to solve problems involving factorial a | Recursion and Sequences | Recursive Algorithms | Recursive Factorial Algorithms | Sequences Recursive & Graph Theory | Fibonacci And Recursive Algorithms | Recursive Algorithm Implementation | Intermediate |
| 17 | Analyze the convergence behavior of recursive sequences using limit te | Recursion and Sequences | Convergence Analysis | Limits in Recursive Convergence | Sequences Recursive & Graph Theory | Convergence And Modeling | Sequence Convergence Analysis | Intermediate |
| 18 | Model real-world phenomena using recursive relationships including pop | Recursion and Sequences | Recursive Phenomena | Modeling Recursive Growth | Sequences Recursive & Graph Theory | Convergence And Modeling | Modeling Growth With Recursion | Intermediate |
| 19 | Apply Dijkstra's algorithm to find the shortest path between vertices  | Graph Algorithms | Shortest Paths | Dijkstra Shortest Paths | Sequences Recursive & Graph Theory | Graph Optimization Algorithms | Dijkstra's Shortest Path | Intermediate |
| 20 | Implement Kruskal's algorithm to determine the minimum spanning tree o | Graph Algorithms | Minimum Spanning Trees | Kruskal Minimum Spanning Tree | Sequences Recursive & Graph Theory | Graph Optimization Algorithms | Kruskal's Minimum Spanning Tree | Intermediate |
| 21 | Analyze network flow problems using the Ford-Fulkerson method to find  | Graph Algorithms | Maximum Flow | Ford-Fulkerson Maximum Flow | Sequences Recursive & Graph Theory | Graph Optimization Algorithms | Ford-Fulkerson Max Flow | Intermediate |
| 22 | Solve the traveling salesperson problem using nearest neighbor and bru | Graph Algorithms | Route Optimization | Traveling Salesperson Heuristics | Sequences Recursive & Graph Theory | Combinatorial Graph Problems | Traveling Salesperson Algorithms | Intermediate |
| 23 | Apply graph coloring algorithms to solve scheduling and assignment pro | Graph Algorithms | Graph Coloring | Graph Coloring for Scheduling | Sequences Recursive & Graph Theory | Combinatorial Graph Problems | Graph Coloring Scheduling | Intermediate |
| 24 | Evaluate network reliability by calculating connectivity and identifyi | Graph Algorithms | Network Reliability | Critical Paths and Connectivity | Sequences Recursive & Graph Theory | Network Reliability Analysis | Network Connectivity Evaluation | Advanced |
| 25 | Calculate voting power indices such as the Banzhaf power index for wei | Voting and Apportionment | Voting Power | Banzhaf Power Index | Voting Theory & Fair Division | Voting Power Indices | Banzhaf Power Index | Foundational |
| 26 | Apply Arrow's Impossibility Theorem to analyze the limitations of voti | Voting and Apportionment | Arrow's Theorem | Arrow Impossibility Analysis | Voting Theory & Fair Division | Arrow's Impossibility Theorem | Limits Of Voting Systems | Intermediate |
| 27 | Implement different voting methods including plurality, Borda count, a | Voting and Apportionment | Voting Procedures | Plurality, Borda, and Runoff | Voting Theory & Fair Division | Voting Methods | Plurality Borda And Runoff | Intermediate |
| 28 | Analyze apportionment methods such as Hamilton's, Jefferson's, and Web | Voting and Apportionment | Apportionment | Hamilton, Jefferson, Webster Methods | Voting Theory & Fair Division | Apportionment Methods | Hamilton Jefferson Webster Methods | Intermediate |
| 29 | Evaluate voting systems against fairness criteria including majority c | Voting and Apportionment | Fairness Evaluation | Voting Fairness Criteria | Voting Theory & Fair Division | Evaluating Fairness Criteria | Assessing Voting Fairness Standards | Advanced |
| 30 | Calculate the Shapley-Shubik power index to measure influence in coali | Voting and Apportionment | Coalition Power | Shapley-Shubik Power Index | Voting Theory & Fair Division | Voting Power Indices | Shapley-Shubik Power Index | Foundational |
| 31 | Apply the divider-chooser method to divide goods or resources fairly b | Fair Division | Divider-Chooser | Divider-Chooser Fair Split | Voting Theory & Fair Division | Two-Party Fair Division | Divider-Chooser Method | Intermediate |
| 32 | Implement the lone-divider method to achieve proportional division amo | Fair Division | Lone-Divider | Lone-Divider Proportional Division | Voting Theory & Fair Division | Multi-Party Division Methods | Lone-Divider Method | Intermediate |
| 33 | Execute the last-diminisher method to ensure each participant receives | Fair Division | Last Diminisher | Last-Diminisher Procedure | Voting Theory & Fair Division | Multi-Party Division Methods | Last-Diminisher Method | Intermediate |
| 34 | Calculate fair shares using the adjusted winner procedure for two-part | Fair Division | Adjusted Winner | Adjusted Winner Fair Shares | Voting Theory & Fair Division | Two-Party Fair Division | Adjusted Winner Procedure | Foundational |
| 35 | Analyze real-world scenarios to determine which fair division algorith | Fair Division | Algorithm Selection | Selecting Fair Division Algorithms | Voting Theory & Fair Division | Fair Division Applications | Selecting Fair Division Algorithms | Intermediate |
| 36 | Evaluate the fairness of proposed divisions using mathematical criteri | Fair Division | Fairness Criteria | Proportionality and Envy-Freeness | Voting Theory & Fair Division | Fair Division Applications | Proportionality And Envy-Freeness | Advanced |
| 37 | Convert between different number bases including binary, octal, and he | Discrete Structures in Computing | Number Base Systems | Converting Number Bases | Counting Combinatorics & Number Systems | Number Base Systems | Number Base Conversion | Foundational |
| 38 | Apply Boolean algebra operations including AND, OR, and NOT to simplif | Discrete Structures in Computing | Boolean Algebra | Simplifying Boolean Expressions | Counting Combinatorics & Number Systems | Boolean Logic And Parity | Boolean Algebra Simplification | Intermediate |
| 39 | Design truth tables to represent logical relationships and evaluate co | Discrete Structures in Computing | Truth Table Design | Designing Compound Truth Tables | Logical Reasoning And Argumentation | Truth Tables | Designing Truth Tables | Advanced |
| 40 | Implement error-detection codes such as check digits and parity bits t | Discrete Structures in Computing | Error Detection | Parity Bits and Check Digits | Counting Combinatorics & Number Systems | Boolean Logic And Parity | Error-Detection Codes | Intermediate |
| 41 | Analyze data compression techniques to calculate compression ratios an | Discrete Structures in Computing | Data Compression | Compression Ratios and Efficiency | Counting Combinatorics & Number Systems | Compression And Cryptography | Data Compression Ratios | Intermediate |
| 42 | Evaluate algorithmic efficiency by comparing time and space complexity | Discrete Structures in Computing | Complexity Analysis | Comparing Time and Space Complexity | Counting Combinatorics & Number Systems | Algorithmic Complexity Analysis | Algorithmic Efficiency Analysis | Advanced |
| 43 | Apply cryptographic methods including Caesar ciphers and modular arith | Discrete Structures in Computing | Cryptographic Methods | Caesar Ciphers and Modular Arithmetic | Counting Combinatorics & Number Systems | Compression And Cryptography | Caesar Cipher Encryption | Intermediate |

## Title agreement

- identical module titles old vs new: 7/43 (differences are expected — both are valid phrasings; judge quality, not equality)
