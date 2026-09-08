# Run analysis — 20260905-150527_300LOs_Synthetic-300-regen-full_claude_cli

Generated 2026-09-05T15:05:27 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 664.0s

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
| user_prompt | broader, real-world themed units |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **162** (top: Fraction Division ×9, Measures Of Center ×9, Opposite Numbers ×7, Absolute Value ×7, Statistical Questions ×7, Data Distribution ×7, Axis Reflections ×6, Prism Volume ×6, Unit Conversion ×5, Coordinate Distance ×5)

## 3. Output structure

- Parts: **17** (1 overview + 14 content + 2 semester) · Chapters: **215** · Modules: 346 · LO modules: 300
- Content estimate: 115084 words · 7657 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic_300 Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Proportional Reasoning In Everyday Life | 19 | 15 | 34 | 31 | 11965 | 682 |
| 3 | understand | Decimals, Fractions And Factors In Practice | 19 | 15 | 32 | 29 | 10647 | 634 |
| 4 | understand | Signed Numbers In Real-World Contexts | 13 | 9 | 23 | 20 | 6924 | 484 |
| 5 | understand | Comparing And Ordering Rational Numbers | 14 | 10 | 28 | 25 | 8379 | 554 |
| 6 | understand | Mapping Points On The Coordinate Plane | 13 | 9 | 23 | 20 | 6740 | 480 |
| 7 | understand | Building Algebraic Expressions And Properties | 19 | 15 | 29 | 26 | 10694 | 636 |
| 8 | understand | Exponents And Evaluating Formulas | 13 | 9 | 14 | 11 | 5777 | 418 |
| 9 | understand | Modeling Equations And Relationships | 16 | 12 | 27 | 24 | 9376 | 576 |
| 10 | understand | Area And Design On Grid Maps | 12 | 8 | 20 | 17 | 6235 | 450 |
| 11 | understand | Volume And Surface Area In Construction | 11 | 7 | 17 | 14 | 5730 | 416 |
| 12 | understand | Statistical Questions And Center Summaries | 14 | 10 | 26 | 23 | 6693 | 502 |
| 13 | understand | Interpreting Graphs And Data Distributions | 14 | 10 | 20 | 17 | 6051 | 454 |
| 14 | understand | Logical Reasoning, Patterns And Counting | 13 | 9 | 21 | 18 | 7814 | 492 |
| 15 | understand | Networks, Elections And Information Systems | 20 | 16 | 28 | 25 | 12059 | 654 |
| 16 | semester | Synthetic_300 Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 17 | semester | Synthetic_300 Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Ratio Meaning And Notation | 3 | 873 | 42 |  | Writing Ratios Three Ways; Expressing Ratios In Multiple Forms; Defining Ratios |
| 2 | 3 | Ratio Meaning And Notation (2) | 1 | 291 | 14 |  | Ratio Notation And Terms |
| 2 | 4 | Describing Ratios And Rates | 2 | 582 | 28 |  | Describing Ratio Relationships; Using Ratio Language |
| 2 | 5 | Describing Ratios And Rates - Ratio Language | 2 | 950 | 36 |  | Ratio Relationships In Words; Rate Language In Context |
| 2 | 6 | Unit Rate Fundamentals | 3 | 873 | 42 |  | Calculating Unit Rates; Defining Unit Rates; Unit Rate Calculations |
| 2 | 7 | Expressing Unit Rates | 3 | 873 | 42 |  | Unit Rates With Units; Finding Unit Rates; Expressing Rates With Units |
| 2 | 8 | Reading Ratio Tables | 2 | 582 | 28 |  | Completing Ratio Tables; Comparing Ratios With Tables |
| 2 | 9 | Percent In Everyday Life | 2 | 950 | 36 |  | Percent Problem Strategies; Modeling Percent Problems |
| 2 | 10 | Percent In Everyday Life - Calculation Problems | 2 | 766 | 32 |  | Percent Of A Quantity; Finding The Whole Amount |
| 2 | 11 | Converting Measurement Units | 2 | 950 | 36 |  | Ratio Reasoning For Conversions; Rate Reasoning For Conversions |
| 2 | 12 | Converting Measurement Units - Unit Conversion | 1 | 291 | 14 |  | Applying Ratios To Conversions |
| 2 | 13 | Units In Multiplication And Division | 2 | 950 | 36 |  | Units In Multiplication; Units In Division |
| 2 | 14 | Real-World Unit Rate Problems | 2 | 950 | 36 |  | Unit Pricing Problems; Constant Speed Problems |
| 2 | 15 | Building Equivalent Ratio Tables | 2 | 950 | 36 |  | Solving With Equivalent Ratios; Equivalent Ratio Strategies |
| 2 | 16 | Building Equivalent Ratio Tables (2) | 2 | 1134 | 44 |  | Creating Ratio Tables; Graphing Ratio Table Values |
| 3 | 2 | Decimals In Everyday Transactions | 3 | 873 | 42 |  | Adding Multi-Digit Decimals; Subtracting Multi-Digit Decimals; Decimal Sums In Transactions |
| 3 | 3 | Decimals In Everyday Transactions - Decimal Addition | 1 | 291 | 14 |  | Decimal Subtraction Algorithm |
| 3 | 4 | Precision In Measurement Calculations | 3 | 873 | 42 |  | Multiplying Multi-Digit Decimals; Dividing Multi-Digit Decimals; Decimal Multiplication In Measurement |
| 3 | 5 | Precision In Measurement Calculations - Decimal Multiplication | 1 | 291 | 14 |  | Decimal Division Algorithm |
| 3 | 6 | Long Division Fluency | 2 | 582 | 28 |  | Whole Number Long Division; Fluent Division Strategies |
| 3 | 7 | Finding Greatest Common Factors | 3 | 873 | 42 |  | Identifying Greatest Common Factors; Factoring Out Common Factors; Greatest Common Factor In Sums |
| 3 | 8 | Finding Greatest Common Factors - Distributive Property | 1 | 291 | 14 |  | Distributive Factoring Expressions |
| 3 | 9 | Understanding Fraction Division | 3 | 873 | 42 |  | Meaning Of Fraction Quotients; Computing Fraction Quotients; Writing Fraction Division Equations |
| 3 | 10 | Division In Real-World Problems | 2 | 950 | 36 |  | Whole Number Division Word Problems; Real-World Division Applications |
| 3 | 11 | Factoring With The Distributive Property | 2 | 950 | 36 |  | Applying The Distributive Property; Distributive Property Notation |
| 3 | 12 | Prime Factorization Techniques | 2 | 950 | 36 |  | Prime Factorization Of Numbers; Factors And Multiples Analysis |
| 3 | 13 | Fraction Division Word Problems | 2 | 950 | 36 |  | Recognizing Fraction Division Problems; Identifying Division Situations |
| 3 | 14 | Fraction Division Word Problems (2) | 1 | 475 | 18 |  | Solving Fraction Division Problems |
| 3 | 15 | Modeling Fraction Division | 2 | 950 | 36 |  | Interpreting Fraction Quotients; Applying Fraction Division Algorithms |
| 3 | 16 | Modeling Fraction Division (2) | 1 | 475 | 18 |  | Visual Models For Division |
| 4 | 2 | Number Line Basics | 2 | 582 | 28 |  | Horizontal Number Line Placement; Vertical Number Line Placement |
| 4 | 3 | Opposite Number Pairs | 3 | 873 | 42 |  | Identifying Opposite Pairs; Equal Distance From Zero; Locating Opposites On Number Line |
| 4 | 4 | Opposite Number Pairs - Numbers | 1 | 291 | 14 |  | Distance Of Opposite Integers |
| 4 | 5 | Opposite Number Properties | 3 | 873 | 42 |  | Signs And Number Line Sides; Opposite Of An Opposite; Zero As Its Own Opposite |
| 4 | 6 | Meaning Of Signed Numbers | 3 | 873 | 42 |  | Zero In Real-World Situations; Interpreting Zero In Context; Positive And Negative Directions |
| 4 | 7 | Representing Signed Quantities | 2 | 582 | 28 |  | Modeling Quantities With Signed Numbers; Choosing Signed Number Representations |
| 4 | 8 | Signed Numbers In Context | 2 | 950 | 36 |  | Above And Below Sea Level; Temperature Elevation And Balances |
| 4 | 9 | Signed Numbers In Context - Rational Number | 2 | 950 | 36 |  | Rational Numbers For Real Quantities; Gains Losses And Direction |
| 4 | 10 | Positive And Negative Quantities | 2 | 950 | 36 |  | Positive Quantities In Context; Negative Quantities In Context |
| 5 | 2 | Distance From Zero | 3 | 873 | 42 |  | Absolute Value As Distance; Zero Distance Meaning; Defining Absolute Value |
| 5 | 3 | Measuring Magnitude | 3 | 873 | 42 |  | Calculating Absolute Value; Absolute Value Of Signed Numbers; Rational Number Magnitude |
| 5 | 4 | Number Line Positions | 3 | 873 | 42 |  | Inequalities On Number Lines; Number Position From Symbols; Locating Greater And Lesser Values |
| 5 | 5 | Comparing Rational Numbers | 2 | 582 | 28 |  | Comparing With Inequality Symbols; Rational Number Comparisons |
| 5 | 6 | Magnitude Versus Order | 3 | 873 | 42 |  | Comparing Absolute Values; Greater Distance From Zero; Magnitude Versus Numerical Order |
| 5 | 7 | Real-World Order Statements | 3 | 873 | 42 |  | Writing Real-World Order Statements; Interpreting Order Statements; Explaining Real-World Relationships |
| 5 | 8 | Ordering Number Sets | 2 | 950 | 36 |  | Ordering Rational Number Sets; Least To Greatest Ordering |
| 5 | 9 | Magnitude In Everyday Life | 2 | 950 | 36 |  | Absolute Value In Context; Solving Magnitude Problems |
| 5 | 10 | Magnitude In Everyday Life - Absolute Value | 2 | 582 | 28 |  | Magnitude Of Positive Quantities; Magnitude Of Negative Quantities |
| 5 | 11 | Real-World Number Comparisons | 2 | 950 | 36 |  | Applying Rational Number Order; Real-World Comparison Problems |
| 6 | 2 | Plotting Points On Maps | 3 | 873 | 42 |  | Quadrant Sign Analysis; Identifying Point Quadrants; Plotting Rational Coordinates |
| 6 | 3 | Reading Coordinate Signs | 3 | 873 | 42 |  | Determining Quadrant By Sign; Sign Rules For Quadrants; Sign-Only Coordinate Pairs |
| 6 | 4 | Reflections Across Axes | 3 | 873 | 42 |  | X-Axis Reflection Pairs; Y-Axis Reflection Pairs; Identifying Y-Axis Reflections |
| 6 | 5 | Explaining Axis Reflections | 2 | 582 | 28 |  | Identifying X-Axis Reflections; Describing Coordinate Reflections |
| 6 | 6 | Distance On The Grid | 3 | 873 | 42 |  | Horizontal And Vertical Distance; Same-Coordinate Distance Calculation; Distance Using Absolute Value |
| 6 | 7 | Distance On The Grid - Coordinate | 1 | 291 | 14 |  | Vertical Distance With Absolute Value |
| 6 | 8 | Graphing All Quadrants | 2 | 950 | 36 |  | Four-Quadrant Point Graphing; Plotting Points In All Quadrants |
| 6 | 9 | Graphing All Quadrants - Coordinate Plane | 1 | 475 | 18 |  | Real-World Quadrant Graphing |
| 6 | 10 | Mapping Real-World Distances | 2 | 950 | 36 |  | Solving Distance Problems; Applying Coordinate Distance Skills |
| 7 | 2 | Understanding Variables | 3 | 873 | 42 |  | Variables In Context; Variable Value Constraints; Variables As Unknowns |
| 7 | 3 | Understanding Variables - Variable Meaning | 1 | 291 | 14 |  | Variable Value Sets |
| 7 | 4 | Expression Parts Vocabulary | 3 | 873 | 42 |  | Identifying Expression Terms; Identifying Coefficients; Identifying Expression Factors |
| 7 | 5 | Expression Vocabulary In Context | 3 | 873 | 42 |  | Sums Products And Quotients; Naming Expression Parts; Grouping Expression Parts |
| 7 | 6 | Writing Real-World Expressions | 3 | 873 | 42 |  | Translating Verbal Statements; Expressions For Real Situations; Recording Operations As Expressions |
| 7 | 7 | Substitution Verification Methods | 2 | 582 | 28 |  | Verifying Equivalence By Substitution; Writing Expressions To Solve Problems |
| 7 | 8 | Applying Property Rules | 2 | 950 | 36 |  | Commutative Property Application; Associative Property Application |
| 7 | 9 | Applying Property Rules - Distributive | 1 | 475 | 18 |  | Distributive Property Application |
| 7 | 10 | Variables And Equivalent Expressions | 2 | 950 | 36 |  | Verifying Expression Equivalence; Variables In Real-World Problems |
| 7 | 11 | Commutative And Associative Rules | 1 | 659 | 26 |  | Commutative Property Rules |
| 7 | 12 | Commutative And Associative Rules - Properties Operations | 1 | 659 | 26 |  | Associative Property Rules |
| 7 | 13 | Distributive And Inverse Rules | 1 | 659 | 26 |  | Distributive Property Rules |
| 7 | 14 | Distributive And Inverse Rules - Properties Operations | 1 | 659 | 26 |  | Inverse Property Rules |
| 7 | 15 | Justifying Equivalent Expressions | 1 | 659 | 26 |  | Justifying Expression Equivalence |
| 7 | 16 | Justifying Equivalent Expressions - Properties Operations | 1 | 659 | 26 |  | Identity Property Rules |
| 8 | 2 | Writing Exponential Expressions | 2 | 582 | 28 |  | Writing Situational Exponent Expressions; Translating Situations To Exponents |
| 8 | 3 | Exponent Comparison And Substitution | 2 | 582 | 28 |  | Comparing Exponent Expressions; Substituting Values In Expressions |
| 8 | 4 | Evaluating Exponential Expressions | 1 | 659 | 26 |  | Order Of Operations With Exponents |
| 8 | 5 | Evaluating Exponential Expressions - Exponent | 1 | 659 | 26 |  | Applying Exponent Order Rules |
| 8 | 6 | Evaluating Exponential Expressions (3) | 1 | 659 | 26 |  | Evaluating Numerical Exponent Expressions |
| 8 | 7 | Absolute Value And Exponents | 1 | 659 | 26 |  | Evaluating Absolute Value Expressions |
| 8 | 8 | Absolute Value And Exponents (2) | 1 | 659 | 26 |  | Combining Absolute Value And Exponents |
| 8 | 9 | Formula And Expression Evaluation | 1 | 659 | 26 |  | Order Of Operations Without Parentheses |
| 8 | 10 | Formula And Expression Evaluation (2) | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 9 | 2 | Writing Equations And Inequalities | 3 | 873 | 42 |  | Writing Addition Equations; Writing Multiplication Equations; Writing One-Variable Inequalities |
| 9 | 3 | Graphing Inequality Solutions | 3 | 873 | 42 |  | Plotting Inequalities On Number Lines; Infinite Inequality Solution Sets; Recognizing Infinite Solutions |
| 9 | 4 | Graphing Inequality Solutions - Number Line | 1 | 291 | 14 |  | Number Line Solution Diagrams |
| 9 | 5 | Modeling Variable Relationships | 3 | 873 | 42 |  | Writing Relationship Equations; Dependent Variable Equations; Connecting Tables Graphs Equations |
| 9 | 6 | Interpreting Solutions In Context | 3 | 873 | 42 |  | Interpreting Equation Solutions; Interpreting Inequality Solutions; Meaning Of Solving |
| 9 | 7 | Testing Equation And Inequality Solutions | 2 | 950 | 36 |  | Testing Equation Solutions; Testing Inequality Solutions |
| 9 | 8 | Testing Equation And Inequality Solutions - Solution | 2 | 950 | 36 |  | Substitution In Equations; Substitution In Inequalities |
| 9 | 9 | Solving Real-World Equations | 2 | 950 | 36 |  | Solving Addition Equations; Solving Multiplication Equations |
| 9 | 10 | Analyzing Variable Relationships | 2 | 950 | 36 |  | Representing Changing Quantities; Analyzing Relationship Tables |
| 9 | 11 | Analyzing Variable Relationships - Relationship Graphs | 1 | 475 | 18 |  | Analyzing Relationship Graphs |
| 9 | 12 | Relationship Tables And Graphs | 1 | 659 | 26 |  | Creating Relationship Tables |
| 9 | 13 | Relationship Tables And Graphs (2) | 1 | 659 | 26 |  | Creating Relationship Graphs |
| 10 | 2 | Plotting Shapes On Grids | 3 | 873 | 42 |  | Horizontal Side Length; Vertical Side Length; Plotting Polygon Vertices |
| 10 | 3 | Plotting Shapes On Grids - Coordinate Side | 1 | 291 | 14 |  | Polygon Side Lengths |
| 10 | 4 | Grid Perimeter And Area | 2 | 582 | 28 |  | Coordinate Plane Perimeter; Coordinate Plane Area |
| 10 | 5 | Triangle Area Methods | 2 | 582 | 28 |  | Right Triangle Area; General Triangle Area |
| 10 | 6 | Decomposing Polygon Shapes | 3 | 873 | 42 |  | Irregular Polygon Decomposition; Special Quadrilateral Area; Polygon Area By Decomposition |
| 10 | 7 | Rectangle Vertex Puzzles | 2 | 950 | 36 |  | Finding Vertical Rectangle Vertices; Finding Horizontal Rectangle Vertices |
| 10 | 8 | Grid Map Applications | 2 | 950 | 36 |  | Real-World Area Problems; Real-World Polygon Geometry |
| 10 | 9 | Composite Land Area Design | 2 | 1134 | 44 |  | Composing Land Shapes; Composite Shape Area Applications |
| 11 | 2 | Volume Of Building Prisms | 3 | 873 | 42 |  | Prism Volume Using Length Width Height; Prism Volume Using Base Height; Comparing Rectangular Prism Volumes |
| 11 | 3 | Surface Area From Nets | 2 | 582 | 28 |  | Finding Surface Area From Nets; Net-Based Surface Area Calculation |
| 11 | 4 | Fractional Dimension Volumes | 2 | 766 | 32 |  | Volume By Unit Cube Packing; Unit Cubes And Edge Length Volume |
| 11 | 5 | Fractional Dimension Volumes - Prism Volume | 2 | 950 | 36 |  | Fractional Prism Volume With Lwh; Fractional Prism Volume With Base Height |
| 11 | 6 | Construction Measurement Applications | 2 | 950 | 36 |  | Real-World Surface Area Problems; Real-World Fractional Volume Problems |
| 11 | 7 | Constructing And Applying Nets | 2 | 950 | 36 |  | Constructing Nets For Solids; Applying Nets To Real-World Problems |
| 11 | 8 | Designing Composite Nets | 1 | 659 | 26 |  | Designing Nets For Solids |
| 12 | 2 | Recognizing Statistical Questions | 3 | 873 | 42 |  | Writing Statistical Questions; Identifying Non-Statistical Questions; Explaining Statistical Question Criteria |
| 12 | 3 | Statistical Questions In Context | 3 | 873 | 42 |  | Crafting Variability-Based Questions; Distinguishing Deterministic Questions; Justifying Statistical Classifications |
| 12 | 4 | Statistical Questions In Context (2) | 1 | 291 | 14 |  | Classifying Statistical Questions |
| 12 | 5 | Planning Data Investigations | 2 | 582 | 28 |  | Describing Data Attributes; Reporting Sample Size |
| 12 | 6 | Calculating Data Averages | 3 | 873 | 42 |  | Calculating Mean Median Mode; Finding Central Tendency Values; Computing Median And Mean |
| 12 | 7 | Comparing Center Measures | 3 | 873 | 42 |  | Choosing Best Center Measure; Evaluating Measures Of Center; Summarizing Data With One Number |
| 12 | 8 | Comparing Center Measures (2) | 1 | 291 | 14 |  | Matching Center Measure To Shape |
| 12 | 9 | Interpreting Center Values | 2 | 582 | 28 |  | Interpreting Center In Context; Explaining Center Measure Meaning |
| 12 | 10 | Measuring Data Variability | 3 | 873 | 42 |  | Summarizing Spread With One Number; Calculating IQR And MAD; Matching Variability Measure To Shape |
| 12 | 11 | Interpreting Data Spread | 2 | 582 | 28 |  | Interpreting Range And IQR; Explaining Data Spread Meaning |
| 13 | 2 | Understanding Data Distributions | 3 | 873 | 42 |  | Data Set Distributions; Center Of Distribution; Spread Of Distribution |
| 13 | 3 | Understanding Data Distributions - Distribution | 1 | 291 | 14 |  | Shape Of Distribution |
| 13 | 4 | Describing Distribution Traits | 3 | 873 | 42 |  | Center And Spread Description; Symmetric And Skewed Shapes; Analyzing Center And Spread |
| 13 | 5 | Describing Distribution Traits - Shape | 1 | 291 | 14 |  | Symmetric Versus Skewed Distributions |
| 13 | 6 | Spotting Data Anomalies | 2 | 582 | 28 |  | Gaps Peaks And Clusters; Extreme Values And Outliers |
| 13 | 7 | Data Distributions In Context | 3 | 873 | 42 |  | Context From Data Patterns; Interpreting Data Set Origins; Overall Pattern Description |
| 13 | 8 | Data Distributions In Context - Distribution | 1 | 291 | 14 |  | Identifying Data Deviations |
| 13 | 9 | Constructing Data Displays | 1 | 659 | 26 |  | Creating Dot Plots |
| 13 | 10 | Constructing Data Displays (2) | 1 | 659 | 26 |  | Creating Histograms |
| 13 | 11 | Constructing Data Displays (3) | 1 | 659 | 26 |  | Creating Box Plots |
| 14 | 2 | Reasoning About Choices | 3 | 873 | 42 |  | Identifying Logical Fallacies; Calculating Permutations; Calculating Combinations |
| 14 | 3 | Patterns In Sequences | 2 | 582 | 28 |  | Defining Recursive Sequences; Computing Recursive Sequence Terms |
| 14 | 4 | Building Logical Arguments | 2 | 950 | 36 |  | Constructing Valid Arguments; Applying Rules Of Inference |
| 14 | 5 | Building Logical Arguments - Quantifiers | 1 | 475 | 18 |  | Using Logical Quantifiers |
| 14 | 6 | Practical Counting Strategies | 2 | 950 | 36 |  | Multiplication Principle Counting; Counting Arrangements With Repetition |
| 14 | 7 | Practical Counting Strategies - Inclusion-Exclusion Principle | 2 | 950 | 36 |  | Applying Inclusion-Exclusion Principle; Selecting Counting Techniques |
| 14 | 8 | Recursive Models And Growth | 2 | 950 | 36 |  | Modeling With Fibonacci Sequences; Building Recursive Algorithms |
| 14 | 9 | Recursive Models And Growth - Sequence Convergence | 2 | 950 | 36 |  | Analyzing Sequence Convergence; Modeling Growth Recursively |
| 14 | 10 | Evaluating Argument Validity | 2 | 1134 | 44 |  | Testing Validity With Truth Tables; Constructing Counterexamples |
| 15 | 2 | Measuring Voting Power | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 15 | 3 | Two Party Fair Division | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 15 | 4 | Number Systems And Cryptography | 2 | 766 | 32 |  | Number Base Conversion; Caesar Cipher Encryption |
| 15 | 5 | Graph Path Optimization | 2 | 950 | 36 |  | Dijkstra's Shortest Path; Kruskal's Spanning Tree |
| 15 | 6 | Graph Path Optimization - Traveling Salesperson | 1 | 475 | 18 |  | Traveling Salesperson Algorithms |
| 15 | 7 | Voting Methods And Apportionment | 2 | 950 | 36 |  | Arrow's Impossibility Theorem; Comparing Voting Methods |
| 15 | 8 | Voting Methods And Apportionment (2) | 1 | 475 | 18 |  | Legislative Apportionment Methods |
| 15 | 9 | Multi Party Fair Division | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 15 | 10 | Multi Party Fair Division - Algorithm Selection | 1 | 475 | 18 |  | Fair Division Algorithm Selection |
| 15 | 11 | Data Systems Efficiency | 2 | 950 | 36 |  | Error-Detection Codes; Data Compression Ratios |
| 15 | 12 | Data Systems Efficiency - Algorithmic | 1 | 659 | 26 |  | Algorithmic Time Complexity |
| 15 | 13 | Network Flow And Reliability | 2 | 950 | 36 |  | Maximum Flow Networks; Graph Coloring Scheduling |
| 15 | 14 | Network Flow And Reliability (2) | 1 | 659 | 26 |  | Network Reliability Analysis |
| 15 | 15 | Logic And Truth Tables | 2 | 1134 | 44 |  | Boolean Algebra Operations; Constructing Truth Tables |
| 15 | 16 | Fairness Criteria Across Systems | 1 | 659 | 26 |  | Voting Fairness Criteria |
| 15 | 17 | Fairness Criteria Across Systems (2) | 1 | 659 | 26 |  | Fair Division Criteria |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 215 |
| fill ratio | 34% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=215 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 14 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 39 |
| prompt tokens | 1668663 |
| completion tokens | 189486 |
| max single prompt | 60597 |
| tokens per LO | 6193.8 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 244904 |
| plan_chapters | 14 | 661832 |
| plan_parts | 1 | 28372 |
| titles | 14 | 733555 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 25092 | 2717 | 30015 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 24991 | 2246 | 25867 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 25079 | 2564 | 36561 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 25100 | 4123 | 43462 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 24972 | 2157 | 25639 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 24972 | 2307 | 22432 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 23742 | 2697 | 27816 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 23734 | 2636 | 24516 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 23566 | 2176 | 21132 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 23656 | 2255 | 22384 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 28372 | 21784 | 188711 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 25650 | 10742 | 104218 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 25638 | 6182 | 68940 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 55062 | 5091 | 52633 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 58226 | 8232 | 79286 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 56489 | 6418 | 68538 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 60597 | 11286 | 116027 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 52291 | 2985 | 35641 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 60042 | 10115 | 97137 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 56347 | 7521 | 73372 | 1 |
| 21 | plan_chapters | P10 | claude-sonnet-5 | 54993 | 6223 | 70133 | 1 |
| 22 | plan_chapters | P11 | claude-sonnet-5 | 56435 | 6425 | 65257 | 1 |
| 23 | plan_chapters | P12 | claude-sonnet-5 | 51622 | 4168 | 43311 | 1 |
| 24 | plan_chapters | P13 | claude-sonnet-5 | 24013 | 6658 | 68808 | 1 |
| 25 | plan_chapters | P14 | claude-sonnet-5 | 24427 | 15292 | 153161 | 1 |
| 26 | titles | 2 | claude-sonnet-5 | 53950 | 3158 | 34097 | 1 |
| 27 | titles | 3 | claude-sonnet-5 | 54077 | 3371 | 37089 | 1 |
| 28 | titles | 4 | claude-sonnet-5 | 52514 | 2474 | 32052 | 1 |
| 29 | titles | 5 | claude-sonnet-5 | 52762 | 2468 | 30341 | 1 |
| 30 | titles | 6 | claude-sonnet-5 | 52565 | 2371 | 26894 | 1 |
| 31 | titles | 7 | claude-sonnet-5 | 53135 | 2525 | 25435 | 1 |
| 32 | titles | 8 | claude-sonnet-5 | 51104 | 1814 | 25403 | 1 |
| 33 | titles | 9 | claude-sonnet-5 | 52054 | 2551 | 27090 | 1 |
| 34 | titles | 10 | claude-sonnet-5 | 52284 | 2479 | 28416 | 1 |
| 35 | titles | 11 | claude-sonnet-5 | 50492 | 1845 | 23330 | 1 |
| 36 | titles | 12 | claude-sonnet-5 | 51884 | 2467 | 28057 | 1 |
| 37 | titles | 13 | claude-sonnet-5 | 51592 | 2588 | 30313 | 1 |
| 38 | titles | 14 | claude-sonnet-5 | 51823 | 1794 | 21745 | 1 |
| 39 | titles | 15 | claude-sonnet-5 | 53319 | 2581 | 26852 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 300 |
| avg words per title | 3.54 |
| titles outside 2–5 words | 3 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Proportional Reasoning In Everyday Life' - 15 understand chapters OK
FINAL: Part 'Decimals, Fractions And Factors In Practice' - 15 understand chapters OK
FINAL: Part 'Signed Numbers In Real-World Contexts' - 9 understand chapters OK
FINAL: Part 'Comparing And Ordering Rational Numbers' - 10 understand chapters OK
FINAL: Part 'Mapping Points On The Coordinate Plane' - 9 understand chapters OK
FINAL: Part 'Building Algebraic Expressions And Properties' - 15 understand chapters OK
FINAL: Part 'Exponents And Evaluating Formulas' - 9 understand chapters OK
FINAL: Part 'Modeling Equations And Relationships' - 12 understand chapters OK
FINAL: Part 'Area And Design On Grid Maps' - 8 understand chapters OK
FINAL: Part 'Volume And Surface Area In Construction' - 7 understand chapters OK
FINAL: Part 'Statistical Questions And Center Summaries' - 10 understand chapters OK
FINAL: Part 'Interpreting Graphs And Data Distributions' - 10 understand chapters OK
FINAL: Part 'Logical Reasoning, Patterns And Counting' - 9 understand chapters OK
FINAL: Part 'Networks, Elections And Information Systems' - 16 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
