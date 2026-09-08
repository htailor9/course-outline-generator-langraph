# Run analysis — 20260905-145047_300LOs_Synthetic300-UserPrompt_claude_cli

Generated 2026-09-05T14:50:48 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 575.3s

## Verdict

- ✅ all invariants passed
- ✅ no LLM fallbacks
- ✅ no LLM errors
- ✅ pacing within tolerance

## 1. Input

| field | value |
| --- | --- |
| course_title | Synthetic300_UserPrompt |
| grade_band | MS |
| subject_area | Mathematics |
| progression | SKILLS_BASED_PROGRESSION |
| learning objectives | 300 |
| calendar | 5/wk × 128 wk = 640 lesson days |
| minutes_per_lesson | 45 |
| chapter word limit | 2000 |
| user_prompt | Prefer broader units with short names of at most 3 words. Lesson names should emphasise real-world applications. |
| batch_size / concurrency | 30 / 5 |
| planning mode | id-level |

## 2. Annotation (analyser stage)

- Bloom's tier mix: Advanced 27, Foundational 176, Intermediate 97
- Unique primary skills: **126** (top: Equivalent Expressions ×11, Absolute Value ×10, Fraction Division ×9, Prism Volume ×8, Opposite Numbers ×7, Statistical Questions ×7, Fair Division ×6, Measures Of Center ×6, Coordinate Distance ×6, Data Distribution ×6)

## 3. Output structure

