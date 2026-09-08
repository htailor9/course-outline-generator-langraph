# Run analysis — 20260908-111618_300LOs_Synthetic-300-regen-full_claude_cli

Generated 2026-09-08T11:16:18 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 578.1s

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
| user_prompt | — |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **139** (top: Measures Of Center ×9, Prism Volume ×8, Fraction Division ×7, Opposite Numbers ×7, Statistical Questions ×7, Coordinate Distance ×6, Absolute Value ×6, Expression Vocabulary ×6, Inequality Solutions ×6, Unit Conversion ×5)

## 3. Output structure

- Parts: **20** (1 overview + 17 content + 2 semester) · Chapters: **229** · Modules: 355 · LO modules: 300
- Content estimate: 115084 words · 8197 minutes across understand chapters
- Min-4 merges applied: 2

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic_300 Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Ratios Rates And Percents | 22 | 18 | 34 | 31 | 11965 | 682 |
| 3 | understand | Fraction And Whole Number Division | 11 | 7 | 16 | 13 | 5255 | 394 |
| 4 | understand | Decimals Factors And Multiples | 12 | 8 | 19 | 16 | 5392 | 420 |
| 5 | understand | Integers And Signed Numbers | 13 | 9 | 21 | 18 | 6342 | 456 |
| 6 | understand | Absolute Value And Rational Comparison | 14 | 10 | 27 | 24 | 8088 | 540 |
| 7 | understand | The Cartesian Plane | 14 | 10 | 23 | 20 | 6740 | 480 |
| 8 | understand | Statistical Questions And Measures Of Center | 13 | 9 | 25 | 22 | 6402 | 488 |
| 9 | understand | Analyzing Data Distributions | 13 | 9 | 21 | 18 | 6342 | 468 |
| 10 | understand | Algebraic Expressions And Evaluation | 13 | 9 | 21 | 18 | 6158 | 460 |
| 11 | understand | Properties And Exponent Rules | 19 | 15 | 22 | 19 | 10313 | 594 |
| 12 | understand | Solving Equations And Inequalities | 17 | 13 | 30 | 27 | 10249 | 618 |
| 13 | understand | Coordinate Distance And Composite Regions | 12 | 8 | 20 | 17 | 6235 | 450 |
| 14 | understand | Volume And Surface Area | 11 | 7 | 17 | 14 | 5730 | 416 |
| 15 | understand | Logical Reasoning And Argumentation | 8 | 4 | 9 | 6 | 2850 | 292 |
| 16 | understand | Counting Combinatorics And Recursive Sequences | 10 | 6 | 15 | 12 | 4964 | 380 |
| 17 | understand | Graph Theory & Voting Apportionment | 10 | 6 | 15 | 12 | 5700 | 404 |
| 18 | understand | Equitable Resource & Number Systems | 12 | 8 | 16 | 13 | 6359 | 430 |
| 19 | semester | Synthetic_300 Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 20 | semester | Synthetic_300 Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Ratio Definitions | 3 | 873 | 42 |  | Ratio Notation Forms; Writing Ratios Three Ways; Ratio As Comparison |
| 2 | 3 | Ratio Definitions (2) | 1 | 291 | 14 |  | Ratio Notation And Terms |
| 2 | 4 | Ratio Language | 2 | 582 | 28 |  | Describing Ratio Relationships; Verbal Ratio Comparisons |
| 2 | 5 | Ratio Language (2) | 1 | 475 | 18 |  | Ratio Relationships In Words |
| 2 | 6 | Unit Rate Foundations | 3 | 873 | 42 |  | Calculating Unit Rates; Unit Rate From Ratios; Defining Unit Rate |
| 2 | 7 | Unit Rate Foundations (2) | 1 | 291 | 14 |  | Unit Rates With Nonzero Terms |
| 2 | 8 | Expressing Unit Rates | 2 | 582 | 28 |  | Unit Rates With Units; Naming Unit Rate Units |
| 2 | 9 | Expressing Unit Rates - Rate | 1 | 475 | 18 |  | Rate Language In Context |
| 2 | 10 | Ratio Table Basics | 2 | 950 | 40 |  | Building Ratio Tables; Finding Missing Table Values |
| 2 | 11 | Ratio Table Basics - Tables | 1 | 291 | 14 |  | Comparing Ratios With Tables |
| 2 | 12 | Equivalent Ratios And Graphs | 2 | 950 | 36 |  | Equivalent Ratio Strategies; Modeling Equivalent Ratios |
| 2 | 13 | Equivalent Ratios And Graphs - Ratio Tables | 1 | 475 | 18 |  | Graphing Ratio Table Values |
| 2 | 14 | Unit Rate Applications | 2 | 950 | 36 |  | Unit Pricing Problems; Constant Speed Problems |
| 2 | 15 | Percent Calculations | 2 | 766 | 32 |  | Percent Of A Quantity; Finding The Whole Amount |
| 2 | 16 | Percent Problem Solving | 2 | 950 | 36 |  | Percent Reasoning Models; Solving Percent Problems |
| 2 | 17 | Unit Conversion | 2 | 950 | 36 |  | Converting Measurement Units; Ratio Reasoning For Conversions |
| 2 | 18 | Unit Conversion (2) | 1 | 291 | 14 |  | Applying Ratios To Convert Units |
| 2 | 19 | Unit Analysis In Operations | 2 | 950 | 36 |  | Multiplying With Unit Analysis; Dividing With Unit Analysis |
| 3 | 2 | Whole Number Division Fluency | 2 | 582 | 28 |  | Standard Division Algorithm; Multi-Digit Quotient Fluency |
| 3 | 3 | Fraction Quotient Foundations | 3 | 873 | 42 |  | Meaning Of Fraction Quotients; Dividing Fractions By Fractions; Equations For Fraction Division |
| 3 | 4 | Whole Number Division Applications | 2 | 950 | 36 |  | Whole Number Division Problems; Real-World Division Scenarios |
| 3 | 5 | Fraction Division In Context | 2 | 950 | 36 |  | Identifying Fraction Division Situations; Recognizing Fraction Division Problems |
| 3 | 6 | Fraction Division In Context (2) | 1 | 475 | 18 |  | Solving Fraction Division Problems |
| 3 | 7 | Interpreting Fraction Quotients | 2 | 950 | 36 |  | Applying Fraction Division Algorithms; Contextual Fraction Quotients |
| 3 | 8 | Interpreting Fraction Quotients - Division | 1 | 475 | 18 |  | Modeling Fraction Division Visually |
| 4 | 2 | Decimal Addition And Subtraction | 3 | 873 | 42 |  | Adding Multi-Digit Decimals; Subtracting Multi-Digit Decimals; Decimal Addition Algorithm |
| 4 | 3 | Decimal Addition And Subtraction (2) | 1 | 291 | 14 |  | Decimal Subtraction Algorithm |
| 4 | 4 | Decimal Multiplication And Division | 3 | 873 | 42 |  | Multiplying Multi-Digit Decimals; Dividing Multi-Digit Decimals; Decimal Multiplication Algorithm |
| 4 | 5 | Decimal Multiplication And Division (2) | 1 | 291 | 14 |  | Decimal Division Algorithm |
| 4 | 6 | Greatest Common Factor | 3 | 873 | 42 |  | Identifying Common Factors; Factoring Out Common Factors; Finding Shared Factors |
| 4 | 7 | Greatest Common Factor - Distributive Property | 1 | 291 | 14 |  | Factoring Sums Distributively |
| 4 | 8 | Distributive Property Factoring | 2 | 950 | 36 |  | Distributive Property Notation; Writing Factored Expressions |
| 4 | 9 | Prime Factorization | 2 | 950 | 36 |  | Prime Factorization Method; Factor Trees And Primes |
| 5 | 2 | Opposite Number Pairs | 3 | 873 | 42 |  | Locating Opposite Numbers; Number Line Opposite Pairs; Opposite Signs And Position |
| 5 | 3 | Distance And Symmetry | 3 | 873 | 42 |  | Equal Distance From Zero; Opposite Numbers Equidistant Property; Opposite Of An Opposite |
| 5 | 4 | Distance And Symmetry - Opposite Numbers | 1 | 291 | 14 |  | Zero As Its Own Opposite |
| 5 | 5 | Signed Number Meaning | 2 | 582 | 28 |  | Representing Quantities With Signed Numbers; Positive And Negative Value Meaning |
| 5 | 6 | Zero In Real Contexts | 3 | 873 | 42 |  | Zero In Real-World Situations; Interpreting Zero In Context; Modeling Quantities With Signed Numbers |
| 5 | 7 | Directional Quantities | 2 | 950 | 36 |  | Opposite Directions With Signed Numbers; Positive Numbers For Real Quantities |
| 5 | 8 | Directional Quantities - Signed Numbers | 1 | 475 | 18 |  | Negative Numbers For Real Quantities |
| 5 | 9 | Applying Signed Quantities | 2 | 950 | 36 |  | Rational Numbers For Real Contexts; Applying Rational Numbers To Context |
| 5 | 10 | Applying Signed Quantities - Numbers Context | 1 | 475 | 18 |  | Gains Losses And Sea Level |
| 6 | 2 | Number Line Placement | 2 | 582 | 28 |  | Horizontal Number Line Placement; Vertical Number Line Placement |
| 6 | 3 | Understanding Absolute Value | 3 | 873 | 42 |  | Absolute Value As Distance; Meaning Of Absolute Value; Defining Absolute Value |
| 6 | 4 | Calculating Absolute Value | 3 | 873 | 42 |  | Absolute Value Of Signed Numbers; Computing Absolute Value; Absolute Value Of Rational Numbers |
| 6 | 5 | Absolute Value Comparisons | 3 | 873 | 42 |  | Comparing Absolute Values; Greater Distance From Zero; Absolute Value As Magnitude |
| 6 | 6 | Absolute Value Comparisons - Magnitude | 1 | 291 | 14 |  | Magnitude Of Negative Quantities |
| 6 | 7 | Rational Number Comparison Basics | 3 | 873 | 42 |  | Comparing With Inequality Symbols; Inequality Symbol Comparisons; Absolute Value Versus Order |
| 6 | 8 | Rational Number Order Statements | 3 | 873 | 42 |  | Writing Order Statements; Interpreting Order Statements; Explaining Order Relationships |
| 6 | 9 | Ordering Rational Numbers | 2 | 950 | 36 |  | Ordering Least To Greatest; Ordering Greatest To Least |
| 6 | 10 | Real-World Magnitude Applications | 2 | 950 | 36 |  | Absolute Value In Context; Applying Rational Number Ordering |
| 6 | 11 | Real-World Magnitude Applications - Rational Number | 2 | 950 | 36 |  | Real-World Rational Comparisons; Real-World Absolute Value Problems |
| 7 | 2 | Plotting Ordered Pairs | 3 | 873 | 42 |  | Identifying Quadrants By Sign; Determining Quadrant Location; Plotting Points On Plane |
| 7 | 3 | Quadrant Sign Analysis | 2 | 582 | 28 |  | Quadrant Location From Signs; Explaining Sign Quadrant Rules |
| 7 | 4 | Reflections Across Axes | 3 | 873 | 42 |  | X-Axis Reflection Pairs; Y-Axis Reflection Pairs; Identifying Y-Axis Reflections |
| 7 | 5 | Reflections Across Axes - Coordinate | 1 | 291 | 14 |  | Identifying X-Axis Reflections |
| 7 | 6 | Recognizing Axis Symmetry | 2 | 582 | 28 |  | Sign-Only Coordinate Pairs; Describing Reflection Relationships |
| 7 | 7 | Measuring Coordinate Distance | 3 | 873 | 42 |  | Distance On Shared Axis; Horizontal And Vertical Distance; Vertical Distance With Absolute Value |
| 7 | 8 | Measuring Coordinate Distance (2) | 1 | 291 | 14 |  | Horizontal Distance With Absolute Value |
| 7 | 9 | Graphing All Quadrants | 2 | 950 | 36 |  | Graphing Four-Quadrant Points; Plotting Points All Quadrants |
| 7 | 10 | Graphing All Quadrants - Coordinate Plane | 1 | 475 | 18 |  | Graphing Points For Problems |
| 7 | 11 | Applying Coordinate Distance | 2 | 950 | 36 |  | Real-World Coordinate Distance; Applying Distance To Problems |
| 8 | 2 | Recognizing Statistical Questions | 3 | 873 | 42 |  | Writing Statistical Questions; Statistical Question Examples; Identifying Variability In Questions |
| 8 | 3 | Distinguishing Statistical Questions | 3 | 873 | 42 |  | Statistical Question Non-Examples; Explaining Statistical Questions; Writing Non-Statistical Questions |
| 8 | 4 | Distinguishing Statistical Questions (2) | 1 | 291 | 14 |  | Justifying Statistical Questions |
| 8 | 5 | Center And Spread Concepts | 3 | 873 | 42 |  | Describing Center And Spread; Measures Of Center Concept; Measures Of Variation Concept |
| 8 | 6 | Calculating Center Measures | 3 | 873 | 42 |  | Calculating Mean Median Mode; Finding Mean Median Mode; Calculating Mean And Median |
| 8 | 7 | Comparing Center Measures | 3 | 873 | 42 |  | Comparing Measures Of Center; Choosing Best Center Measure; Selecting Center Measures By Shape |
| 8 | 8 | Interpreting Center Measures | 2 | 582 | 28 |  | Interpreting Center In Context; Explaining Center Measure Meaning |
| 8 | 9 | Applying Variability Measures | 3 | 873 | 42 |  | Interpreting Range And IQR; Explaining Data Spread; Calculating IQR And MAD |
| 8 | 10 | Applying Variability Measures (2) | 1 | 291 | 14 |  | Selecting Variability Measures |
| 9 | 2 | Investigating Data Attributes | 3 | 873 | 42 |  | Data As Distributions; Attribute Measurement Units; Counting Data Observations |
| 9 | 3 | Center Spread And Shape | 3 | 873 | 42 |  | Identifying Center; Identifying Spread; Identifying Shape |
| 9 | 4 | Analyzing Distribution Shape | 3 | 873 | 42 |  | Describing Center And Spread; Symmetric Or Skewed Shapes; Classifying Distribution Shape |
| 9 | 5 | Outliers Gaps And Clusters | 2 | 582 | 28 |  | Gaps Peaks And Clusters; Identifying Data Anomalies |
| 9 | 6 | Data Patterns In Context | 3 | 873 | 42 |  | Interpreting Data Context; Context From Data Patterns; Overall Patterns In Context |
| 9 | 7 | Data Patterns In Context - Distribution | 1 | 291 | 14 |  | Identifying Data Deviations |
| 9 | 8 | Constructing Data Displays | 1 | 659 | 26 |  | Constructing Dot Plots |
| 9 | 9 | Constructing Data Displays (2) | 1 | 659 | 26 |  | Constructing Histograms |
| 9 | 10 | Constructing Data Displays (3) | 1 | 659 | 26 |  | Constructing Box Plots |
| 10 | 2 | Expression Vocabulary Basics | 3 | 873 | 42 |  | Identifying Expression Terms; Identifying Coefficients; Identifying Expression Factors |
| 10 | 3 | Expression Structure Terms | 3 | 873 | 42 |  | Sums Products And Quotients; Naming Expression Parts; Grouping Terms As One Unit |
| 10 | 4 | Understanding Variables | 3 | 873 | 42 |  | Variables As Unknown Values; Variable Value Constraints; Variables Representing Numbers |
| 10 | 5 | Understanding Variables - Variable Representation | 1 | 291 | 14 |  | Variable Domains In Context |
| 10 | 6 | Writing Algebraic Expressions | 3 | 873 | 42 |  | Translating Verbal Statements; Expressions For Real-World Relationships; Recording Operations As Expressions |
| 10 | 7 | Writing Algebraic Expressions (2) | 1 | 291 | 14 |  | Expressions For Problem Solving |
| 10 | 8 | Variable Substitution | 2 | 766 | 32 |  | Substituting Values For Variables; Representing Unknowns With Variables |
| 10 | 9 | Order Of Operations Evaluation | 1 | 659 | 26 |  | Order Of Operations Without Parentheses |
| 10 | 10 | Order Of Operations Evaluation - Expression | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 11 | 2 | Exponents And Expression Equivalence | 3 | 873 | 42 |  | Writing Exponential Expressions; Comparing Exponential Values; Testing Expression Equivalence |
| 11 | 3 | Exponents And Expression Equivalence (2) | 1 | 291 | 14 |  | Writing Exponential Notation |
| 11 | 4 | Applying Properties To Expressions | 2 | 950 | 36 |  | Verifying Expression Equivalence; Commutative Property Applications |
| 11 | 5 | Applying Properties To Expressions - Associative Property | 2 | 950 | 36 |  | Associative Property Applications; Distributive Property Applications |
| 11 | 6 | Generating Equivalent Expressions | 1 | 659 | 26 |  | Commutative Property Expressions |
| 11 | 7 | Generating Equivalent Expressions - Associative Property | 1 | 659 | 26 |  | Associative Property Expressions |
| 11 | 8 | Generating Equivalent Expressions - Distributive Property | 1 | 659 | 26 |  | Distributive Property Expressions |
| 11 | 9 | Justifying Property Equivalence | 1 | 659 | 26 |  | Justifying Expression Equivalence |
| 11 | 10 | Justifying Property Equivalence - Inverse Properties | 1 | 659 | 26 |  | Inverse Property Expressions |
| 11 | 11 | Justifying Property Equivalence - Identity Properties | 1 | 659 | 26 |  | Identity Property Expressions |
| 11 | 12 | Evaluating Exponential Expressions | 1 | 659 | 26 |  | Order Of Operations With Exponents |
| 11 | 13 | Evaluating Exponential Expressions - Exponent | 1 | 659 | 26 |  | Exponent Evaluation Order |
| 11 | 14 | Evaluating Exponential Expressions - Exponents | 1 | 659 | 26 |  | Numerical Exponent Evaluation |
| 11 | 15 | Absolute Value And Exponents | 1 | 659 | 26 |  | Absolute Value Order Of Operations |
| 11 | 16 | Absolute Value And Exponents (2) | 1 | 659 | 26 |  | Absolute Value With Exponents |
| 12 | 2 | Understanding Solution Meaning | 3 | 873 | 42 |  | Equation Solutions In Context; Inequality Solutions In Context; Meaning Of Solving |
| 12 | 3 | Writing One-Step Equations | 2 | 582 | 28 |  | Writing Addition Equations; Writing Multiplication Equations |
| 12 | 4 | Number Line Inequality Reasoning | 3 | 873 | 42 |  | Inequality Statements On Number Lines; Number Position From Inequalities; Comparing Positions Using Inequalities |
| 12 | 5 | Inequality Notation And Graphs | 3 | 873 | 42 |  | Graphing Inequality Solutions; Writing One-Variable Inequalities; Number Line Inequality Diagrams |
| 12 | 6 | Infinite Solution Sets | 2 | 582 | 28 |  | Infinitely Many Inequality Solutions; Recognizing Infinite Solution Sets |
| 12 | 7 | Modeling Variable Relationships | 3 | 873 | 42 |  | Equations From Variable Relationships; Dependent Variable Equations; Connecting Graphs Tables Equations |
| 12 | 8 | Verifying Solutions By Substitution | 2 | 950 | 36 |  | Testing Equation Solutions; Testing Inequality Solutions |
| 12 | 9 | Verifying Solutions By Substitution - Solution Verification | 2 | 950 | 36 |  | Substitution Check For Equations; Substitution Check For Inequalities |
| 12 | 10 | Solving One-Step Equations | 2 | 950 | 36 |  | Solving Addition Equations; Solving Multiplication Equations |
| 12 | 11 | Analyzing Variable Relationships | 2 | 950 | 36 |  | Representing Related Quantities; Variable Relationships In Tables |
| 12 | 12 | Analyzing Variable Relationships (2) | 1 | 475 | 18 |  | Variable Relationships In Graphs |
| 12 | 13 | Building Relationship Representations | 1 | 659 | 26 |  | Tables For Variable Relationships |
| 12 | 14 | Building Relationship Representations - Dependent Independent | 1 | 659 | 26 |  | Graphs For Variable Relationships |
| 13 | 2 | Coordinate Side Lengths | 2 | 582 | 28 |  | Horizontal Side Length; Vertical Side Length |
| 13 | 3 | Coordinate Polygon Construction | 2 | 582 | 28 |  | Plotting Polygon Vertices; Polygon Side Lengths |
| 13 | 4 | Coordinate Perimeter And Area | 2 | 582 | 28 |  | Coordinate Polygon Perimeter; Coordinate Polygon Area |
| 13 | 5 | Triangle Area Decomposition | 2 | 582 | 28 |  | Right Triangle Area; General Triangle Area |
| 13 | 6 | Irregular Polygon Area | 3 | 873 | 42 |  | Decomposing Irregular Polygons; Special Quadrilateral Area; Composite Polygon Area |
| 13 | 7 | Rectangle Vertex Coordinates | 2 | 950 | 36 |  | Vertices With Shared X-Coordinate; Vertices With Shared Y-Coordinate |
| 13 | 8 | Real-World Geometry Applications | 2 | 950 | 36 |  | Coordinate Geometry Word Problems; Composite Area Word Problems |
| 13 | 9 | Composite Shape Construction | 2 | 1134 | 44 |  | Combining Polygon Areas; Composite Area Applications |
| 14 | 2 | Whole Number Prism Volume | 3 | 873 | 42 |  | Volume By Length Width Height; Volume By Base Area; Comparing Rectangular Prism Volumes |
| 14 | 3 | Surface Area From Nets | 2 | 582 | 28 |  | Surface Area Via Nets; Net-Based Surface Area |
| 14 | 4 | Unit Cube Volume Packing | 2 | 766 | 32 |  | Volume By Cube Packing; Cube Packing Volume Equivalence |
| 14 | 5 | Fractional Prism Volume Applications | 2 | 950 | 36 |  | Fractional Volume Length Width Height; Fractional Volume By Base Area |
| 14 | 6 | Fractional Prism Volume Applications (2) | 1 | 475 | 18 |  | Fractional Volume Word Problems |
| 14 | 7 | Applied Surface Area | 2 | 950 | 36 |  | Surface Area Word Problems; Building Nets With Triangles |
| 14 | 8 | Advanced Net Construction | 2 | 1134 | 44 |  | Rectangle-Triangle Net Design; Net Construction Word Problems |
| 15 | 2 | Logical Fallacies | 1 | 291 | 14 |  | Identifying Logical Fallacies |
| 15 | 3 | Constructing Logical Arguments | 2 | 950 | 36 |  | Symbolic Argument Construction; Rules Of Inference |
| 15 | 4 | Quantifiers And Counterexamples | 2 | 950 | 36 |  | Universal And Existential Quantifiers; Constructing Counterexamples |
| 15 | 5 | Evaluating Argument Validity | 1 | 659 | 26 |  | Truth Tables For Validity |
| 16 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Ordered Arrangement Permutations; Unordered Selection Combinations |
| 16 | 3 | Recursive Sequence Foundations | 2 | 582 | 28 |  | Recursive Sequence Definitions; Arithmetic Geometric Term Calculation |
| 16 | 4 | Counting Techniques And Strategies | 2 | 950 | 36 |  | Multiplication Principle Counting; Counting Arrangements With Repetition |
| 16 | 5 | Counting Techniques And Strategies - Inclusion-Exclusion Principle | 2 | 950 | 36 |  | Inclusion-Exclusion Set Counting; Choosing Counting Techniques |
| 16 | 6 | Fibonacci And Recursive Algorithms | 2 | 950 | 36 |  | Fibonacci Sequence Modeling; Recursive Algorithm Implementation |
| 16 | 7 | Convergence And Recursive Modeling | 2 | 950 | 36 |  | Sequence Convergence Analysis; Recursive Growth Modeling |
| 17 | 2 | Shortest Paths And Trees | 2 | 950 | 36 |  | Dijkstra's Shortest Path Algorithm; Kruskal's Minimum Spanning Tree |
| 17 | 3 | Network Flow And Routing | 2 | 950 | 36 |  | Ford-Fulkerson Max Flow; Traveling Salesperson Algorithms |
| 17 | 4 | Coloring And Network Reliability | 2 | 1134 | 44 |  | Graph Coloring Scheduling; Network Reliability Analysis |
| 17 | 5 | Voting Power Indices | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 17 | 6 | Voting And Apportionment Methods | 2 | 950 | 36 |  | Comparing Voting Methods; Apportionment Method Comparison |
| 17 | 7 | Voting Fairness Criteria | 2 | 1134 | 44 |  | Arrow's Impossibility Theorem; Evaluating Fairness Criteria |
| 18 | 2 | Two-Party Fair Division | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 18 | 3 | Multi-Party Fair Division | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 18 | 4 | Evaluating Fair Division | 2 | 1134 | 44 |  | Choosing Fair Division Methods; Evaluating Division Fairness |
| 18 | 5 | Number Base Conversion | 1 | 291 | 14 |  | Converting Between Number Bases |
| 18 | 6 | Information Encoding Techniques | 2 | 950 | 36 |  | Boolean Algebra Simplification; Error Detection Codes |
| 18 | 7 | Information Encoding Techniques - Data Compression | 2 | 950 | 36 |  | Data Compression Ratios; Cryptographic Encryption Methods |
| 18 | 8 | Logic And Complexity | 1 | 659 | 26 |  | Truth Table Construction |
| 18 | 9 | Logic And Complexity - Algorithmic Efficiency | 1 | 659 | 26 |  | Algorithmic Efficiency Analysis |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 229 |
| fill ratio | 36% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=229 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 17 content parts; all parts >= 4 understand chapters: True.
- Merges applied: 2 (see enforcement_log).

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 47 |
| prompt tokens | 1701106 |
| completion tokens | 171921 |
| max single prompt | 63707 |
| tokens per LO | 6243.4 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 185305 |
| plan_chapters | 19 | 773981 |
| plan_parts | 1 | 63707 |
| titles | 17 | 678113 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 18035 | 2707 | 30998 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 17934 | 2167 | 25732 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 19241 | 1059 | 19616 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 19262 | 2412 | 29801 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 19134 | 4193 | 43137 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 17915 | 2450 | 21722 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 17904 | 2702 | 36502 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 19115 | 2197 | 23251 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 18947 | 2622 | 25473 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 17818 | 2415 | 23467 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 63707 | 18471 | 156211 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 46685 | 8126 | 80083 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 44495 | 6732 | 82678 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 41360 | 3364 | 39170 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 41765 | 3594 | 37105 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 43716 | 6094 | 67284 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 43954 | 6263 | 66287 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 43063 | 5451 | 53828 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 43197 | 5245 | 52143 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 18155 | 2213 | 25299 | 1 |
| 21 | plan_chapters | P10 | claude-sonnet-5 | 45024 | 7845 | 81869 | 1 |
| 22 | plan_chapters | P11 | claude-sonnet-5 | 18547 | 7207 | 67524 | 1 |
| 23 | plan_chapters | P12 | claude-sonnet-5 | 42564 | 5236 | 53930 | 1 |
| 24 | plan_chapters | P13 | claude-sonnet-5 | 41174 | 4042 | 43455 | 1 |
| 25 | plan_chapters | P14 | claude-sonnet-5 | 38253 | 1579 | 21660 | 1 |
| 26 | plan_chapters | P15 | claude-sonnet-5 | 42203 | 5269 | 54920 | 1 |
| 27 | plan_chapters | P16 | claude-sonnet-5 | 38832 | 2159 | 35587 | 1 |
| 28 | plan_chapters | P17 | claude-sonnet-5 | 59808 | 2301 | 30286 | 1 |
| 29 | plan_chapters | P18 | claude-sonnet-5 | 38624 | 1875 | 28919 | 1 |
| 30 | plan_chapters | P19 | claude-sonnet-5 | 42562 | 5814 | 65804 | 1 |
| 31 | titles | 2 | claude-sonnet-5 | 42498 | 3601 | 36186 | 1 |
| 32 | titles | 3 | claude-sonnet-5 | 39519 | 1827 | 27463 | 1 |
| 33 | titles | 4 | claude-sonnet-5 | 39260 | 2131 | 27442 | 1 |
| 34 | titles | 5 | claude-sonnet-5 | 41623 | 3444 | 34898 | 1 |
| 35 | titles | 6 | claude-sonnet-5 | 40416 | 2530 | 29831 | 1 |
| 36 | titles | 7 | claude-sonnet-5 | 40437 | 2622 | 29142 | 1 |
| 37 | titles | 8 | claude-sonnet-5 | 40011 | 2219 | 31356 | 1 |
| 38 | titles | 9 | claude-sonnet-5 | 39295 | 1914 | 21781 | 1 |
| 39 | titles | 10 | claude-sonnet-5 | 39358 | 1907 | 21692 | 1 |
| 40 | titles | 11 | claude-sonnet-5 | 40730 | 3168 | 35071 | 1 |
| 41 | titles | 12 | claude-sonnet-5 | 40491 | 2365 | 27052 | 1 |
| 42 | titles | 13 | claude-sonnet-5 | 39471 | 1946 | 23215 | 1 |
| 43 | titles | 14 | claude-sonnet-5 | 39567 | 2454 | 30783 | 1 |
| 44 | titles | 15 | claude-sonnet-5 | 38120 | 844 | 16612 | 1 |
| 45 | titles | 16 | claude-sonnet-5 | 39505 | 1572 | 20755 | 1 |
| 46 | titles | 17 | claude-sonnet-5 | 38895 | 1712 | 50839 | 2 |
| 47 | titles | 18 | claude-sonnet-5 | 38917 | 1861 | 24453 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 299 |
| avg words per title | 3.53 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
MERGE: Part 'Graph Theory And Network Algorithms' (3 chapters) merged with 'Voting And Apportionment Methods' (3 chapters)
RESULT: Part 'Graph Theory & Voting Apportionment' now has 6 chapters
MERGE: Part 'Equitable Resource Allocation' (3 chapters) merged with 'Number Systems And Information Theory' (5 chapters)
RESULT: Part 'Equitable Resource & Number Systems' now has 8 chapters
FINAL: Part 'Ratios Rates And Percents' - 18 understand chapters OK
FINAL: Part 'Fraction And Whole Number Division' - 7 understand chapters OK
FINAL: Part 'Decimals Factors And Multiples' - 8 understand chapters OK
FINAL: Part 'Integers And Signed Numbers' - 9 understand chapters OK
FINAL: Part 'Absolute Value And Rational Comparison' - 10 understand chapters OK
FINAL: Part 'The Cartesian Plane' - 10 understand chapters OK
FINAL: Part 'Statistical Questions And Measures Of Center' - 9 understand chapters OK
FINAL: Part 'Analyzing Data Distributions' - 9 understand chapters OK
FINAL: Part 'Algebraic Expressions And Evaluation' - 9 understand chapters OK
FINAL: Part 'Properties And Exponent Rules' - 15 understand chapters OK
FINAL: Part 'Solving Equations And Inequalities' - 13 understand chapters OK
FINAL: Part 'Coordinate Distance And Composite Regions' - 8 understand chapters OK
FINAL: Part 'Volume And Surface Area' - 7 understand chapters OK
FINAL: Part 'Logical Reasoning And Argumentation' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics And Recursive Sequences' - 6 understand chapters OK
FINAL: Part 'Graph Theory & Voting Apportionment' - 6 understand chapters OK
FINAL: Part 'Equitable Resource & Number Systems' - 8 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
