# Run analysis — 20260905-145240_300LOs_Synthetic-300-regen-Fraction-And-Whole-N_claude_cli

Generated 2026-09-05T14:52:40 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 108.9s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Synthetic_300 |
| grade_band | MS |
| subject_area | Mathematics |
| progression | SKILLS_BASED_PROGRESSION |
| learning objectives | 300 |
| calendar | 5/wk × 128 wk = 640 lesson days |
| minutes_per_lesson | 45 |
| chapter word limit | 2000 |
| user_prompt | make lesson names more application-focused |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **142** (top: Equivalent Expressions ×11, Absolute Value ×10, Measures Of Center ×9, Data Distribution ×8, Prism Volume ×8, Opposite Numbers ×7, Statistical Questions ×7, Fraction Division ×7, Rational Number Comparison ×6, Fair Division ×5)

## 3. Output structure

- Parts: **21** (1 overview + 18 content + 2 semester) · Chapters: **233** · Modules: 358 · LO modules: 300
- Content estimate: 115084 words · 8377 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic_300 Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Ratios Rates And Percents | 19 | 15 | 34 | 31 | 11965 | 682 |
| 3 | understand | Fraction And Whole Number Division | 11 | 7 | 16 | 13 | 5255 | 394 |
| 4 | understand | Decimals Factors And Multiples | 12 | 8 | 19 | 16 | 5392 | 420 |
| 5 | understand | Integers And Signed Numbers | 12 | 8 | 21 | 18 | 6342 | 456 |
| 6 | understand | Absolute Value And Number Comparison | 14 | 10 | 26 | 23 | 8165 | 538 |
| 7 | understand | The Cartesian Plane | 14 | 10 | 25 | 22 | 7322 | 508 |
| 8 | understand | Statistical Questions And Center Measures | 13 | 9 | 24 | 21 | 6111 | 474 |
| 9 | understand | Data Distribution And Summary | 14 | 10 | 22 | 19 | 6633 | 482 |
| 10 | understand | Algebraic Terms And Evaluation | 12 | 8 | 18 | 15 | 5101 | 414 |
| 11 | understand | Exponents And Equivalent Expressions | 16 | 12 | 21 | 18 | 9654 | 568 |
| 12 | understand | Equations Inequalities And Relationships | 21 | 17 | 33 | 30 | 11306 | 664 |
| 13 | understand | Coordinate Geometry And Area | 13 | 9 | 20 | 17 | 6235 | 450 |
| 14 | understand | Volume And Surface Area | 12 | 8 | 17 | 14 | 5730 | 416 |
| 15 | understand | Logical Reasoning And Argumentation | 8 | 4 | 9 | 6 | 2850 | 292 |
| 16 | understand | Counting Combinatorics & Sequences Recursion | 10 | 6 | 15 | 12 | 4964 | 380 |
| 17 | understand | Graph Theory & Voting Apportionment | 11 | 7 | 15 | 12 | 5700 | 404 |
| 18 | understand | Equitable Resource Allocation | 8 | 4 | 9 | 6 | 2850 | 292 |
| 19 | understand | Number Systems And Information Theory | 8 | 4 | 10 | 7 | 3509 | 318 |
| 20 | semester | Synthetic_300 Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 21 | semester | Synthetic_300 Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Ratio Definitions And Notation | 3 | 873 | 42 |  | Notation Forms For Ratios; Writing Ratios Three Ways; Defining Ratios |
| 2 | 3 | Ratio Language And Terminology | 3 | 873 | 42 |  | Describing Ratio Relationships; Ratio Language In Context; Ratio Notation And Terms |
| 2 | 4 | Unit Rate Fundamentals | 3 | 873 | 42 |  | Calculating Unit Rates; Finding Unit Rates From Ratios; Defining Unit Rate |
| 2 | 5 | Expressing Unit Rates | 3 | 873 | 42 |  | Unit Rates With Units; Expressing Rates With Units; Unit Rate Calculations |
| 2 | 6 | Ratio Reasoning Applications | 3 | 873 | 42 |  | Percent As Rate Per Hundred; Completing Ratio Tables; Comparing Ratios With Tables |
| 2 | 7 | Ratio Reasoning Applications - Unit Conversion | 1 | 291 | 14 |  | Converting Units With Ratios |
| 2 | 8 | Equivalent Ratios And Graphs | 2 | 950 | 36 |  | Solving With Equivalent Ratios; Equivalent Ratio Strategies |
| 2 | 9 | Equivalent Ratios And Graphs - Ratio Tables | 1 | 475 | 18 |  | Graphing Ratio Table Values |
| 2 | 10 | Unit Rate Applications | 2 | 950 | 36 |  | Ratios In Word Form; Real-World Rate Language |
| 2 | 11 | Unit Rate Applications (2) | 2 | 950 | 36 |  | Unit Pricing Problems; Constant Speed Problems |
| 2 | 12 | Percent Problem Solving | 2 | 950 | 36 |  | Solving Percent Problems; Percent Reasoning Strategies |
| 2 | 13 | Percent Problem Solving - Problems | 1 | 475 | 18 |  | Finding The Whole From Percent |
| 2 | 14 | Unit Conversion Applications | 2 | 950 | 36 |  | Measurement Conversion Problems; Converting Measurements With Rates |
| 2 | 15 | Unit Conversion Applications (2) | 2 | 950 | 36 |  | Units When Multiplying Quantities; Units When Dividing Quantities |
| 2 | 16 | Constructing Ratio Tables | 1 | 659 | 26 |  | Building Ratio Tables |
| 3 | 2 | Solving Long Division | 2 | 582 | 28 |  | Dividing Multi-Digit Numbers; Long Division Word Problems |
| 3 | 3 | Computing Fraction Quotients | 3 | 873 | 42 |  | Meaning Of Fraction Quotients; Fraction-By-Fraction Division; Writing Fraction Division Equations |
| 3 | 4 | Practical Whole Number Division | 2 | 950 | 36 |  | Applying Division To Real Problems; Real-World Whole Number Division |
| 3 | 5 | Fraction Division In Context | 2 | 950 | 36 |  | Recognizing Division In Word Problems; Determining When To Divide Fractions |
| 3 | 6 | Fraction Division In Context (2) | 1 | 475 | 18 |  | Applying Fraction Division To Word Problems |
| 3 | 7 | Modeling Fraction Quotients | 2 | 950 | 36 |  | Using Division To Solve Problems; Making Sense Of Quotients In Context |
| 3 | 8 | Modeling Fraction Quotients - Division | 1 | 475 | 18 |  | Modeling Fraction Division Visually |
| 4 | 2 | Decimal Addition And Subtraction | 3 | 873 | 42 |  | Adding Multi-Digit Decimals; Subtracting Multi-Digit Decimals; Decimal Sum Algorithm |
| 4 | 3 | Decimal Addition And Subtraction (2) | 1 | 291 | 14 |  | Decimal Difference Algorithm |
| 4 | 4 | Decimal Multiplication And Division | 3 | 873 | 42 |  | Multiplying Multi-Digit Decimals; Dividing Multi-Digit Decimals; Decimal Product Algorithm |
| 4 | 5 | Decimal Multiplication And Division (2) | 1 | 291 | 14 |  | Decimal Quotient Algorithm |
| 4 | 6 | Factoring Common Factors | 3 | 873 | 42 |  | Finding Common Factors In Sums; Factoring Out Common Sums; Shared Factor Identification |
| 4 | 7 | Factoring Common Factors - Greatest Factor | 1 | 291 | 14 |  | Rewriting Sums As Products |
| 4 | 8 | Distributive Property Factoring | 2 | 950 | 36 |  | Factoring With Distributive Property; Distributive Property For GCF |
| 4 | 9 | Prime Factorization | 2 | 950 | 36 |  | Prime Factorization Of Numbers; Breaking Numbers Into Primes |
| 5 | 2 | Identifying Opposite Pairs | 3 | 873 | 42 |  | Opposites On A Number Line; Locating Opposite Pairs; Opposite Signs And Zero |
| 5 | 3 | Opposite Number Properties | 3 | 873 | 42 |  | Equal Distance From Zero; Distance From Zero Examples; Opposite Of An Opposite |
| 5 | 4 | Opposite Number Properties - Numbers | 1 | 291 | 14 |  | Zero As Its Own Opposite |
| 5 | 5 | Meaning Of Zero And Signs | 3 | 873 | 42 |  | Meaning Of Zero In Context; Zero In Real-World Situations; Signs Show Opposite Directions |
| 5 | 6 | Representing Signed Quantities | 2 | 582 | 28 |  | Choosing Positive Or Negative Values; Representing Quantities With Signed Numbers |
| 5 | 7 | Signed Numbers In Context | 2 | 950 | 36 |  | Signed Numbers For Real Situations; Above And Below Sea Level |
| 5 | 8 | Signed Numbers In Context - Number Meaning | 2 | 950 | 36 |  | Positive Numbers In Context; Negative Numbers In Context |
| 5 | 9 | Rational Numbers In Real Contexts | 2 | 950 | 36 |  | Temperature Elevation And Balances; Rational Numbers For Real Quantities |
| 6 | 2 | Understanding Absolute Value | 3 | 873 | 42 |  | Absolute Value As Distance; Distance From Zero Concept; Defining Absolute Value |
| 6 | 3 | Calculating Absolute Value | 3 | 873 | 42 |  | Absolute Value Of Integers; Computing Absolute Values; Absolute Value Of Rationals |
| 6 | 4 | Absolute Value Magnitude | 2 | 582 | 28 |  | Magnitude Of Positive Quantities; Magnitude Of Negative Quantities |
| 6 | 5 | Comparing Rational Numbers | 2 | 582 | 28 |  | Comparing With Inequality Symbols; Number Line Comparisons |
| 6 | 6 | Rational Number Order Statements | 3 | 873 | 42 |  | Writing Order Statements; Interpreting Order Statements; Explaining Order Relationships |
| 6 | 7 | Absolute Value Vs Order | 3 | 873 | 42 |  | Comparing Distance From Zero; Greater Absolute Value; Absolute Value Versus Order |
| 6 | 8 | Ordering Rational Numbers | 2 | 950 | 36 |  | Ordering Least To Greatest; Ordering Greatest To Least |
| 6 | 9 | Applying Rational Comparisons | 2 | 950 | 36 |  | Real World Number Comparisons; Solving Comparison Problems |
| 6 | 10 | Absolute Value Applications | 2 | 950 | 36 |  | Absolute Value In Context; Distance And Temperature Problems |
| 6 | 11 | Absolute Value Applications (2) | 1 | 659 | 26 |  | Order Of Operations With Absolute Value |
| 7 | 2 | Plotting Points Basics | 3 | 873 | 42 |  | Horizontal Number Line Placement; Vertical Number Line Placement; Plotting Coordinate Pairs |
| 7 | 3 | Quadrant Identification | 3 | 873 | 42 |  | Determining Quadrant From Signs; Sign Patterns And Quadrants; Locating Points By Quadrant |
| 7 | 4 | Quadrant Identification (2) | 1 | 291 | 14 |  | Explaining Sign Rules For Quadrants |
| 7 | 5 | Recognizing Axis Reflections | 3 | 873 | 42 |  | Reflections Across The X-Axis; Reflections Across The Y-Axis; Spotting Sign-Only Differences |
| 7 | 6 | Describing Axis Reflections | 3 | 873 | 42 |  | Y-Axis Reflection Pairs; X-Axis Reflection Pairs; Explaining Axis Reflection Relationships |
| 7 | 7 | Coordinate Distance Basics | 3 | 873 | 42 |  | Distance Along Shared Coordinates; Finding Distance With Shared Coordinate; Horizontal Distance Via Absolute Value |
| 7 | 8 | Coordinate Distance Basics (2) | 1 | 291 | 14 |  | Vertical Distance Via Absolute Value |
| 7 | 9 | Graphing Ordered Pairs | 2 | 950 | 36 |  | Plotting Points In Four Quadrants; Graphing Pairs Across Quadrants |
| 7 | 10 | Graphing Ordered Pairs - Coordinate Plane | 1 | 475 | 18 |  | Graphing Points For Real-World Problems |
| 7 | 11 | Coordinate Distance Applications | 2 | 950 | 36 |  | Solving Real-World Distance Problems; Applying Coordinates To Distance Problems |
| 8 | 2 | Recognizing Statistical Questions | 3 | 873 | 42 |  | Writing Statistical Questions; Identifying Response Variability; Statistical Question Criteria |
| 8 | 3 | Evaluating Statistical Questions | 3 | 873 | 42 |  | Deterministic Question Examples; Justifying Statistical Questions; Non-Statistical Question Examples |
| 8 | 4 | Evaluating Statistical Questions (2) | 1 | 291 | 14 |  | Statistical Question Justification |
| 8 | 5 | Calculating Central Tendency | 3 | 873 | 42 |  | Mean Median And Mode; Finding Central Tendency Values; Single-Number Data Summaries |
| 8 | 6 | Calculating Central Tendency - Measures Center | 1 | 291 | 14 |  | Median And Mean Calculations |
| 8 | 7 | Selecting Center Measures | 3 | 873 | 42 |  | Comparing Measures Of Center; Choosing Best Center Measure; Center Measures And Distribution Shape |
| 8 | 8 | Interpreting Center Measures | 2 | 582 | 28 |  | Interpreting Center In Context; Explaining Center Measure Meaning |
| 8 | 9 | Calculating Data Variability | 2 | 582 | 28 |  | Summarizing Spread With One Number; Calculating IQR And MAD |
| 8 | 10 | Interpreting Data Variability | 3 | 873 | 42 |  | Interpreting Range And IQR; Explaining Data Spread Meaning; Variability Measures And Distribution Shape |
| 9 | 2 | Statistical Investigation Basics | 3 | 873 | 42 |  | Data Sets As Distributions; Measurement Attributes And Units; Counting Data Observations |
| 9 | 3 | Distribution Characteristics | 3 | 873 | 42 |  | Measures Of Center; Measures Of Spread; Distribution Shape Identification |
| 9 | 4 | Reading Graphical Displays | 3 | 873 | 42 |  | Center And Spread In Graphs; Symmetric And Skewed Shapes; Summarizing Graph Center Spread |
| 9 | 5 | Reading Graphical Displays - Distribution Shape | 1 | 291 | 14 |  | Skewed Versus Symmetric Data |
| 9 | 6 | Distribution Features And Context | 3 | 873 | 42 |  | Gaps Peaks And Clusters; Interpreting Data Context; Outliers And Data Clusters |
| 9 | 7 | Distribution Features And Context - Data Interpretation | 1 | 291 | 14 |  | Context From Data Patterns |
| 9 | 8 | Patterns And Deviations | 2 | 582 | 28 |  | Overall Data Patterns; Deviations From Patterns |
| 9 | 9 | Creating Data Displays | 1 | 659 | 26 |  | Constructing Dot Plots |
| 9 | 10 | Creating Data Displays (2) | 1 | 659 | 26 |  | Constructing Histograms |
| 9 | 11 | Creating Data Displays (3) | 1 | 659 | 26 |  | Constructing Box Plots |
| 10 | 2 | Understanding Variables | 2 | 582 | 28 |  | Interpreting Variables; Variable Value Constraints |
| 10 | 3 | Expression Vocabulary | 3 | 873 | 42 |  | Naming Expression Terms; Identifying Coefficients; Identifying Factors |
| 10 | 4 | Expression Vocabulary - Sums Products | 1 | 291 | 14 |  | Sums Products And Quotients |
| 10 | 5 | Analyzing Expression Parts | 3 | 873 | 42 |  | Substituting Values For Variables; Expression Part Vocabulary; Grouping Expression Parts |
| 10 | 6 | Writing Algebraic Expressions | 3 | 873 | 42 |  | Expressions From Verbal Statements; Expressions For Real-World Quantities; Recording Operations As Expressions |
| 10 | 7 | Writing Algebraic Expressions (2) | 1 | 291 | 14 |  | Expressions For Problem Solving |
| 10 | 8 | Evaluating Expressions | 1 | 659 | 26 |  | Order Of Operations |
| 10 | 9 | Evaluating Expressions - Formula Evaluation | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 11 | 2 | Exponential Notation Basics | 3 | 873 | 42 |  | Writing Exponential Expressions; Comparing Exponent Values; Modeling Situations With Exponents |
| 11 | 3 | Commutative Property Expressions | 2 | 1134 | 44 |  | Commutative Property Applications; Rewriting Expressions Commutatively |
| 11 | 4 | Associative Property Expressions | 2 | 1134 | 44 |  | Associative Property Applications; Regrouping Terms And Factors |
| 11 | 5 | Distributive Property Expressions | 2 | 1134 | 44 |  | Distributive Property Applications; Expanding Expressions With Distribution |
| 11 | 6 | Inverse And Identity Properties | 1 | 659 | 26 |  | Inverse Property Applications |
| 11 | 7 | Inverse And Identity Properties - Equivalent Expressions | 1 | 659 | 26 |  | Identity Property Applications |
| 11 | 8 | Evaluating Expression Equivalence | 2 | 1134 | 44 |  | Testing Expression Equivalence; Justifying Equivalence Reasoning |
| 11 | 9 | Evaluating Expression Equivalence - Equivalent Expressions | 1 | 291 | 14 |  | Verifying Equivalence By Substitution |
| 11 | 10 | Exponential Expression Evaluation | 1 | 659 | 26 |  | Evaluating Exponential Expressions |
| 11 | 11 | Exponential Expression Evaluation - Exponents | 1 | 659 | 26 |  | Applying Order Of Operations With Exponents |
| 11 | 12 | Exponential Expression Evaluation - Absolute Value | 1 | 659 | 26 |  | Evaluating Absolute Value And Exponents |
| 11 | 13 | Exponential Expression Evaluation - Expressions | 1 | 659 | 26 |  | Evaluating Numerical Exponent Expressions |
| 12 | 2 | Variable Representation | 2 | 766 | 32 |  | Variables In Real-World Problems; Variable As Unknown Number |
| 12 | 3 | Variable Representation (2) | 1 | 291 | 14 |  | Variables Representing Number Sets |
| 12 | 4 | Solution Meaning And Testing | 2 | 766 | 32 |  | Meaning Of A Solution; Testing Equation Solutions |
| 12 | 5 | Solution Meaning And Testing - Inequality Truth | 1 | 475 | 18 |  | Testing Inequality Solutions |
| 12 | 6 | Equation And Inequality Solutions | 2 | 950 | 36 |  | Checking Equation Solutions; Checking Inequality Solutions |
| 12 | 7 | Equation And Inequality Solutions - Equations Inequalities | 2 | 582 | 28 |  | Interpreting Equation Solutions; Interpreting Inequality Solutions |
| 12 | 8 | One-Step Equations | 2 | 582 | 28 |  | Writing Addition Equations; Writing Multiplication Equations |
| 12 | 9 | One-Step Equations - Addition Multiplication | 2 | 950 | 36 |  | Solving Addition Equations; Solving Multiplication Equations |
| 12 | 10 | Writing Inequalities | 3 | 873 | 42 |  | Infinite Inequality Solutions; Writing Simple Inequalities; Recognizing Infinite Solutions |
| 12 | 11 | Number Line Solutions | 2 | 582 | 28 |  | Number Line Notation For Inequalities; Graphing Inequalities On Number Lines |
| 12 | 12 | Inequality Interpretation | 3 | 873 | 42 |  | Inequalities As Number Line Positions; Number Positions From Inequality Symbols; Farther Left Or Right |
| 12 | 13 | Relationship Equations | 2 | 766 | 32 |  | Equations For Variable Relationships; Variables For Changing Quantities |
| 12 | 14 | Relationship Equations - Dependent Independent | 1 | 291 | 14 |  | Dependent Variable Equations |
| 12 | 15 | Relationship Tables And Graphs | 2 | 950 | 36 |  | Analyzing Relationships With Tables; Analyzing Relationships With Graphs |
| 12 | 16 | Relationship Tables And Graphs - Dependent Independent | 1 | 291 | 14 |  | Connecting Tables Graphs And Equations |
| 12 | 17 | Constructing Relationship Models | 1 | 659 | 26 |  | Creating Tables Of Values |
| 12 | 18 | Constructing Relationship Models - Graphing Relationships | 1 | 659 | 26 |  | Creating Relationship Graphs |
| 13 | 2 | Coordinate Side Lengths | 3 | 873 | 42 |  | Horizontal Side Length; Vertical Side Length; Plotting Polygon Vertices |
| 13 | 3 | Coordinate Side Lengths - Geometry | 1 | 291 | 14 |  | Polygon Side Measurement |
| 13 | 4 | Coordinate Perimeter And Area | 2 | 582 | 28 |  | Coordinate Plane Perimeter; Coordinate Plane Area |
| 13 | 5 | Triangle Area Techniques | 2 | 582 | 28 |  | Right Triangle Area; General Triangle Area |
| 13 | 6 | Polygon Area Decomposition | 3 | 873 | 42 |  | Irregular Polygon Decomposition; Special Quadrilateral Area; Composite Polygon Area |
| 13 | 7 | Missing Rectangle Vertices | 2 | 950 | 36 |  | Missing Vertices Same X-Coordinate; Missing Vertices Same Y-Coordinate |
| 13 | 8 | Real-World Area Applications | 2 | 950 | 36 |  | Applying Area Composition; Coordinate Geometry Applications |
| 13 | 9 | Real-World Area Applications - Composite | 1 | 475 | 18 |  | Composite Shape Applications |
| 13 | 10 | Composing Complex Areas | 1 | 659 | 26 |  | Combining Polygon Areas |
| 14 | 2 | Prism Volume Foundations | 3 | 873 | 42 |  | Rectangular Prism Volume Formula; Base Area Times Height; Comparing Prism Volumes |
| 14 | 3 | Prism Volume Foundations (2) | 1 | 291 | 14 |  | Unit Cube Packing With Fractions |
| 14 | 4 | Surface Area Foundations | 2 | 582 | 28 |  | Surface Area From Nets; Net-Based Surface Area Calculation |
| 14 | 5 | Fractional Prism Volume | 2 | 950 | 36 |  | Cube Packing Versus Edge Multiplication; Fractional Edge Length Volume |
| 14 | 6 | Fractional Prism Volume (2) | 2 | 950 | 36 |  | Fractional Volume Using Base Area; Real-World Fractional Prism Problems |
| 14 | 7 | Nets And Surface Area Practice | 2 | 950 | 36 |  | Real-World Surface Area Problems; Constructing Nets From Shapes |
| 14 | 8 | Nets And Surface Area Practice (2) | 1 | 475 | 18 |  | Applied Net And Area Problems |
| 14 | 9 | Advanced Net Construction | 1 | 659 | 26 |  | Designing 3D Figure Nets |
| 15 | 2 | Recognizing Fallacies | 1 | 291 | 14 |  | Ad Hominem And Straw Man |
| 15 | 3 | Quantifiers And Arguments | 2 | 950 | 36 |  | Premises And Conclusions; Universal And Existential Quantifiers |
| 15 | 4 | Inference And Counterexamples | 2 | 950 | 36 |  | Modus Ponens And Tollens; Constructing Counterexamples |
| 15 | 5 | Argument Validity | 1 | 659 | 26 |  | Truth Tables For Validity |
| 16 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Permutation Formula; Combination Formula |
| 16 | 3 | Multiplicative Counting Methods | 2 | 950 | 36 |  | Multiplication Counting Principle; Arrangements With Repetition |
| 16 | 4 | Inclusion-Exclusion And Strategy | 2 | 950 | 36 |  | Inclusion-Exclusion Principle; Choosing Counting Techniques |
| 16 | 5 | Recursive Sequence Basics | 2 | 582 | 28 |  | Defining Recursive Sequences; Computing Recursive Terms |
| 16 | 6 | Fibonacci And Recursive Algorithms | 2 | 950 | 36 |  | Fibonacci Sequence Modeling; Recursive Factorial Algorithms |
| 16 | 7 | Convergence And Modeling | 2 | 950 | 36 |  | Sequence Convergence Analysis; Modeling Growth Recursively |
| 17 | 2 | Path And Tree Algorithms | 2 | 950 | 36 |  | Dijkstra's Shortest Path; Kruskal's Spanning Tree |
| 17 | 3 | Flow And Routing Problems | 2 | 950 | 36 |  | Maximum Flow Networks; Traveling Salesperson Solutions |
| 17 | 4 | Coloring And Network Reliability | 2 | 1134 | 44 |  | Graph Coloring Scheduling; Network Reliability Analysis |
| 17 | 5 | Voting Power Indices | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 17 | 6 | Voting Methods | 1 | 475 | 18 |  | Comparing Voting Methods |
| 17 | 7 | Apportionment Methods | 1 | 475 | 18 |  | Apportionment Method Comparison |
| 17 | 8 | Voting Fairness Criteria | 2 | 1134 | 44 |  | Arrow's Impossibility Theorem; Evaluating Voting Fairness Criteria |
| 18 | 2 | Adjusted Winner Method | 1 | 291 | 14 |  | Two-Party Issue Allocation |
| 18 | 3 | Fair Division Methods | 2 | 950 | 36 |  | Divider-Chooser Method; Lone-Divider Method |
| 18 | 4 | Fair Division Methods (2) | 2 | 950 | 36 |  | Last-Diminisher Method; Choosing A Division Algorithm |
| 18 | 5 | Fairness Criteria | 1 | 659 | 26 |  | Proportionality And Envy-Freeness |
| 19 | 2 | Number Encoding Methods | 2 | 766 | 32 |  | Binary Octal Hex Conversion; Check Digits And Parity Bits |
| 19 | 3 | Boolean Logic Systems | 2 | 1134 | 44 |  | Simplifying Boolean Expressions; Truth Table Construction |
| 19 | 4 | Applied Information Theory | 2 | 1134 | 44 |  | Data Compression Ratios; Time And Space Complexity |
| 19 | 5 | Applied Information Theory - Cryptography | 1 | 475 | 18 |  | Caesar Cipher Encryption |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 233 |
| fill ratio | 36% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=233 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 18 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 3 |
| prompt tokens | 140929 |
| completion tokens | 9356 |
| max single prompt | 49868 |
| tokens per LO | 500.9 |

