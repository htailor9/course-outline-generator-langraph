# Run analysis — 20260905-144110_300LOs_Synthetic300-Chrono_claude_cli

Generated 2026-09-05T14:41:10 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 549.1s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Synthetic300_Chrono |
| grade_band | MS |
| subject_area | Mathematics |
| progression | CHRONOLOGICAL_PROGRESSION |
| learning objectives | 300 |
| calendar | 5/wk × 128 wk = 640 lesson days |
| minutes_per_lesson | 45 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **130** (top: Absolute Value ×10, Fraction Division ×9, Measures Of Center ×9, Coordinate Distance ×8, Data Distribution ×8, Opposite Numbers ×7, Statistical Questions ×7, Inequality Solutions ×7, Signed Numbers ×6, Coordinate Reflections ×6)

## 3. Output structure

- Parts: **20** (1 overview + 17 content + 2 semester) · Chapters: **228** · Modules: 355 · LO modules: 300
- Content estimate: 115084 words · 8197 minutes across understand chapters
- Min-4 merges applied: 1

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic300_Chrono Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Decimal And Whole Number Operations | 10 | 6 | 15 | 12 | 3860 | 356 |
| 3 | understand | Factors And Fraction Division | 12 | 8 | 19 | 16 | 6312 | 440 |
| 4 | understand | Ratio And Rate Reasoning | 11 | 7 | 17 | 14 | 5178 | 400 |
| 5 | understand | Proportional Relationships And Percents | 15 | 11 | 20 | 17 | 6787 | 462 |
| 6 | understand | Integers And The Number Line | 13 | 9 | 23 | 20 | 6924 | 484 |
| 7 | understand | Comparing And Ordering Rational Numbers | 14 | 10 | 28 | 25 | 8379 | 554 |
| 8 | understand | Coordinate Plane And Transformations | 14 | 10 | 25 | 22 | 7322 | 508 |
| 9 | understand | Introduction To Variables And Expressions | 11 | 7 | 17 | 14 | 4810 | 400 |
| 10 | understand | Properties Of Operations And Exponents | 21 | 17 | 26 | 23 | 12397 | 678 |
| 11 | understand | One-Step Equations And Inequalities | 13 | 9 | 23 | 20 | 7108 | 488 |
| 12 | understand | Dependent Independent & Perimeter, Area, | 14 | 10 | 21 | 18 | 7262 | 484 |
| 13 | understand | Coordinate Geometry And Volume Applications | 13 | 9 | 19 | 16 | 6128 | 436 |
| 14 | understand | Statistics Fundamentals | 12 | 8 | 25 | 22 | 6402 | 488 |
| 15 | understand | Data Analysis And Displays | 12 | 8 | 21 | 18 | 6342 | 468 |
| 16 | understand | Logic And Combinatorics | 12 | 8 | 15 | 12 | 5332 | 392 |
| 17 | understand | Recursion, Graphs, And Algorithms | 16 | 12 | 22 | 19 | 9025 | 534 |
| 18 | understand | Voting And Fair Division | 10 | 6 | 15 | 12 | 5516 | 400 |
| 19 | semester | Synthetic300_Chrono Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 20 | semester | Synthetic300_Chrono Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Whole Number Division | 2 | 582 | 28 |  | Long Division Algorithm; Multi-Digit Whole Number Quotients |
| 2 | 3 | Decimal Addition And Subtraction | 3 | 873 | 42 |  | Adding Multi-Digit Decimals; Subtracting Multi-Digit Decimals; Decimal Place Value Addition |
| 2 | 4 | Decimal Addition And Subtraction (2) | 1 | 291 | 14 |  | Decimal Regrouping Subtraction |
| 2 | 5 | Decimal Multiplication | 2 | 582 | 28 |  | Multiplying Multi-Digit Decimals; Decimal Product Place Value |
| 2 | 6 | Decimal Division | 2 | 582 | 28 |  | Dividing Multi-Digit Decimals; Decimal Quotient Placement |
| 2 | 7 | Whole Number Division Applications | 2 | 950 | 36 |  | Whole Number Division Word Problems; Real-World Whole Number Division |
| 3 | 2 | Common Factor Identification | 2 | 582 | 28 |  | Sum GCF Identification; Shared Factor Detection |
| 3 | 3 | Common Factor Extraction | 2 | 766 | 32 |  | Factoring Out Common Factor; Distributive Property Factoring |
| 3 | 4 | Common Factor Extraction - Gcf Factoring | 1 | 291 | 14 |  | Factored Sum Expression |
| 3 | 5 | Prime Factorization | 2 | 950 | 36 |  | Prime Factorization Method; Factor Tree Method |
| 3 | 6 | Fraction Division Fundamentals | 3 | 873 | 42 |  | Meaning Of Fraction Quotients; Fraction Division Algorithm; Fraction Division Equations |
| 3 | 7 | Modeling Fraction Division | 2 | 950 | 36 |  | Fraction Division Word Problems; Visual Fraction Division Models |
| 3 | 8 | Fraction Division Applications | 2 | 950 | 36 |  | Recognizing Fraction Division Situations; Applying Fraction Division Algorithms |
| 3 | 9 | Fraction Division Applications (2) | 2 | 950 | 36 |  | Identifying Fraction Division Problems; Solving Fraction Division Problems |
| 4 | 2 | Ratio Notation And Language | 3 | 873 | 42 |  | Ratio Notation Forms; Describing Ratio Relationships; Writing Ratios Three Ways |
| 4 | 3 | Ratio Notation And Language (2) | 1 | 291 | 14 |  | Ratio Relationship Descriptions |
| 4 | 4 | Unit Rate Calculations | 3 | 873 | 42 |  | Calculating Unit Rates; Unit Rates With Units; Finding Unit Rates |
| 4 | 5 | Unit Rate Calculations (2) | 1 | 291 | 14 |  | Expressing Unit Rates |
| 4 | 6 | Equivalent Ratio Problems | 2 | 950 | 36 |  | Equivalent Ratio Tables; Modeling Equivalent Ratios |
| 4 | 7 | Percent And Measurement Applications | 2 | 950 | 36 |  | Percent Problems With Ratios; Measurement Conversion Ratios |
| 4 | 8 | Percent And Measurement Applications - Problems Unit | 2 | 950 | 36 |  | Solving Percent Problems; Converting Units With Ratios |
| 5 | 2 | Understanding Ratios | 2 | 766 | 32 |  | Defining Ratios; Describing Ratios With Words |
| 5 | 3 | Understanding Ratios (2) | 1 | 291 | 14 |  | Ratio Notation |
| 5 | 4 | Unit Rate Concepts | 2 | 582 | 28 |  | Defining Unit Rates; Calculating Unit Rates |
| 5 | 5 | Unit Rate Concepts - Rates | 1 | 475 | 18 |  | Rate Language In Context |
| 5 | 6 | Equivalent Ratio Tables | 2 | 950 | 40 |  | Building Ratio Tables; Finding Missing Ratio Values |
| 5 | 7 | Equivalent Ratio Tables - Comparison | 1 | 291 | 14 |  | Comparing Ratios With Tables |
| 5 | 8 | Graphing Ratios And Rates | 2 | 950 | 36 |  | Plotting Ratio Pairs; Unit Pricing Problems |
| 5 | 9 | Graphing Ratios And Rates - Unit Rate | 1 | 475 | 18 |  | Constant Speed Problems |
| 5 | 10 | Percent Reasoning | 2 | 766 | 32 |  | Finding Percent Of A Quantity; Finding The Whole Amount |
| 5 | 11 | Unit Conversion Strategies | 2 | 766 | 32 |  | Converting Measurement Units; Unit Conversion In Multiplication |
| 5 | 12 | Unit Conversion Strategies (2) | 1 | 475 | 18 |  | Unit Conversion In Division |
| 6 | 2 | Number Line Placement | 3 | 873 | 42 |  | Horizontal Number Line Placement; Vertical Number Line Placement; Opposite Signs And Zero |
| 6 | 3 | Opposite Number Pairs | 3 | 873 | 42 |  | Identifying Opposite Numbers; Equal Distance From Zero; Opposite Number Identification |
| 6 | 4 | Opposite Number Pairs - Numbers | 1 | 291 | 14 |  | Distance From Zero Explained |
| 6 | 5 | Opposite Number Properties | 2 | 582 | 28 |  | Double Opposite Property; Zero As Its Own Opposite |
| 6 | 6 | Zero And Signed Values | 3 | 873 | 42 |  | Zero In Real-World Contexts; Rational Numbers In Real Contexts; Opposite Directions With Signed Numbers |
| 6 | 7 | Representing Rational Quantities | 2 | 582 | 28 |  | Representing Real-World Quantities; Positive And Negative Representations |
| 6 | 8 | Signed Numbers In Context | 2 | 950 | 36 |  | Elevation And Sea Level Values; Gains And Losses Representation |
| 6 | 9 | Signed Numbers In Context (2) | 2 | 950 | 36 |  | Positive Quantities In Context; Negative Quantities In Context |
| 6 | 10 | Applying Rational Numbers | 2 | 950 | 36 |  | Temperature Elevation And Balances; Rational Numbers For Real Situations |
| 7 | 2 | Number Line Inequalities | 3 | 873 | 42 |  | Inequality Position Meaning; Position From Inequality Symbols; Locating Greater And Lesser Values |
| 7 | 3 | Absolute Value Basics | 3 | 873 | 42 |  | Absolute Value As Distance; Distance From Zero Concept; Defining Absolute Value |
| 7 | 4 | Calculating Absolute Value | 3 | 873 | 42 |  | Calculating Signed Absolute Values; Absolute Value Computation; Absolute Value Of Rationals |
| 7 | 5 | Comparing Absolute Values | 3 | 873 | 42 |  | Comparing Distance From Zero; Greater Absolute Value Comparison; Absolute Value Versus Order |
| 7 | 6 | Absolute Value In Context | 2 | 582 | 28 |  | Magnitude Of Positive Quantities; Magnitude Of Negative Quantities |
| 7 | 7 | Comparing Rational Numbers | 2 | 582 | 28 |  | Comparing Rationals With Symbols; Rational Inequality Comparison |
| 7 | 8 | Rational Number Order Statements | 3 | 873 | 42 |  | Writing Rational Order Statements; Interpreting Rational Order Statements; Explaining Rational Order Relationships |
| 7 | 9 | Applying Absolute Value | 2 | 950 | 36 |  | Absolute Value In Real Contexts; Real-World Absolute Value Problems |
| 7 | 10 | Ordering Rational Numbers | 2 | 950 | 36 |  | Ordering Rationals Least To Greatest; Sequencing Rational Number Sets |
| 7 | 11 | Real-World Rational Comparisons | 2 | 950 | 36 |  | Real-World Rational Number Problems; Applying Rational Comparisons Practically |
| 8 | 2 | Quadrant Identification | 3 | 873 | 42 |  | Identifying Quadrants by Sign; Quadrant Sign Patterns; Locating Points by Quadrant |
| 8 | 3 | Quadrant Identification - Coordinate Plane | 1 | 291 | 14 |  | Explaining Quadrant Signs |
| 8 | 4 | Plotting Ordered Pairs | 2 | 950 | 36 |  | Graphing Four-Quadrant Points; Plotting Points on Axes |
| 8 | 5 | Plotting Ordered Pairs - Coordinate Plane | 2 | 766 | 32 |  | Graphing Real-World Coordinates; Plotting Integer and Rational Pairs |
| 8 | 6 | Axis Reflections | 3 | 873 | 42 |  | Reflecting Points Across X-Axis; Reflecting Points Across Y-Axis; Y-Axis Reflection Pairs |
| 8 | 7 | Reflection Relationships | 3 | 873 | 42 |  | X-Axis Reflection Pairs; Sign-Change Coordinate Pairs; Describing Axis Reflections |
| 8 | 8 | Horizontal Vertical Distance | 3 | 873 | 42 |  | Distance on Shared Coordinates; Same-Coordinate Point Distance; Horizontal Side Length |
| 8 | 9 | Horizontal Vertical Distance - Coordinate | 1 | 291 | 14 |  | Vertical Side Length |
| 8 | 10 | Distance Absolute Value | 2 | 582 | 28 |  | Vertical Distance with Absolute Value; Horizontal Distance with Absolute Value |
| 8 | 11 | Real World Applications | 2 | 950 | 36 |  | Mapping Real-World Distances; Coordinate Distance Word Problems |
| 9 | 2 | Expression Vocabulary Basics | 3 | 873 | 42 |  | Identifying Expression Terms; Identifying Coefficients; Identifying Factors |
| 9 | 3 | Expression Vocabulary Basics - Algebraic | 1 | 291 | 14 |  | Sums Products And Quotients |
| 9 | 4 | Expression Term Grouping | 2 | 582 | 28 |  | Naming Expression Parts; Treating Groups As Units |
| 9 | 5 | Variables In Context | 2 | 582 | 28 |  | Interpreting Variables As Unknowns; Variable Value Constraints |
| 9 | 6 | Writing Algebraic Expressions | 3 | 873 | 42 |  | Translating Verbal Statements; Modeling Real-World Relationships; Expressing Operations With Variables |
| 9 | 7 | Independent Dependent Relationships | 1 | 659 | 26 |  | Tables Of Variable Relationships |
| 9 | 8 | Independent Dependent Relationships - Variable | 2 | 950 | 40 |  | Graphing Variable Relationships; Equations For Variable Relationships |
| 10 | 2 | Exponent Notation Basics | 3 | 873 | 42 |  | Writing Exponent Expressions; Comparing Exponent Values; Writing Numerical Exponents |
| 10 | 3 | Substitution And Equivalence | 2 | 582 | 28 |  | Testing Expression Equivalence; Substituting Variable Values |
| 10 | 4 | Core Operation Properties | 2 | 950 | 36 |  | Commutative Property Application; Associative Property Application |
| 10 | 5 | Core Operation Properties - Distributive Property | 1 | 475 | 18 |  | Distributive Property Application |
| 10 | 6 | Distributive Property Applications | 2 | 1134 | 44 |  | Factoring Out GCF; Distributive Property Expressions |
| 10 | 7 | Equivalent Expression Reasoning | 2 | 1134 | 44 |  | Determining Expression Equivalence; Justifying Equivalence Reasoning |
| 10 | 8 | Commutative And Associative Practice | 1 | 659 | 26 |  | Commutative Property Expressions |
| 10 | 9 | Commutative And Associative Practice - Properties Operations | 1 | 659 | 26 |  | Associative Property Expressions |
| 10 | 10 | Inverse And Identity Properties | 1 | 659 | 26 |  | Inverse Property Application |
| 10 | 11 | Inverse And Identity Properties - Operations | 1 | 659 | 26 |  | Identity Property Application |
| 10 | 12 | Exponent Evaluation Skills | 1 | 659 | 26 |  | Evaluating Exponent Expressions |
| 10 | 13 | Exponent Evaluation Skills - Exponents | 1 | 659 | 26 |  | Evaluating Numerical Exponents |
| 10 | 14 | Absolute Value In Expressions | 1 | 659 | 26 |  | Evaluating Absolute Value Expressions |
| 10 | 15 | Absolute Value In Expressions - Order Operations | 1 | 659 | 26 |  | Absolute Value With Exponents |
| 10 | 16 | Order Of Operations Mastery | 1 | 659 | 26 |  | Applying Order Of Operations |
| 10 | 17 | Order Of Operations Mastery (2) | 1 | 659 | 26 |  | Order Of Operations Without Parentheses |
| 10 | 18 | Order Of Operations Mastery - Formula Evaluation | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 11 | 2 | Understanding Variables | 3 | 873 | 42 |  | Writing Algebraic Expressions; Variables As Unknowns; Variable Value Sets |
| 11 | 3 | Writing Equations And Inequalities | 3 | 873 | 42 |  | Writing Addition Equations; Writing Multiplication Equations; Writing Simple Inequalities |
| 11 | 4 | Meaning Of Solutions | 3 | 873 | 42 |  | Interpreting Equation Solutions; Interpreting Inequality Solutions; Meaning Of Solving |
| 11 | 5 | Inequality Solution Sets | 3 | 873 | 42 |  | Graphing Inequality Solutions; Infinite Solution Sets; Infinite Inequality Solutions |
| 11 | 6 | Inequality Solution Sets - Solutions | 1 | 291 | 14 |  | Number Line Diagrams |
| 11 | 7 | Solving One-Step Equations | 2 | 950 | 36 |  | Solving Addition Equations; Solving Multiplication Equations |
| 11 | 8 | Solving One-Step Equations - Variables | 1 | 475 | 18 |  | Modeling With Variables |
| 11 | 9 | Verifying Solutions By Substitution | 2 | 950 | 36 |  | Checking Equation Solutions; Checking Inequality Solutions |
| 11 | 10 | Verifying Solutions By Substitution - Equation Inequality | 2 | 950 | 36 |  | Substitution In Equations; Substitution In Inequalities |
| 12 | 2 | Variables And Equations | 2 | 766 | 32 |  | Representing Related Quantities With Variables; Writing Dependent Variable Equations |
| 12 | 3 | Tables Graphs And Equations | 2 | 950 | 36 |  | Analyzing Variable Relationships In Tables; Analyzing Variable Relationships In Graphs |
| 12 | 4 | Tables Graphs And Equations - Dependent Independent | 1 | 291 | 14 |  | Connecting Graphs Tables And Equations |
| 12 | 5 | Coordinate Polygon Measures | 2 | 582 | 28 |  | Perimeter Of Coordinate Polygons; Area Of Coordinate Polygons |
| 12 | 6 | Rectangular Prism Volume | 3 | 873 | 42 |  | Prism Volume Using Length Width Height; Prism Volume Using Base Area; Comparing Rectangular Prism Volumes |
| 12 | 7 | Rectangle Vertex Coordinates | 2 | 950 | 36 |  | Missing Vertices With Equal X-Coordinates; Missing Vertices With Equal Y-Coordinates |
| 12 | 8 | Area Decomposition Strategies | 2 | 950 | 40 |  | Decomposing Irregular Polygons For Area; Composing Shapes To Find Area |
| 12 | 9 | Area Decomposition Strategies - Problem Solving | 1 | 475 | 18 |  | Solving Real-World Area Problems |
| 12 | 10 | Nets And Surface Area | 2 | 950 | 40 |  | Creating Nets For Solid Figures; Calculating Surface Area From Nets |
| 12 | 11 | Nets And Surface Area - Application | 1 | 475 | 18 |  | Applying Surface Area To Real Problems |
| 13 | 2 | Coordinate Geometry Essentials | 2 | 582 | 28 |  | Plotting Polygon Vertices; Horizontal And Vertical Side Lengths |
| 13 | 3 | Coordinate Geometry Essentials (2) | 1 | 475 | 18 |  | Coordinate Geometry Word Problems |
| 13 | 4 | Triangle And Quadrilateral Area | 3 | 873 | 42 |  | Area Of Right Triangles; Area Of General Triangles; Area Of Special Quadrilaterals |
| 13 | 5 | Composite Polygon Area | 2 | 766 | 32 |  | Decomposing Polygons For Area; Composite Area Word Problems |
| 13 | 6 | Volume By Unit Cubes | 2 | 766 | 32 |  | Volume Via Unit Cube Packing; Unit Cubes And Edge Length Volume |
| 13 | 7 | Prism Volume Formulas | 2 | 950 | 36 |  | Volume Formula Length Width Height; Volume Formula Base Times Height |
| 13 | 8 | Prism Volume Formulas - Prisms | 1 | 475 | 18 |  | Prism Volume Word Problems |
| 13 | 9 | Nets And Surface Area | 2 | 766 | 32 |  | Constructing Three-Dimensional Nets; Surface Area From Nets |
| 13 | 10 | Nets And Surface Area (2) | 1 | 475 | 18 |  | Surface Area Word Problems |
| 14 | 2 | Statistical Questions Basics | 3 | 873 | 42 |  | Statistical Question Examples; Statistical Question Non-Examples; Justifying Statistical Questions |
| 14 | 3 | Measures Of Center | 3 | 873 | 42 |  | Mean Median Mode Calculation; Choosing Best Measure Of Center; Interpreting Center Values |
| 14 | 4 | Variability And Distribution | 3 | 873 | 42 |  | Interpreting Range And IQR; Describing Center And Spread; Symmetric And Skewed Shapes |
| 14 | 5 | Graph Features And Context | 2 | 582 | 28 |  | Unusual Graph Features; Data Set Context Description |
| 14 | 6 | Center Measures Practice | 3 | 873 | 42 |  | Center Values Calculation; Best Measure Selection; Center Value Interpretation |
| 14 | 7 | Spread And Shape Analysis | 3 | 873 | 42 |  | Range And IQR Interpretation; Center And Spread Description; Distribution Shape Identification |
| 14 | 8 | Data Patterns And Meaning | 2 | 582 | 28 |  | Identifying Graph Anomalies; Context From Data Patterns |
| 14 | 9 | Statistical Question Practice | 3 | 873 | 42 |  | Examples Of Statistical Questions; Non-Statistical Question Examples; Explaining Statistical Question Validity |
| 15 | 2 | Statistical Questions And Attributes | 3 | 873 | 42 |  | Identifying Statistical Questions; Data Sets As Distributions; Describing Data Attributes |
| 15 | 3 | Distribution Characteristics | 3 | 873 | 42 |  | Center Of A Distribution; Spread Of A Distribution; Shape Of A Distribution |
| 15 | 4 | Measures Of Center | 3 | 873 | 42 |  | Summarizing Data With Center; Calculating Median And Mean; Choosing Measures Of Center |
| 15 | 5 | Measures Of Variability | 3 | 873 | 42 |  | Summarizing Data Variation; Calculating IQR And MAD; Choosing Measures Of Variability |
| 15 | 6 | Interpreting Data Patterns | 3 | 873 | 42 |  | Describing Overall Data Patterns; Identifying Data Deviations; Reporting Number Of Observations |
| 15 | 7 | Numerical Data Displays | 1 | 659 | 26 |  | Creating Dot Plots |
| 15 | 8 | Numerical Data Displays (2) | 1 | 659 | 26 |  | Creating Histograms |
| 15 | 9 | Numerical Data Displays (3) | 1 | 659 | 26 |  | Creating Box Plots |
| 16 | 2 | Argument Construction And Inference | 2 | 950 | 36 |  | Constructing Valid Arguments; Modus Ponens And Tollens |
| 16 | 3 | Argument Construction And Inference - Logical Fallacies | 1 | 291 | 14 |  | Spotting Logical Fallacies |
| 16 | 4 | Quantifiers And Validity | 2 | 1134 | 44 |  | Truth Tables And Validity; Universal And Existential Quantifiers |
| 16 | 5 | Quantifiers And Validity - Counterexamples | 1 | 475 | 18 |  | Disproving With Counterexamples |
| 16 | 6 | Counting Principles And Arrangements | 2 | 766 | 32 |  | Multiplication Counting Principle; Permutations Of Ordered Arrangements |
| 16 | 7 | Counting Principles And Arrangements - Combinations | 1 | 291 | 14 |  | Combinations Without Order |
| 16 | 8 | Advanced Counting Techniques | 2 | 950 | 36 |  | Arrangements With Repetition; Inclusion-Exclusion Principle |
| 16 | 9 | Advanced Counting Techniques - Technique Selection | 1 | 475 | 18 |  | Choosing Counting Techniques |
| 17 | 2 | Recursive Sequences Basics | 2 | 582 | 28 |  | Recursive Sequence Definitions; Arithmetic And Geometric Terms |
| 17 | 3 | Number Base Systems | 1 | 291 | 14 |  | Converting Between Number Bases |
| 17 | 4 | Recursive Applications And Modeling | 2 | 950 | 36 |  | Fibonacci Sequence Modeling; Factorial And Combinatorial Algorithms |
| 17 | 5 | Recursive Applications And Modeling - Sequence Convergence | 2 | 950 | 36 |  | Sequence Convergence Analysis; Population And Investment Growth Models |
| 17 | 6 | Graph Optimization Algorithms | 2 | 950 | 36 |  | Dijkstra's Shortest Path; Kruskal's Minimum Spanning Tree |
| 17 | 7 | Graph Optimization Algorithms - Network Flow | 1 | 475 | 18 |  | Maximum Flow Networks |
| 17 | 8 | Combinatorial Graph Problems | 2 | 950 | 36 |  | Traveling Salesperson Algorithms; Graph Coloring Scheduling |
| 17 | 9 | Information Encoding Techniques | 2 | 950 | 36 |  | Boolean Algebra Simplification; Error Detection Codes |
| 17 | 10 | Information Encoding Techniques - Data Compression | 2 | 950 | 36 |  | Data Compression Ratios; Caesar Cipher Encryption |
| 17 | 11 | Network Reliability Analysis | 1 | 659 | 26 |  | Network Connectivity And Critical Paths |
| 17 | 12 | Advanced Logic And Efficiency | 1 | 659 | 26 |  | Truth Table Construction |
| 17 | 13 | Advanced Logic And Efficiency - Algorithmic | 1 | 659 | 26 |  | Time And Space Complexity |
| 18 | 2 | Weighted Voting Power | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 18 | 3 | Voting Methods And Fairness | 2 | 950 | 36 |  | Arrow's Impossibility Theorem; Plurality Borda And Runoff Methods |
| 18 | 4 | Voting Methods And Fairness - Apportionment System | 2 | 1134 | 44 |  | Hamilton Jefferson Webster Methods; Voting Fairness Criteria |
| 18 | 5 | Two-Party Fair Division | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 18 | 6 | Multi-Party Fair Division | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 18 | 7 | Evaluating Fair Division | 2 | 1134 | 44 |  | Choosing Fair Division Algorithms; Proportionality And Envy-Freeness |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 228 |
| fill ratio | 36% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=228 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 17 content parts; all parts >= 4 understand chapters: True.
- Merges applied: 1 (see enforcement_log).

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 47 |
| prompt tokens | 1947197 |
| completion tokens | 164913 |
| max single prompt | 75330 |
| tokens per LO | 7040.4 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 220453 |
| plan_chapters | 18 | 847050 |
| plan_parts | 1 | 71692 |
| titles | 18 | 808002 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 22525 | 1052 | 17554 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 22424 | 2135 | 24867 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 22512 | 2739 | 30677 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 22533 | 2705 | 29973 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 22405 | 3603 | 38280 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 21186 | 4909 | 45079 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 21175 | 2903 | 27584 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 22386 | 2363 | 27690 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 22218 | 2643 | 26925 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 21089 | 1082 | 13876 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 71692 | 19508 | 161543 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 46386 | 2221 | 30703 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 75330 | 4951 | 55234 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 47575 | 3191 | 37762 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 48472 | 4268 | 50026 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 49617 | 5085 | 54304 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 21704 | 6174 | 60204 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 47320 | 2971 | 28720 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 46671 | 3230 | 37295 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 50611 | 6475 | 64618 | 1 |
| 21 | plan_chapters | P10 | claude-sonnet-5 | 22702 | 7162 | 70948 | 1 |
| 22 | plan_chapters | P11 | claude-sonnet-5 | 44800 | 1703 | 25781 | 1 |
| 23 | plan_chapters | P12 | claude-sonnet-5 | 49450 | 5981 | 64332 | 1 |
| 24 | plan_chapters | P13 | claude-sonnet-5 | 46659 | 2845 | 31032 | 1 |
| 25 | plan_chapters | P14 | claude-sonnet-5 | 48294 | 3958 | 41436 | 1 |
| 26 | plan_chapters | P15 | claude-sonnet-5 | 47695 | 4052 | 40486 | 1 |
| 27 | plan_chapters | P16 | claude-sonnet-5 | 50749 | 6358 | 69218 | 1 |
| 28 | plan_chapters | P17 | claude-sonnet-5 | 50809 | 6115 | 63928 | 1 |
| 29 | plan_chapters | P18 | claude-sonnet-5 | 52206 | 8644 | 91397 | 1 |
| 30 | titles | 2 | claude-sonnet-5 | 45814 | 1695 | 25478 | 1 |
| 31 | titles | 3 | claude-sonnet-5 | 46071 | 1563 | 21354 | 1 |
| 32 | titles | 4 | claude-sonnet-5 | 46396 | 1987 | 27047 | 1 |
| 33 | titles | 5 | claude-sonnet-5 | 46197 | 1777 | 24597 | 1 |
| 34 | titles | 6 | claude-sonnet-5 | 46680 | 1902 | 30328 | 1 |
| 35 | titles | 7 | claude-sonnet-5 | 47760 | 2627 | 28745 | 1 |
| 36 | titles | 8 | claude-sonnet-5 | 47583 | 3281 | 35116 | 1 |
| 37 | titles | 9 | claude-sonnet-5 | 45767 | 2139 | 26621 | 1 |
| 38 | titles | 10 | claude-sonnet-5 | 46911 | 2548 | 29044 | 1 |
| 39 | titles | 10 | claude-sonnet-5 | 43125 | 384 | 14092 | 1 |
| 40 | titles | 11 | claude-sonnet-5 | 46328 | 2202 | 23275 | 1 |
| 41 | titles | 12 | claude-sonnet-5 | 45772 | 1926 | 23390 | 1 |
| 42 | titles | 13 | claude-sonnet-5 | 45658 | 1693 | 21962 | 1 |
| 43 | titles | 14 | claude-sonnet-5 | 47011 | 1857 | 22856 | 1 |
| 44 | titles | 15 | claude-sonnet-5 | 46305 | 1787 | 20451 | 1 |
| 45 | titles | 16 | claude-sonnet-5 | 22374 | 807 | 12947 | 1 |
| 46 | titles | 17 | claude-sonnet-5 | 47314 | 2339 | 26203 | 1 |
| 47 | titles | 18 | claude-sonnet-5 | 44936 | 1373 | 22124 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 299 |
| avg words per title | 3.6 |
| titles outside 2–5 words | 3 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
MERGE: Part 'Dependent And Independent Variables' (3 chapters) merged with 'Perimeter, Area, And Volume Basics' (7 chapters)
RESULT: Part 'Dependent Independent & Perimeter, Area,' now has 10 chapters
FINAL: Part 'Decimal And Whole Number Operations' - 6 understand chapters OK
FINAL: Part 'Factors And Fraction Division' - 8 understand chapters OK
FINAL: Part 'Ratio And Rate Reasoning' - 7 understand chapters OK
FINAL: Part 'Proportional Relationships And Percents' - 11 understand chapters OK
FINAL: Part 'Integers And The Number Line' - 9 understand chapters OK
FINAL: Part 'Comparing And Ordering Rational Numbers' - 10 understand chapters OK
FINAL: Part 'Coordinate Plane And Transformations' - 10 understand chapters OK
FINAL: Part 'Introduction To Variables And Expressions' - 7 understand chapters OK
FINAL: Part 'Properties Of Operations And Exponents' - 17 understand chapters OK
FINAL: Part 'One-Step Equations And Inequalities' - 9 understand chapters OK
FINAL: Part 'Dependent Independent & Perimeter, Area,' - 10 understand chapters OK
FINAL: Part 'Coordinate Geometry And Volume Applications' - 9 understand chapters OK
FINAL: Part 'Statistics Fundamentals' - 8 understand chapters OK
FINAL: Part 'Data Analysis And Displays' - 8 understand chapters OK
FINAL: Part 'Logic And Combinatorics' - 8 understand chapters OK
FINAL: Part 'Recursion, Graphs, And Algorithms' - 12 understand chapters OK
FINAL: Part 'Voting And Fair Division' - 6 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
