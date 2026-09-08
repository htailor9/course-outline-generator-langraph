# Run analysis — 20260905-143156_300LOs_Synthetic300-Theme_claude_cli

Generated 2026-09-05T14:31:56 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 515.3s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Synthetic300_Theme |
| grade_band | MS |
| subject_area | Mathematics |
| progression | THEME_BASED_PROGRESSION |
| learning objectives | 300 |
| calendar | 5/wk × 128 wk = 640 lesson days |
| minutes_per_lesson | 45 |
| chapter word limit | 2000 |
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **160** (top: Absolute Value ×10, Measures Of Center ×9, Decimal Operations ×8, Statistical Questions ×7, Fraction Division ×7, Equivalent Expressions ×7, Data Distribution ×6, Unit Rates ×5, Greatest Common Factor ×5, Dependent And Independent Variables ×5)

## 3. Output structure

- Parts: **13** (1 overview + 10 content + 2 semester) · Chapters: **203** · Modules: 334 · LO modules: 300
- Content estimate: 115084 words · 6937 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic300_Theme Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Ratios, Rates, and Proportions | 21 | 17 | 34 | 31 | 11965 | 682 |
| 3 | understand | Fraction, Decimal, and Factor Operations | 18 | 14 | 32 | 29 | 10647 | 634 |
| 4 | understand | Statistical Questions and Data Analysis | 23 | 19 | 43 | 40 | 12744 | 776 |
| 5 | understand | Rational Numbers and Absolute Value | 23 | 19 | 48 | 45 | 15303 | 858 |
| 6 | understand | Graphing on the Coordinate Plane | 14 | 10 | 23 | 20 | 6740 | 480 |
| 7 | understand | Algebraic Expressions and Properties | 27 | 23 | 39 | 36 | 15996 | 856 |
| 8 | understand | Equations, Inequalities, and Variables | 20 | 16 | 28 | 25 | 9851 | 594 |
| 9 | understand | Geometric Measurement and Surface Area | 20 | 16 | 34 | 31 | 11965 | 686 |
| 10 | understand | Logic, Proof, and Combinatorics | 15 | 11 | 21 | 18 | 7814 | 492 |
| 11 | understand | Networks, Social Choice, and Computation | 17 | 13 | 28 | 25 | 12059 | 654 |
| 12 | semester | Synthetic300_Theme Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 13 | semester | Synthetic300_Theme Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Understanding Ratios | 3 | 873 | 42 |  | Ratio Notation Forms; Writing Ratios Three Ways; Defining Ratios |
| 2 | 3 | Understanding Ratios (2) | 1 | 291 | 14 |  | Ratio Notation and Terminology |
| 2 | 4 | Ratio Language and Comparison | 2 | 582 | 28 |  | Describing Ratio Relationships; Comparing Quantities with Ratios |
| 2 | 5 | Ratio Language and Comparison - Ratios | 1 | 475 | 18 |  | Ratios in Word Form |
| 2 | 6 | Defining Unit Rates | 3 | 873 | 42 |  | Calculating Unit Rates; Finding Unit Rates from Ratios; Defining Unit Rate |
| 2 | 7 | Defining Unit Rates (2) | 1 | 291 | 14 |  | Unit Rates with Nonzero Terms |
| 2 | 8 | Describing Unit Rates | 2 | 582 | 28 |  | Unit Rates with Units; Expressing Rates with Units |
| 2 | 9 | Describing Unit Rates (2) | 1 | 475 | 18 |  | Rate Language in Context |
| 2 | 10 | Ratio Tables and Equivalence | 2 | 950 | 36 |  | Equivalent Ratio Strategies; Modeling Equivalent Ratios |
| 2 | 11 | Ratio Tables and Equivalence (2) | 2 | 582 | 28 |  | Missing Values in Ratio Tables; Comparing Ratios with Tables |
| 2 | 12 | Percent Problems | 2 | 950 | 36 |  | Percent Problems with Ratio Models; Rate Reasoning for Percents |
| 2 | 13 | Percent Problems - Percents | 2 | 766 | 32 |  | Percent as Rate per Hundred; Finding the Whole from a Percent |
| 2 | 14 | Unit Rate Applications | 2 | 950 | 36 |  | Unit Pricing Problems; Constant Speed Problems |
| 2 | 15 | Measurement Conversion | 2 | 950 | 36 |  | Converting Measurements with Ratios; Rate Reasoning for Conversions |
| 2 | 16 | Measurement Conversion - Unit | 1 | 291 | 14 |  | Ratio-Based Unit Conversion |
| 2 | 17 | Unit Conversion Operations | 2 | 950 | 36 |  | Units in Multiplication; Units in Division |
| 2 | 18 | Graphing Ratio Tables | 2 | 1134 | 44 |  | Building Ratio Tables; Plotting Ratio Pairs |
| 3 | 2 | Adding and Subtracting Decimals | 3 | 873 | 42 |  | Adding Multi-Digit Decimals; Subtracting Multi-Digit Decimals; Standard Decimal Addition |
| 3 | 3 | Adding and Subtracting Decimals - Decimal Operations | 1 | 291 | 14 |  | Decimal Subtraction Algorithm |
| 3 | 4 | Multiplying and Dividing Decimals | 3 | 873 | 42 |  | Multiplying Multi-Digit Decimals; Dividing Multi-Digit Decimals; Standard Decimal Multiplication |
| 3 | 5 | Multiplying and Dividing Decimals - Decimal Operations | 1 | 291 | 14 |  | Decimal Division Algorithm |
| 3 | 6 | Whole Number Division | 2 | 766 | 32 |  | Multi-Digit Division Fluency; Real-World Division Problems |
| 3 | 7 | Whole Number Division (2) | 2 | 766 | 32 |  | Standard Division Algorithm; Applying Division To Word Problems |
| 3 | 8 | Greatest Common Factor | 3 | 873 | 42 |  | Identifying Common Factors In Sums; Factoring Out The GCF; Shared Factors Of Addends |
| 3 | 9 | Greatest Common Factor (2) | 1 | 291 | 14 |  | Factoring Sums Using GCF |
| 3 | 10 | Understanding Fraction Division | 3 | 873 | 42 |  | Meaning Of Fraction Quotients; Computing Fraction Quotients; Writing Fraction Division Equations |
| 3 | 11 | Prime Factorization | 2 | 950 | 36 |  | Prime Factorization Of Whole Numbers; Factors And Multiples Breakdown |
| 3 | 12 | Distributive Property Application | 2 | 950 | 36 |  | Factoring With The Distributive Property; Distributive Property For GCF |
| 3 | 13 | Applying Fraction Division | 2 | 950 | 36 |  | Solving Fraction Division Problems; Visual Models For Fraction Division |
| 3 | 14 | Fluent Fraction Division | 2 | 950 | 36 |  | Recognizing Fraction Division Situations; Solving Fraction Quotients |
| 3 | 15 | Fluent Fraction Division (2) | 2 | 950 | 36 |  | Identifying Fraction Division Problems; Applying Fraction Division Algorithms |
| 4 | 2 | Statistics Vocabulary Foundations | 3 | 873 | 42 |  | Recognizing Statistical Questions; Defining Measures Of Center; Defining Measures Of Variation |
| 4 | 3 | Statistical Question Basics | 3 | 873 | 42 |  | Writing Statistical Questions; Identifying Non-Statistical Questions; Explaining Statistical Questions |
| 4 | 4 | Statistical Question Practice | 3 | 873 | 42 |  | Crafting Statistical Questions; Spotting Non-Statistical Questions; Justifying Statistical Classification |
| 4 | 5 | Data Distribution Characteristics | 3 | 873 | 42 |  | Forming Data Distributions; Center Of A Distribution; Spread Of A Distribution |
| 4 | 6 | Data Distribution Characteristics (2) | 1 | 291 | 14 |  | Shape Of A Distribution |
| 4 | 7 | Calculating Measures Of Center | 3 | 873 | 42 |  | Calculating Mean Median Mode; Comparing Measures Of Center; Interpreting Center In Context |
| 4 | 8 | Applying Measures Of Center | 3 | 873 | 42 |  | Finding Mean Median Mode; Choosing Best Measure Of Center; Interpreting Center Values |
| 4 | 9 | Exact Center And Spread | 2 | 582 | 28 |  | Calculating Median And Mean; Calculating IQR And MAD |
| 4 | 10 | Interpreting Data Spread | 2 | 582 | 28 |  | Interpreting Range And IQR; Explaining Data Spread |
| 4 | 11 | Describing Center And Spread | 2 | 582 | 28 |  | Describing Graphed Center And Spread; Summarizing Center And Spread |
| 4 | 12 | Distribution Shape Patterns | 2 | 582 | 28 |  | Symmetric And Skewed Shapes; Identifying Distribution Shapes |
| 4 | 13 | Unusual Data Features | 2 | 582 | 28 |  | Spotting Unusual Data Features; Gaps Peaks And Clusters |
| 4 | 14 | Data Context Interpretation | 2 | 582 | 28 |  | Interpreting Data Context; Connecting Data To Context |
| 4 | 15 | Patterns And Deviations | 2 | 582 | 28 |  | Describing Overall Patterns; Identifying Striking Deviations |
| 4 | 16 | Choosing Center And Spread | 2 | 582 | 28 |  | Selecting Measures Of Center; Selecting Measures Of Variability |
| 4 | 17 | Data Collection Details | 2 | 582 | 28 |  | Measurement Methods And Units; Reporting Sample Size |
| 4 | 18 | Constructing Data Displays | 1 | 659 | 26 |  | Creating Dot Plots |
| 4 | 19 | Constructing Data Displays (2) | 1 | 659 | 26 |  | Creating Histograms |
| 4 | 20 | Constructing Data Displays (3) | 1 | 659 | 26 |  | Creating Box Plots |
| 5 | 2 | Number Line Placement | 2 | 582 | 28 |  | Horizontal Number Line Points; Vertical Number Line Points |
| 5 | 3 | Opposite Numbers | 3 | 873 | 42 |  | Identifying Opposite Pairs; Equal Distance From Zero; Opposite Signs And Location |
| 5 | 4 | Properties Of Opposites | 3 | 873 | 42 |  | Opposite Number Pairs; Distance From Zero Explained; Opposite Of An Opposite |
| 5 | 5 | Properties Of Opposites (2) | 1 | 291 | 14 |  | Zero As Its Own Opposite |
| 5 | 6 | Signed Numbers In Context | 3 | 873 | 42 |  | Representing Quantities With Signed Numbers; Positive And Negative Representations; Opposite Directions And Values |
| 5 | 7 | Meaning Of Zero | 2 | 582 | 28 |  | Zero In Real-World Situations; Interpreting Zero As Reference |
| 5 | 8 | Real-World Rational Quantities | 2 | 950 | 36 |  | Temperature Elevation And Balances; Rational Numbers In Real Contexts |
| 5 | 9 | Positive And Negative Quantities | 2 | 950 | 36 |  | Sea Level Gains And Losses; Describing Opposite Direction Quantities |
| 5 | 10 | Positive And Negative Quantities - Signed Numbers | 2 | 950 | 36 |  | Positive Numbers In Context; Negative Numbers In Context |
| 5 | 11 | Absolute Value As Distance | 3 | 873 | 42 |  | Absolute Value Distance Meaning; Explaining Absolute Value Distance; Defining Absolute Value |
| 5 | 12 | Calculating Absolute Value | 3 | 873 | 42 |  | Computing Absolute Value Of Signed Numbers; Absolute Value Calculations; Absolute Value Of Rational Numbers |
| 5 | 13 | Absolute Value Magnitude | 2 | 582 | 28 |  | Magnitude Of Positive Quantities; Magnitude Of Negative Quantities |
| 5 | 14 | Comparing Absolute Values | 2 | 582 | 28 |  | Comparing Distance From Zero; Greater Absolute Value Distance |
| 5 | 15 | Absolute Value Applications | 2 | 950 | 36 |  | Absolute Value In Real Problems; Applying Magnitude To Contexts |
| 5 | 16 | Inequality On A Number Line | 3 | 873 | 42 |  | Inequality Statements As Position; Position From Inequality Symbols; Farther Left Or Right |
| 5 | 17 | Comparing Rational Numbers | 3 | 873 | 42 |  | Comparing With Inequality Symbols; Rational Number Comparisons; Absolute Value Versus Order |
| 5 | 18 | Order Statements In Context | 3 | 873 | 42 |  | Writing Order Statements; Interpreting Order Statements; Explaining Order Relationships |
| 5 | 19 | Ordering Rational Numbers | 2 | 950 | 36 |  | Ordering Sets Of Numbers; Least To Greatest Ordering |
| 5 | 20 | Applying Comparisons And Order | 2 | 950 | 36 |  | Solving With Comparison And Order; Real-World Ordering Problems |
| 6 | 2 | Coordinate Plane Quadrants | 3 | 873 | 42 |  | Identifying Quadrants by Sign; Quadrant Sign Analysis; Determining Point Quadrants |
| 6 | 3 | Coordinate Plane Quadrants - Quadrant Identification | 1 | 291 | 14 |  | Explaining Sign-Based Quadrants |
| 6 | 4 | Plotting Ordered Pairs | 2 | 950 | 36 |  | Graphing Points in All Quadrants; Plotting Four-Quadrant Points |
| 6 | 5 | Plotting Ordered Pairs - Coordinate Plane | 2 | 766 | 32 |  | Graphing Real-World Coordinates; Plotting Rational Number Pairs |
| 6 | 6 | Axis Reflections | 3 | 873 | 42 |  | Reflections Across the X-Axis; Reflections Across the Y-Axis; Comparing Y-Axis Reflections |
| 6 | 7 | Axis Reflections - Coordinate | 1 | 291 | 14 |  | Identifying X-Axis Reflections |
| 6 | 8 | Reflection Patterns | 2 | 582 | 28 |  | Recognizing Sign-Only Differences; Describing Axis Reflection Relationships |
| 6 | 9 | Coordinate Point Distances | 3 | 873 | 42 |  | Distance Between Shared Coordinates; Finding Horizontal or Vertical Distance; Distance Using Absolute Value |
| 6 | 10 | Coordinate Point Distances - Distance | 1 | 291 | 14 |  | Vertical Coordinate Distance |
| 6 | 11 | Distance Word Problems | 2 | 950 | 36 |  | Solving Coordinate Distance Problems; Applying Distance to Real-World Problems |
| 7 | 2 | Understanding Variables | 3 | 873 | 42 |  | Variables As Unknowns; Variable Value Constraints; Unknown Number Variables |
| 7 | 3 | Understanding Variables - Variable | 1 | 291 | 14 |  | Variable Value Sets |
| 7 | 4 | Writing Algebraic Expressions | 3 | 873 | 42 |  | Expressions From Words; Real-World Expression Writing; Modeling Operations With Expressions |
| 7 | 5 | Writing Algebraic Expressions (2) | 1 | 291 | 14 |  | Expressions For Problem Solving |
| 7 | 6 | Naming Expression Parts | 3 | 873 | 42 |  | Identifying Terms; Identifying Coefficients; Identifying Factors |
| 7 | 7 | Expression Structure And Vocabulary | 3 | 873 | 42 |  | Sums Products And Quotients; Expression Vocabulary Terms; Expressions As Single Units |
| 7 | 8 | Exponential Expressions | 3 | 873 | 42 |  | Writing Exponent Expressions; Comparing Exponent Values; Numerical Exponent Expressions |
| 7 | 9 | Substitution And Equivalence | 2 | 582 | 28 |  | Testing Equivalence By Substitution; Substituting Variable Values |
| 7 | 10 | Applying Properties For Equivalence | 2 | 950 | 36 |  | Equivalence Using Properties; Commutative Property Application |
| 7 | 11 | Applying Properties For Equivalence - Associative Property | 2 | 950 | 36 |  | Associative Property Application; Distributive Property Application |
| 7 | 12 | Evaluating Expressions With Formulas | 1 | 659 | 26 |  | Order Of Operations Evaluation |
| 7 | 13 | Evaluating Expressions With Formulas - Formula Evaluation | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 7 | 14 | Evaluating Exponential Expressions | 1 | 659 | 26 |  | Evaluating Exponent Expressions |
| 7 | 15 | Evaluating Exponential Expressions - Whole Number | 1 | 659 | 26 |  | Whole Number Exponent Evaluation |
| 7 | 16 | Evaluating Exponential Expressions (3) | 1 | 659 | 26 |  | Evaluating Numerical Exponents |
| 7 | 17 | Absolute Value Expressions | 1 | 659 | 26 |  | Evaluating Absolute Value |
| 7 | 18 | Absolute Value Expressions - Exponents | 1 | 659 | 26 |  | Absolute Value With Exponents |
| 7 | 19 | Inverse And Identity Properties | 1 | 659 | 26 |  | Inverse Property Application |
| 7 | 20 | Inverse And Identity Properties - Equivalent Expressions | 1 | 659 | 26 |  | Identity Property Application |
| 7 | 21 | Justifying Equivalent Expressions | 1 | 659 | 26 |  | Justifying Expression Equivalence |
| 7 | 22 | Justifying Equivalent Expressions (2) | 1 | 659 | 26 |  | Commutative Property For Equivalence |
| 7 | 23 | Justifying Equivalent Expressions (3) | 1 | 659 | 26 |  | Associative Property For Equivalence |
| 7 | 24 | Justifying Equivalent Expressions (4) | 1 | 659 | 26 |  | Distributive Property For Equivalence |
| 8 | 2 | Checking Equation Solutions | 2 | 766 | 32 |  | Substitution Check Method; Meaning Of Solving |
| 8 | 3 | Checking Equation Solutions (2) | 1 | 475 | 18 |  | Testing Possible Solutions |
| 8 | 4 | Checking Inequality Solutions | 2 | 766 | 32 |  | Verifying Inequality Solutions; Infinite Solutions Explained |
| 8 | 5 | Checking Inequality Solutions (2) | 1 | 475 | 18 |  | Testing Inequality Values |
| 8 | 6 | One-Step Equations | 2 | 582 | 28 |  | Writing Addition Equations; Writing Multiplication Equations |
| 8 | 7 | One-Step Equations - Addition Multiplication | 2 | 950 | 36 |  | Solving Addition Equations; Solving Multiplication Equations |
| 8 | 8 | Writing Inequalities | 3 | 873 | 42 |  | Graphing Inequality Solutions; Writing Simple Inequalities; Infinite Inequality Solutions |
| 8 | 9 | Writing Inequalities - Number Line | 1 | 291 | 14 |  | Number Line Diagrams |
| 8 | 10 | Interpreting Solutions | 2 | 582 | 28 |  | Interpreting Equation Solutions; Interpreting Inequality Solutions |
| 8 | 11 | Interpreting Solutions - Variable Representation | 1 | 475 | 18 |  | Representing Numbers With Variables |
| 8 | 12 | Independent And Dependent Variables | 2 | 766 | 32 |  | Equations For Variable Relationships; Representing Changing Quantities |
| 8 | 13 | Independent And Dependent Variables (2) | 1 | 291 | 14 |  | Dependent Variable Equations |
| 8 | 14 | Analyzing Variable Relationships | 2 | 950 | 36 |  | Analyzing Data In Tables; Analyzing Relationships In Graphs |
| 8 | 15 | Analyzing Variable Relationships - Dependent Independent | 1 | 291 | 14 |  | Connecting Graphs Tables Equations |
| 8 | 16 | Tables And Graphs | 1 | 659 | 26 |  | Creating Value Tables |
| 8 | 17 | Tables And Graphs - Graphing Relationships | 1 | 659 | 26 |  | Creating Relationship Graphs |
| 9 | 2 | Plotting Polygons | 3 | 873 | 42 |  | Horizontal Side Length; Vertical Side Length; Plotting Polygon Vertices |
| 9 | 3 | Coordinate Perimeter And Area | 3 | 873 | 42 |  | Perimeter On Coordinate Plane; Area On Coordinate Plane; Horizontal And Vertical Side Lengths |
| 9 | 4 | Finding Missing Vertices | 2 | 950 | 36 |  | Missing Vertex Same X-Coordinate; Missing Vertex Same Y-Coordinate |
| 9 | 5 | Finding Missing Vertices - Coordinate Geometry | 1 | 475 | 18 |  | Real-World Coordinate Geometry |
| 9 | 6 | Triangle Area Methods | 2 | 582 | 28 |  | Area Of Right Triangles; Area Of General Triangles |
| 9 | 7 | Quadrilateral And Polygon Area | 3 | 873 | 42 |  | Decomposing Irregular Polygons; Area Of Special Quadrilaterals; Composing And Decomposing Polygons |
| 9 | 8 | Composing And Decomposing Shapes | 2 | 1134 | 44 |  | Composing Shapes For Area; Real-World Area Problems |
| 9 | 9 | Composing And Decomposing Shapes - Area Polygons | 1 | 475 | 18 |  | Composite Shape Area Problems |
| 9 | 10 | Rectangular Prism Volume | 3 | 873 | 42 |  | Volume As Length Width Height; Volume As Base Times Height; Comparing Rectangular Prism Volumes |
| 9 | 11 | Fractional Volume Concepts | 2 | 766 | 32 |  | Unit Cube Packing Volume; Cube Packing Volume Equivalence |
| 9 | 12 | Volume With Fractional Dimensions | 2 | 950 | 36 |  | Volume Formula With Fractional Edges; Base-Height Volume Formula |
| 9 | 13 | Volume With Fractional Dimensions - Prisms | 1 | 475 | 18 |  | Real-World Fractional Volume Problems |
| 9 | 14 | Nets And Surface Area | 2 | 950 | 40 |  | Creating Nets Of Solids; Surface Area From Nets |
| 9 | 15 | Nets And Surface Area - Application | 1 | 475 | 18 |  | Real-World Surface Area Problems |
| 9 | 16 | Constructing Surface Area Models | 2 | 766 | 32 |  | Constructing Three-Dimensional Nets; Calculating Surface Area From Nets |
| 9 | 17 | Constructing Surface Area Models - Nets | 1 | 475 | 18 |  | Real-World Nets And Surface Area |
| 10 | 2 | Arguments And Fallacies | 2 | 766 | 32 |  | Valid Argument Construction; Common Logical Fallacies |
| 10 | 3 | Arguments And Fallacies - Counterexamples | 1 | 475 | 18 |  | Constructing Counterexamples |
| 10 | 4 | Permutations And Combinations | 2 | 766 | 32 |  | Multiplication Counting Principle; Permutation Formula |
| 10 | 5 | Permutations And Combinations (2) | 1 | 291 | 14 |  | Combination Formula |
| 10 | 6 | Recursive Sequences | 2 | 582 | 28 |  | Defining Recursive Sequences; Calculating Sequence Terms |
| 10 | 7 | Recursive Sequences - Fibonacci Sequence | 1 | 475 | 18 |  | Fibonacci Sequence Applications |
| 10 | 8 | Quantifiers And Inference | 2 | 950 | 36 |  | Rules Of Inference; Universal And Existential Quantifiers |
| 10 | 9 | Advanced Counting Strategies | 2 | 950 | 36 |  | Counting With Repetition; Inclusion Exclusion Principle |
| 10 | 10 | Advanced Counting Strategies - Technique Selection | 1 | 475 | 18 |  | Choosing Counting Techniques |
| 10 | 11 | Recursive Applications | 2 | 950 | 36 |  | Recursive Algorithm Design; Modeling With Recursion |
| 10 | 12 | Validity And Convergence | 2 | 1134 | 44 |  | Truth Tables And Validity; Convergence Of Sequences |
| 11 | 2 | Number Systems And Logic | 2 | 766 | 32 |  | Number Base Conversion; Boolean Algebra Simplification |
| 11 | 3 | Number Systems And Logic - Truth Tables | 1 | 659 | 26 |  | Truth Table Design |
| 11 | 4 | Voting Power Indices | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 11 | 5 | Fair Division Foundations | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 11 | 6 | Voting Methods And Winners | 2 | 950 | 36 |  | Plurality And Runoff Voting; Apportionment Methods |
| 11 | 7 | Voting System Fairness | 2 | 1134 | 44 |  | Arrow's Impossibility Theorem; Voting Fairness Criteria |
| 11 | 8 | Proportional Division Methods | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 11 | 9 | Fair Division Evaluation | 2 | 1134 | 44 |  | Fair Division Algorithm Selection; Envy-Free Division Criteria |
| 11 | 10 | Data Encoding And Compression | 2 | 950 | 36 |  | Error-Detection Codes; Data Compression Ratios |
| 11 | 11 | Shortest Paths And Trees | 2 | 950 | 36 |  | Dijkstra's Shortest Path Algorithm; Kruskal's Minimum Spanning Tree |
| 11 | 12 | Network Flow And Coloring | 2 | 950 | 36 |  | Ford-Fulkerson Max Flow; Graph Coloring Scheduling |
| 11 | 13 | Advanced Network Problems | 2 | 1134 | 44 |  | Traveling Salesperson Algorithms; Network Reliability Analysis |
| 11 | 14 | Computation And Security | 2 | 1134 | 44 |  | Algorithmic Time Complexity; Caesar Cipher Encryption |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 203 |
| fill ratio | 32% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=203 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 10 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 31 |
| prompt tokens | 1131855 |
| completion tokens | 167570 |
| max single prompt | 72550 |
| tokens per LO | 4331.4 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 218694 |
| plan_chapters | 10 | 379012 |
| plan_parts | 1 | 72550 |
| titles | 10 | 461599 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 22471 | 1103 | 18346 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 22370 | 2278 | 26492 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 22458 | 2765 | 32322 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 22479 | 2964 | 33687 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 22351 | 1096 | 18533 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 21132 | 2377 | 25178 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 22340 | 2356 | 22796 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 21113 | 2219 | 21994 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 20945 | 2197 | 21825 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 21035 | 3083 | 28669 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 72550 | 20749 | 176055 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 22910 | 10676 | 100471 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 54771 | 9943 | 100693 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 23476 | 9258 | 94035 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 23700 | 10402 | 101157 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 22697 | 5260 | 62572 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 22057 | 14617 | 132986 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 52558 | 7860 | 72121 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 53140 | 7909 | 76769 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 49879 | 5491 | 58172 | 1 |
| 21 | plan_chapters | P10 | claude-sonnet-5 | 53824 | 9596 | 91711 | 1 |
| 22 | titles | 2 | claude-sonnet-5 | 48419 | 3262 | 35025 | 1 |
| 23 | titles | 3 | claude-sonnet-5 | 49318 | 4176 | 41982 | 1 |
| 24 | titles | 4 | claude-sonnet-5 | 50263 | 4088 | 40577 | 1 |
| 25 | titles | 5 | claude-sonnet-5 | 51423 | 4916 | 42856 | 1 |
| 26 | titles | 6 | claude-sonnet-5 | 47279 | 2470 | 30264 | 1 |
| 27 | titles | 7 | claude-sonnet-5 | 49909 | 3892 | 37016 | 1 |
| 28 | titles | 8 | claude-sonnet-5 | 47021 | 2810 | 29837 | 1 |
| 29 | titles | 9 | claude-sonnet-5 | 49317 | 4449 | 40479 | 1 |
| 30 | titles | 10 | claude-sonnet-5 | 21284 | 1030 | 15119 | 1 |
| 31 | titles | 11 | claude-sonnet-5 | 47366 | 2278 | 26077 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 300 |
| avg words per title | 3.55 |
| titles outside 2–5 words | 2 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Ratios, Rates, and Proportions' - 17 understand chapters OK
FINAL: Part 'Fraction, Decimal, and Factor Operations' - 14 understand chapters OK
FINAL: Part 'Statistical Questions and Data Analysis' - 19 understand chapters OK
FINAL: Part 'Rational Numbers and Absolute Value' - 19 understand chapters OK
FINAL: Part 'Graphing on the Coordinate Plane' - 10 understand chapters OK
FINAL: Part 'Algebraic Expressions and Properties' - 23 understand chapters OK
FINAL: Part 'Equations, Inequalities, and Variables' - 16 understand chapters OK
FINAL: Part 'Geometric Measurement and Surface Area' - 16 understand chapters OK
FINAL: Part 'Logic, Proof, and Combinatorics' - 11 understand chapters OK
FINAL: Part 'Networks, Social Choice, and Computation' - 13 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