| node | calls | prompt tokens |
| --- | --- | --- |
| plan_chapters | 1 | 49868 |
| titles | 2 | 91061 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | plan_chapters | P2 | claude-sonnet-5 | 49868 | 5737 | 63025 | 1 |
| 2 | titles | 3 | claude-sonnet-5 | 47193 | 3029 | 32129 | 1 |
| 3 | titles | 3 | claude-sonnet-5 | 43868 | 590 | 13644 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 300 |
| avg words per title | 3.64 |
| titles outside 2–5 words | 4 |
| titles with generic words | 1 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Ratios Rates And Percents' - 15 understand chapters OK
FINAL: Part 'Fraction And Whole Number Division' - 7 understand chapters OK
FINAL: Part 'Decimals Factors And Multiples' - 8 understand chapters OK
FINAL: Part 'Integers And Signed Numbers' - 8 understand chapters OK
FINAL: Part 'Absolute Value And Number Comparison' - 10 understand chapters OK
FINAL: Part 'The Cartesian Plane' - 10 understand chapters OK
FINAL: Part 'Statistical Questions And Center Measures' - 9 understand chapters OK
FINAL: Part 'Data Distribution And Summary' - 10 understand chapters OK
FINAL: Part 'Algebraic Terms And Evaluation' - 8 understand chapters OK
FINAL: Part 'Exponents And Equivalent Expressions' - 12 understand chapters OK
FINAL: Part 'Equations Inequalities And Relationships' - 17 understand chapters OK
FINAL: Part 'Coordinate Geometry And Area' - 9 understand chapters OK
FINAL: Part 'Volume And Surface Area' - 8 understand chapters OK
FINAL: Part 'Logical Reasoning And Argumentation' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics & Sequences Recursion' - 6 understand chapters OK
FINAL: Part 'Graph Theory & Voting Apportionment' - 7 understand chapters OK
FINAL: Part 'Equitable Resource Allocation' - 4 understand chapters OK
FINAL: Part 'Number Systems And Information Theory' - 4 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