- Parts: **12** (1 overview + 9 content + 2 semester) · Chapters: **196** · Modules: 331 · LO modules: 300
- Content estimate: 115084 words · 6757 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic300_UserPrompt Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Number Operations | 19 | 15 | 32 | 29 | 10647 | 634 |
| 3 | understand | Ratios Rates | 20 | 16 | 34 | 31 | 11965 | 682 |
| 4 | understand | Rational Numbers | 25 | 21 | 49 | 46 | 15962 | 884 |
| 5 | understand | Coordinate Plane | 17 | 13 | 32 | 29 | 9911 | 618 |
| 6 | understand | Algebraic Expressions | 25 | 21 | 35 | 32 | 14464 | 788 |
| 7 | understand | Equations Inequalities | 18 | 14 | 31 | 28 | 10724 | 636 |
| 8 | understand | Geometry Measurement | 16 | 12 | 25 | 22 | 8794 | 548 |
| 9 | understand | Data Analysis | 23 | 19 | 43 | 40 | 12744 | 776 |
| 10 | understand | Discrete Mathematics | 28 | 24 | 46 | 43 | 19873 | 966 |
| 11 | semester | Synthetic300_UserPrompt Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 12 | semester | Synthetic300_UserPrompt Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Dividing Whole Numbers | 2 | 582 | 28 |  | Splitting Total Amounts; Dividing Large Quantities |
| 2 | 3 | Balancing Decimal Totals | 3 | 873 | 42 |  | Adding Decimal Amounts; Subtracting Decimal Amounts; Combining Money Totals |
| 2 | 4 | Balancing Decimal Totals - Operations | 1 | 291 | 14 |  | Calculating Change Owed |
| 2 | 5 | Decimal Price Calculations | 3 | 873 | 42 |  | Multiplying Decimal Prices; Dividing Decimal Prices; Calculating Total Cost |
| 2 | 6 | Decimal Price Calculations - Operations | 1 | 291 | 14 |  | Splitting Bills Evenly |
| 2 | 7 | Grouping Items Evenly | 3 | 873 | 42 |  | Finding Common Factors; Factoring Group Sizes; Identifying Shared Factors |
| 2 | 8 | Grouping Items Evenly - Greatest Common | 1 | 291 | 14 |  | Factoring Package Quantities |
| 2 | 9 | Sharing Fractions Fairly | 3 | 873 | 42 |  | Interpreting Fraction Quotients; Computing Fraction Quotients; Writing Fraction Equations |
| 2 | 10 | Division Word Problems | 2 | 950 | 36 |  | Sharing Supplies Equally; Distributing Items Evenly |
| 2 | 11 | Distributive Factoring Method | 2 | 950 | 36 |  | Factoring With Distributive Property; Rewriting Sums As Products |
| 2 | 12 | Prime Factor Trees | 2 | 950 | 36 |  | Building Factor Trees; Finding Prime Factors |
| 2 | 13 | Fraction Division Scenarios | 2 | 950 | 36 |  | Recognizing Division Situations; Spotting Fraction Division Clues |
| 2 | 14 | Fraction Division Scenarios (2) | 1 | 475 | 18 |  | Solving Recipe Division Problems |
| 2 | 15 | Visualizing Fraction Division | 2 | 950 | 36 |  | Applying Fraction Division Algorithms; Interpreting Fraction Quotient Results |
| 2 | 16 | Visualizing Fraction Division (2) | 1 | 475 | 18 |  | Modeling Fraction Division Visually |
| 3 | 2 | Recipe Ratios | 3 | 873 | 42 |  | Recipe Ratio Notation; Ratios In Recipe Words; Defining Recipe Ratios |
| 3 | 3 | Recipe Ratios (2) | 1 | 291 | 14 |  | Recipe Ratio Terminology |
| 3 | 4 | Comparing Quantities | 2 | 582 | 28 |  | Describing Quantity Relationships; Ratio Language For Quantities |
| 3 | 5 | Comparing Quantities - Ratios | 1 | 475 | 18 |  | Word Form Ratio Comparisons |
| 3 | 6 | Shopping Unit Rates | 3 | 873 | 42 |  | Shopping Price Unit Rates; Calculating Shopping Unit Rates; Defining Unit Rate |
| 3 | 7 | Everyday Rates | 3 | 873 | 42 |  | Everyday Rate Descriptions; Unit Rates With Units; Calculating Everyday Unit Rates |
| 3 | 8 | Everyday Rates - Unit | 1 | 475 | 18 |  | Real-World Rate Language |
| 3 | 9 | Measurement Conversions | 2 | 950 | 36 |  | Converting Measurements With Ratios; Ratio Reasoning For Conversions |
| 3 | 10 | Measurement Conversions - Unit Conversion | 1 | 291 | 14 |  | Converting Units With Ratios |
| 3 | 11 | Scaling Recipes | 2 | 950 | 36 |  | Scaling Recipes With Ratio Tables; Equivalent Ratios For Recipes |
| 3 | 12 | Percents In Sales | 2 | 950 | 36 |  | Percent Problems In Sales; Sales Discounts With Percents |
| 3 | 13 | Percents In Sales - Percent | 2 | 766 | 32 |  | Percent Of A Quantity; Finding The Whole Amount |
| 3 | 14 | Prices And Speed | 2 | 950 | 36 |  | Comparing Unit Prices; Calculating Constant Speed |
| 3 | 15 | Calculating With Units | 2 | 950 | 36 |  | Multiplying Measurement Units; Dividing Measurement Units |
| 3 | 16 | Graphing Ratio Tables | 2 | 950 | 40 |  | Building Ratio Tables; Finding Missing Ratio Values |
| 3 | 17 | Graphing Ratio Tables (2) | 2 | 766 | 32 |  | Plotting Ratio Pairs; Comparing Ratios With Tables |
| 4 | 2 | Number Line Mapping | 2 | 582 | 28 |  | Horizontal Number Line Position; Vertical Number Line Position |
| 4 | 3 | Reading Opposites | 3 | 873 | 42 |  | Identifying Opposite Numbers; Opposite Numbers On Number Line; Opposite Signs And Position |
| 4 | 4 | Opposite Number Rules | 3 | 873 | 42 |  | Equal Distance From Zero; Distance Of Integer Pairs; Opposite Of Opposite |
| 4 | 5 | Opposite Number Rules - Numbers | 1 | 291 | 14 |  | Zero As Its Own Opposite |
| 4 | 6 | Real-World Zero | 2 | 582 | 28 |  | Zero In Real-World Contexts; Meaning Of Zero Value |
| 4 | 7 | Gains And Losses | 3 | 873 | 42 |  | Representing Gains And Losses; Positive And Negative Quantities; Opposite Direction Values |
| 4 | 8 | Distance From Zero | 3 | 873 | 42 |  | Meaning Of Absolute Value; Absolute Value As Distance; Defining Absolute Value |
| 4 | 9 | Calculating Magnitude | 3 | 873 | 42 |  | Calculating Absolute Value; Absolute Value Of Rationals; Computing Absolute Value |
| 4 | 10 | Magnitude In Context | 2 | 582 | 28 |  | Magnitude Of Positive Quantities; Magnitude Of Negative Quantities |
| 4 | 11 | Comparing Distances | 3 | 873 | 42 |  | Comparing Absolute Values; Greater Distance From Zero; Absolute Value Vs Order |
| 4 | 12 | Number Line Comparisons | 3 | 873 | 42 |  | Comparing With Inequality Symbols; Rational Numbers And Inequalities; Inequality As Number Line Position |
| 4 | 13 | Left Or Right | 2 | 582 | 28 |  | Position From Inequality Symbols; Left Or Right Position |
| 4 | 14 | Ordering Real Quantities | 3 | 873 | 42 |  | Writing Real-World Order Statements; Interpreting Real-World Order Statements; Explaining Real-World Order Relationships |
| 4 | 15 | Temperature And Elevation | 2 | 950 | 36 |  | Sea Level And Direction; Temperature Elevation Balances |
| 4 | 16 | Temperature And Elevation - Rational Numbers | 1 | 475 | 18 |  | Rational Numbers In Real Life |
| 4 | 17 | Balances And Directions | 2 | 950 | 36 |  | Above And Below Sea Level; Positive Numbers In Context |
| 4 | 18 | Balances And Directions - Signed Numbers | 1 | 475 | 18 |  | Negative Numbers In Context |
| 4 | 19 | Ordering Rational Numbers | 2 | 950 | 36 |  | Least To Greatest Ordering; Ordering Sets Of Rationals |
| 4 | 20 | Real-World Comparisons | 2 | 950 | 36 |  | Solving With Rational Comparisons; Applying Order To Real Problems |
| 4 | 21 | Absolute Value Applications | 2 | 950 | 36 |  | Absolute Value In Real Life; Real-World Distance And Temperature |
| 4 | 22 | Absolute Value Expressions | 1 | 659 | 26 |  | Evaluating Absolute Value Expressions |
| 5 | 2 | Plotting Map Points | 3 | 873 | 42 |  | Quadrant Sign Analysis; Identifying Map Quadrants; Plotting Rational Coordinates |
| 5 | 3 | Reading Sign Clues | 2 | 582 | 28 |  | Identifying Quadrants; Explaining Sign Rules |
| 5 | 4 | Mirror Across X-Axis | 3 | 873 | 42 |  | X-Axis Reflection Pairs; Identifying X-Axis Reflections; Sign-Only Coordinate Pairs |
| 5 | 5 | Mirror Across Y-Axis | 3 | 873 | 42 |  | Y-Axis Reflection Pairs; Identifying Y-Axis Reflections; Reflection Sign Relationships |
| 5 | 6 | Measuring Yard Distances | 3 | 873 | 42 |  | Same-Coordinate Distances; Horizontal Vertical Distances; Distance Using Absolute Value |
| 5 | 7 | Measuring Fence Sides | 3 | 873 | 42 |  | Horizontal Side Length; Vertical Side Length; Vertical Distance Absolute Value |
| 5 | 8 | Designing Backyard Gardens | 3 | 873 | 42 |  | Coordinate Polygon Perimeter; Coordinate Polygon Area; Drawing Polygon Vertices |
| 5 | 9 | Designing Backyard Gardens - Coordinate Polygons | 1 | 291 | 14 |  | Polygon Side Lengths |
| 5 | 10 | Plotting Field Positions | 2 | 950 | 36 |  | Graphing Four Quadrants; Four-Quadrant Point Graphing |
| 5 | 11 | Plotting Field Positions - Coordinate Plane | 1 | 475 | 18 |  | Real-World Coordinate Graphing |
| 5 | 12 | Solving Travel Distances | 2 | 950 | 36 |  | Real-World Distance Problems; Travel Distance Calculations |
| 5 | 13 | Completing Building Blueprints | 2 | 950 | 36 |  | Missing Vertex X-Coordinate; Missing Vertex Y-Coordinate |
| 5 | 14 | Completing Building Blueprints - Coordinate Polygons | 1 | 475 | 18 |  | Real-World Polygon Applications |
| 6 | 2 | Variables In Context | 2 | 582 | 28 |  | Variables As Unknowns; Constraints On Variable Values |
| 6 | 3 | Everyday Expressions | 3 | 873 | 42 |  | Translating Words To Expressions; Modeling Real-World Quantities; Recording Operations As Expressions |
| 6 | 4 | Expression Parts | 3 | 873 | 42 |  | Identifying Terms; Identifying Coefficients; Identifying Factors |
| 6 | 5 | Expression Parts - Vocabulary | 1 | 291 | 14 |  | Sums Products And Quotients |
| 6 | 6 | Compound Terms | 2 | 582 | 28 |  | Naming Expression Parts; Grouping Terms As Units |
| 6 | 7 | Exponents In Practice | 3 | 873 | 42 |  | Writing Exponential Expressions; Comparing Exponent Values; Numerical Exponent Expressions |
| 6 | 8 | Substituting Values | 2 | 582 | 28 |  | Testing Equivalence By Substitution; Substituting Variable Values |
| 6 | 9 | Equivalent Expressions | 2 | 950 | 36 |  | Verifying Equivalence With Properties; Commutative Property Expressions |
| 6 | 10 | Equivalent Expressions (2) | 2 | 950 | 36 |  | Associative Property Expressions; Distributive Property Expressions |
| 6 | 11 | Properties In Action | 1 | 659 | 26 |  | Applying Commutative Property |
| 6 | 12 | Properties In Action - Equivalent Expressions | 1 | 659 | 26 |  | Applying Associative Property |
| 6 | 13 | Properties In Action (3) | 1 | 659 | 26 |  | Applying Distributive Property |
| 6 | 14 | Justifying Equivalence | 1 | 659 | 26 |  | Justifying Expression Equivalence |
| 6 | 15 | Justifying Equivalence - Equivalent Expressions | 1 | 659 | 26 |  | Applying Inverse Properties |
| 6 | 16 | Justifying Equivalence (3) | 1 | 659 | 26 |  | Applying Identity Properties |
| 6 | 17 | Evaluating Exponents | 1 | 659 | 26 |  | Evaluating Exponential Expressions |
| 6 | 18 | Evaluating Exponents - Whole Number | 1 | 659 | 26 |  | Order Of Operations With Exponents |
| 6 | 19 | Evaluating Exponents - Exponential Expressions | 1 | 659 | 26 |  | Evaluating Numerical Exponents |
| 6 | 20 | Real-World Formulas | 1 | 659 | 26 |  | Absolute Value And Exponents |
| 6 | 21 | Real-World Formulas - Expression Evaluation | 1 | 659 | 26 |  | Order Of Operations Basics |
| 6 | 22 | Real-World Formulas (3) | 1 | 659 | 26 |  | Evaluating Real-World Formulas |
| 7 | 2 | Real-World Variables | 3 | 873 | 42 |  | Writing Variable Expressions; Variables As Unknowns; Variables Representing Number Sets |
| 7 | 3 | Modeling With Equations | 2 | 582 | 28 |  | Writing Addition Equations; Writing Multiplication Equations |
| 7 | 4 | Solutions In Context | 3 | 873 | 42 |  | Interpreting Equation Solutions; Interpreting Inequality Solutions; Infinite Inequality Solutions |
| 7 | 5 | Solutions In Context - Solution Testing | 1 | 291 | 14 |  | Meaning Of Solving |
| 7 | 6 | Real-World Inequalities | 3 | 873 | 42 |  | Graphing Inequality Solutions; Writing Real-World Constraints; Infinite Solution Sets |
| 7 | 7 | Real-World Inequalities - Inequality Solutions | 1 | 291 | 14 |  | Number Line Diagrams |
| 7 | 8 | Modeling Relationships | 3 | 873 | 42 |  | Writing Relationship Equations; Expressing Dependent Variables; Connecting Graphs Tables Equations |
| 7 | 9 | Solving Real Equations | 2 | 950 | 36 |  | Solving Addition Equations; Solving Multiplication Equations |
| 7 | 10 | Testing Possible Solutions | 2 | 950 | 36 |  | Checking Equation Solutions; Checking Inequality Solutions |
| 7 | 11 | Testing Possible Solutions - Solution | 2 | 950 | 36 |  | Testing Equation Values; Testing Inequality Values |
| 7 | 12 | Analyzing Real Relationships | 2 | 950 | 36 |  | Variables In Real Problems; Relating Changing Quantities |
| 7 | 13 | Analyzing Real Relationships - Dependent Independent | 2 | 950 | 36 |  | Analyzing Relationships With Tables; Analyzing Relationships With Graphs |
| 7 | 14 | Charting Real Data | 1 | 659 | 26 |  | Building Data Tables |
| 7 | 15 | Charting Real Data - Relationship Graphs | 1 | 659 | 26 |  | Building Relationship Graphs |
| 8 | 2 | Floor Plan Areas | 3 | 873 | 42 |  | Triangular Floor Sections; Irregular Triangle Floor Areas; Special Quadrilateral Floor Areas |
| 8 | 3 | Land Area Problems | 2 | 766 | 32 |  | Polygon Land Area; Composite Land Area Problems |
| 8 | 4 | Irregular Land Plots | 2 | 950 | 40 |  | Decomposing Irregular Land Plots; Composing Combined Land Areas |
| 8 | 5 | Irregular Land Plots - Composing Decomposing | 1 | 475 | 18 |  | Real World Land Solutions |
| 8 | 6 | Storage Box Volume | 3 | 873 | 42 |  | Volume Using Length Width Height; Volume Using Base and Height; Comparing Storage Container Volumes |
| 8 | 7 | Fractional Box Volume | 2 | 766 | 32 |  | Fractional Edge Unit Cubes; Unit Cubes and Volume Formula |
| 8 | 8 | Fractional Box Volume - Prism | 1 | 475 | 18 |  | Volume Formula With Fractions |
| 8 | 9 | Shipping Crate Volume | 2 | 950 | 36 |  | Base Height Formula for Crates; Real World Shipping Crate Volumes |
| 8 | 10 | Wrapping Paper Area | 2 | 950 | 40 |  | Nets for 3D Figures; Surface Area From Nets |
| 8 | 11 | Wrapping Paper Area - Surface | 1 | 475 | 18 |  | Wrapping Paper Surface Problems |
| 8 | 12 | Product Packaging Design | 2 | 766 | 32 |  | Packaging Net Construction; Packaging Surface Area Calculation |
| 8 | 13 | Product Packaging Design - Nets Surface | 1 | 475 | 18 |  | Real World Packaging Design Problems |
| 9 | 2 | Asking Survey Questions | 3 | 873 | 42 |  | Writing Statistical Questions; Non-Statistical Questions; Justifying Statistical Questions |
| 9 | 3 | Asking Survey Questions - Statistical | 1 | 291 | 14 |  | Identifying Statistical Questions |
| 9 | 4 | Evaluating Poll Questions | 3 | 873 | 42 |  | Crafting Poll Questions; Flawed Poll Questions; Analyzing Poll Questions |
| 9 | 5 | Planning Data Studies | 2 | 582 | 28 |  | Attributes And Measurement; Counting Observations |
| 9 | 6 | Data Distributions | 3 | 873 | 42 |  | Forming Distributions; Center Of Distribution; Spread Of Distribution |
| 9 | 7 | Data Distributions - Distribution | 1 | 291 | 14 |  | Shape Of Distribution |
| 9 | 8 | Reading Data Graphs | 2 | 582 | 28 |  | Center And Spread Analysis; Data Display Vocabulary |
| 9 | 9 | Shapes Of Data | 2 | 582 | 28 |  | Symmetric Vs Skewed Data; Classifying Distribution Shapes |
| 9 | 10 | Spotting Data Outliers | 2 | 582 | 28 |  | Gaps Peaks And Clusters; Extreme Values Detection |
| 9 | 11 | Patterns In Data | 2 | 582 | 28 |  | Overall Data Patterns; Data Deviations |
| 9 | 12 | Data In Context | 2 | 582 | 28 |  | Context From Graphs; Real-World Data Stories |
| 9 | 13 | Calculating Averages | 3 | 873 | 42 |  | Mean Median And Mode; Comparing Center Measures; Interpreting Center Values |
| 9 | 14 | Team Stats Averages | 3 | 873 | 42 |  | Calculating Team Averages; Best Fit Team Stat; Interpreting Team Stats |
| 9 | 15 | Choosing Best Average | 3 | 873 | 42 |  | Center As Single Number; Calculating Median And Mean; Choosing Center Measure |
| 9 | 16 | Understanding Data Spread | 3 | 873 | 42 |  | Interpreting Range And IQR; Range And IQR Meaning; Variation As Single Number |
| 9 | 17 | Measuring Data Spread | 2 | 582 | 28 |  | Calculating IQR And MAD; Choosing Spread Measure |
| 9 | 18 | Graphing Real Data | 1 | 659 | 26 |  | Creating Dot Plots |
| 9 | 19 | Graphing Real Data - Displays | 1 | 659 | 26 |  | Creating Histograms |
| 9 | 20 | Graphing Real Data (3) | 1 | 659 | 26 |  | Creating Box Plots |
| 10 | 2 | Everyday Arguments | 2 | 766 | 32 |  | Building Valid Arguments; Spotting Logical Fallacies |
| 10 | 3 | Arranging And Choosing | 2 | 582 | 28 |  | Ordering Race Results; Choosing Team Combinations |
| 10 | 4 | Building Number Patterns | 2 | 582 | 28 |  | Recursive Sequence Rules; Calculating Sequence Terms |
| 10 | 5 | Measuring Voting Power | 2 | 582 | 28 |  | Banzhaf Power Index; Shapley-Shubik Power Index |
| 10 | 6 | Two Party Fair Division | 2 | 766 | 32 |  | Divider-Chooser Method; Adjusted Winner Procedure |
| 10 | 7 | Digital Number Systems | 2 | 766 | 32 |  | Converting Number Bases; Simplifying Boolean Expressions |
| 10 | 8 | Building Logical Proofs | 2 | 950 | 36 |  | Rules Of Inference; Universal And Existential Quantifiers |
| 10 | 9 | Building Logical Proofs - Counterexamples | 1 | 475 | 18 |  | Disproving With Counterexamples |
| 10 | 10 | Counting Possible Outcomes | 2 | 950 | 36 |  | Multiplication Counting Principle; Counting With Repetition |
| 10 | 11 | Selecting Counting Strategies | 2 | 950 | 36 |  | Inclusion-Exclusion Principle; Comparing Counting Techniques |
| 10 | 12 | Modeling Growth Patterns | 2 | 950 | 36 |  | Fibonacci Sequence Applications; Modeling Population Growth |
| 10 | 13 | Recursive Computation | 2 | 950 | 36 |  | Recursive Algorithm Implementation; Sequence Convergence Analysis |
| 10 | 14 | Network Routing | 2 | 950 | 36 |  | Dijkstra's Shortest Path; Kruskal's Minimum Spanning Tree |
| 10 | 15 | Network Routing - Flow | 1 | 475 | 18 |  | Maximum Network Flow |
| 10 | 16 | Elections And Representation | 2 | 950 | 36 |  | Comparing Voting Methods; Apportioning Legislative Seats |
| 10 | 17 | Multi Party Fair Shares | 2 | 950 | 36 |  | Lone-Divider Method; Last-Diminisher Method |
| 10 | 18 | Securing Digital Data | 2 | 950 | 36 |  | Detecting Data Errors; Encrypting With Ciphers |
| 10 | 19 | Testing Argument Validity | 1 | 659 | 26 |  | Evaluating Argument Validity |
| 10 | 20 | Testing Argument Validity - Truth Tables | 1 | 659 | 26 |  | Designing Truth Tables |
| 10 | 21 | Scheduling And Reliability | 2 | 950 | 36 |  | Traveling Salesperson Routes; Graph Coloring Schedules |
| 10 | 22 | Scheduling And Reliability - Network | 1 | 659 | 26 |  | Network Reliability Analysis |
| 10 | 23 | Fair Voting Systems | 2 | 1134 | 44 |  | Arrow's Impossibility Theorem; Voting Fairness Criteria |
| 10 | 24 | Judging Fair Divisions | 2 | 1134 | 44 |  | Choosing Fair Division Methods; Evaluating Division Fairness |
| 10 | 25 | Efficient Data Processing | 2 | 1134 | 44 |  | Data Compression Ratios; Algorithmic Efficiency Comparison |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 196 |
| fill ratio | 31% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=196 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 9 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 30 |
| prompt tokens | 1111735 |
| completion tokens | 187182 |
| max single prompt | 73674 |
| tokens per LO | 4329.7 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 221093 |
| plan_chapters | 9 | 302239 |
| plan_parts | 1 | 73674 |
| titles | 10 | 514729 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 22589 | 2289 | 26994 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 22488 | 3255 | 32420 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 22576 | 3797 | 40348 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 22597 | 3336 | 35970 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 22469 | 2333 | 26011 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 22469 | 4654 | 44930 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 21239 | 3278 | 32289 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 21231 | 2307 | 21859 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 21063 | 2283 | 22668 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 22372 | 2704 | 26215 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 73674 | 21842 | 178646 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 22937 | 9898 | 100695 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 56869 | 11876 | 119880 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 23777 | 11024 | 106547 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 56792 | 11535 | 112188 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 23168 | 9447 | 96625 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 21681 | 10786 | 109876 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 52164 | 8278 | 88890 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 22267 | 11060 | 110082 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 22584 | 12741 | 114890 | 1 |
| 21 | titles | 2 | claude-sonnet-5 | 49575 | 4300 | 42764 | 1 |
| 22 | titles | 3 | claude-sonnet-5 | 49593 | 4492 | 43016 | 1 |
| 23 | titles | 4 | claude-sonnet-5 | 52264 | 5730 | 53417 | 1 |
| 24 | titles | 5 | claude-sonnet-5 | 48859 | 3240 | 34681 | 1 |
| 25 | titles | 5 | claude-sonnet-5 | 42758 | 356 | 11580 | 1 |
| 26 | titles | 6 | claude-sonnet-5 | 49251 | 3673 | 37790 | 1 |
| 27 | titles | 7 | claude-sonnet-5 | 73322 | 4189 | 37518 | 1 |
| 28 | titles | 8 | claude-sonnet-5 | 47835 | 3048 | 33567 | 1 |
| 29 | titles | 9 | claude-sonnet-5 | 49255 | 3981 | 38726 | 1 |
| 30 | titles | 10 | claude-sonnet-5 | 52017 | 5450 | 52076 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 299 |
| avg words per title | 3.38 |
| titles outside 2–5 words | 0 |
| titles with generic words | 0 |
| LO fallbacks by kind | none |
| soft invariant failures | none |
| LLM errors | none |

## 7. Enforcement log

```
FINAL: Part 'Number Operations' - 15 understand chapters OK
FINAL: Part 'Ratios Rates' - 16 understand chapters OK
FINAL: Part 'Rational Numbers' - 21 understand chapters OK
FINAL: Part 'Coordinate Plane' - 13 understand chapters OK
FINAL: Part 'Algebraic Expressions' - 21 understand chapters OK
FINAL: Part 'Equations Inequalities' - 14 understand chapters OK
FINAL: Part 'Geometry Measurement' - 12 understand chapters OK
FINAL: Part 'Data Analysis' - 19 understand chapters OK
FINAL: Part 'Discrete Mathematics' - 24 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
