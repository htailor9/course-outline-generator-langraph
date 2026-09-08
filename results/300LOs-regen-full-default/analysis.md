# Run analysis — 20260905-151319_300LOs_Synthetic-300-regen-full_claude_cli

Generated 2026-09-05T15:13:19 · provider **claude_cli** · models `{'default': 'sonnet', 'annotate': 'sonnet', 'titles': 'sonnet'}` · wall 466.9s

## Verdict

- ✅ all invariants passed
- ⚠ fallbacks used: {'titles_fallback': 300, 'plan_chapters_fallback': 25}
- ❌ LLM errors: 21
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
- Unique primary skills: **159** (top: Measures Of Center ×9, Opposite Numbers ×7, Statistical Questions ×7, Prism Volume ×7, Fraction Division ×6, Axis Reflections ×6, Expression Vocabulary ×6, Unit Conversion ×5, Coordinate Distance ×5, Signed Numbers In Context ×5)

## 3. Output structure

- Parts: **21** (1 overview + 18 content + 2 semester) · Chapters: **242** · Modules: 358 · LO modules: 300
- Content estimate: 115084 words · 8377 minutes across understand chapters
- Min-4 merges applied: 0

| # | type | part | chapters | understand | modules | LOs | words | minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | overview | Synthetic_300 Course Overview | 1 | 0 | 2 | 0 | 0 | 45 |
| 2 | understand | Ratios Rates And Percents | 19 | 15 | 34 | 31 | 11965 | 682 |
| 3 | understand | Fraction And Whole Number Division | 11 | 7 | 16 | 13 | 5255 | 394 |
| 4 | understand | Decimals Factors And Multiples | 12 | 8 | 19 | 16 | 5392 | 420 |
| 5 | understand | Integers And Signed Numbers | 13 | 9 | 21 | 18 | 6342 | 456 |
| 6 | understand | Absolute Value And Number Comparison | 14 | 10 | 28 | 25 | 8379 | 554 |
| 7 | understand | The Cartesian Plane | 15 | 11 | 25 | 22 | 7322 | 508 |
| 8 | understand | Statistical Questions And Center Measures | 14 | 10 | 26 | 23 | 6693 | 502 |
| 9 | understand | Data Distribution And Summary | 13 | 9 | 20 | 17 | 6051 | 454 |
| 10 | understand | Algebraic Terms And Evaluation | 11 | 7 | 18 | 15 | 5101 | 414 |
| 11 | understand | Exponents And Equivalent Expressions | 17 | 13 | 22 | 19 | 10313 | 594 |
| 12 | understand | Equations Inequalities And Relationships | 19 | 15 | 30 | 27 | 10433 | 622 |
| 13 | understand | Coordinate Geometry And Area | 11 | 7 | 17 | 14 | 4810 | 392 |
| 14 | understand | Volume And Surface Area | 14 | 10 | 20 | 17 | 7155 | 474 |
| 15 | understand | Logical Reasoning And Argumentation | 8 | 4 | 9 | 6 | 2850 | 292 |
| 16 | understand | Counting Combinatorics And Recursive Sequences | 10 | 6 | 15 | 12 | 4964 | 380 |
| 17 | understand | Graph Theory Voting And Apportionment | 15 | 11 | 15 | 12 | 5700 | 404 |
| 18 | understand | Equitable Resource Allocation | 10 | 6 | 9 | 6 | 2850 | 292 |
| 19 | understand | Number Systems And Information Theory | 11 | 7 | 10 | 7 | 3509 | 318 |
| 20 | semester | Synthetic_300 Semester A Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |
| 21 | semester | Synthetic_300 Semester B Reflect & Review | 2 | 0 | 1 | 0 | 0 | 90 |

### Understand chapters

| part | ch | chapter | LOs | words | min | limit | module titles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | Ratio Meaning And Language | 3 | 873 | 42 |  | Ratio Language: Describe; Ratio Notation: Describe; Ratio Definition: Define |
| 2 | 3 | Ratio Notation Forms | 3 | 873 | 42 |  | Ratio Notation: Express; Ratio Notation: Express (L135); Ratio Notation: Express (L236) |
| 2 | 4 | Unit Rate Foundations | 3 | 873 | 42 |  | Unit Rate: Calculate; Unit Rate: Calculate (L140); Unit Rate Definition: Define |
| 2 | 5 | Expressing Unit Rates | 3 | 873 | 42 |  | Unit Rate: Describe; Unit Rate: Describe (L141); Unit Rate Calculation: Calculate |
| 2 | 6 | Ratio Tables Basics | 2 | 582 | 28 |  | Equivalent Ratio Tables: Calculate; Equivalent Ratio Tables: Compare |
| 2 | 7 | Percent And Conversion Foundations | 2 | 582 | 28 |  | Percent Calculation: Calculate; Unit Conversion: Convert |
| 2 | 8 | Rate Language Applications | 2 | 950 | 36 |  | Ratio Language: Use; Rate Language: Use |
| 2 | 9 | Equivalent Ratios And Graphing | 2 | 950 | 36 |  | Equivalent Ratios: Solve; Equivalent Ratios: Solve (L139) |
| 2 | 10 | Equivalent Ratios And Graphing - Ratio Table | 1 | 475 | 18 |  | Ratio Table Graphing: Plot |
| 2 | 11 | Unit Rate Applications | 2 | 950 | 36 |  | Unit Rate Applications: Solve; Unit Rate Applications: Solve (L247) |
| 2 | 12 | Percent Problem Solving | 2 | 950 | 36 |  | Percent Problems: Solve; Percent Problem Solving: Solve |
| 2 | 13 | Percent Problem Solving (2) | 1 | 475 | 18 |  | Percent Problem Solving: Solve |
| 2 | 14 | Unit Conversion Applications | 2 | 950 | 36 |  | Unit Conversion: Solve; Unit Conversion: Solve (L138) |
| 2 | 15 | Unit Conversion Applications (2) | 2 | 950 | 36 |  | Unit Conversion: Transform; Unit Conversion: Transform (L250) |
| 2 | 16 | Constructing Ratio Tables | 1 | 659 | 26 |  | Equivalent Ratio Tables: Create |
| 3 | 2 | Multi-Digit Division Fluency | 2 | 582 | 28 |  | Whole Number Division: Divide; Whole Number Division: Divide (L128) |
| 3 | 3 | Fraction Quotient Foundations | 3 | 873 | 42 |  | Fraction Division: Explain; Fraction Division: Compute; Fraction Division Word Problems: Write |
| 3 | 4 | Real-World Division Problems | 2 | 950 | 36 |  | Whole Number Division: Solve; Whole Number Division: Solve (L129) |
| 3 | 5 | Modeling Fraction Division | 2 | 950 | 36 |  | Fraction Division: Solve; Fraction Division: Solve (L134) |
| 3 | 6 | Modeling Fraction Division - Models | 1 | 475 | 18 |  | Fraction Division Models: Use |
| 3 | 7 | Applying Fraction Division | 2 | 950 | 36 |  | Fraction Division: Analyze; Fraction Division: Analyze (L133) |
| 3 | 8 | Applying Fraction Division - Word Problems | 1 | 475 | 18 |  | Fraction Division Word Problems: Solve |
| 4 | 2 | Decimal Addition And Subtraction | 3 | 873 | 42 |  | Decimal Addition: Add; Decimal Subtraction: Subtract; Decimal Addition Subtraction: Add |
| 4 | 3 | Decimal Addition And Subtraction (2) | 1 | 291 | 14 |  | Decimal Addition Subtraction: Subtract |
| 4 | 4 | Decimal Multiplication And Division | 3 | 873 | 42 |  | Decimal Multiplication: Multiply; Decimal Division: Divide; Decimal Multiplication Division: Multiply |
| 4 | 5 | Decimal Multiplication And Division (2) | 1 | 291 | 14 |  | Decimal Multiplication Division: Divide |
| 4 | 6 | Greatest Common Factor Extraction | 3 | 873 | 42 |  | Greatest Common Factor: Identify; Common Factor Extraction: Express; Greatest Common Factor: Identify (L130) |
| 4 | 7 | Greatest Common Factor Extraction - Distributive Property | 1 | 291 | 14 |  | Distributive Property Factoring: Express |
| 4 | 8 | Distributive Property Factoring | 2 | 950 | 36 |  | Distributive Property Factoring: Apply; Distributive Property Factoring: Apply (L131) |
| 4 | 9 | Prime Factorization | 2 | 950 | 36 |  | Prime Factorization: Determine; Prime Factorization: Determine (L127) |
| 5 | 2 | Number Line Opposites | 3 | 873 | 42 |  | Opposite Numbers: Identify; Opposite Numbers: Explain; Opposite Numbers: Identify (L117) |
| 5 | 3 | Number Line Opposites - Opposite Numbers | 1 | 291 | 14 |  | Opposite Numbers: Explain |
| 5 | 4 | Zero In Real Contexts | 3 | 873 | 42 |  | Meaning Of Zero: Explain; Signed Numbers In Context: Explain; Signed Numbers In Context: Explain (L298) |
| 5 | 5 | Properties Of Opposites | 3 | 873 | 42 |  | Opposite Numbers: Recognize; Opposite Numbers: Recognize (L281); Opposite Numbers: Recognize (L282) |
| 5 | 6 | Modeling Signed Quantities | 2 | 582 | 28 |  | Signed Number Representation: Represent; Signed Number Meaning: Represent |
| 5 | 7 | Describing Opposite Directions | 2 | 950 | 36 |  | Signed Number Representation: Use; Signed Number Meaning: Use |
| 5 | 8 | Describing Opposite Directions - Signed Numbers | 1 | 475 | 18 |  | Signed Numbers In Context: Use |
| 5 | 9 | Real-World Signed Numbers | 2 | 950 | 36 |  | Signed Number Representation: Apply; Signed Numbers In Context: Apply |
| 5 | 10 | Real-World Signed Numbers - Context | 1 | 475 | 18 |  | Signed Numbers In Context: Use |
| 6 | 2 | Absolute Value Meaning | 3 | 873 | 42 |  | Absolute Value: Explain; Absolute Value Concept: Explain; Absolute Value Concept: Define |
| 6 | 3 | Absolute Value Calculation | 3 | 873 | 42 |  | Absolute Value: Calculate; Absolute Value Calculation: Calculate; Absolute Value Calculation: Calculate (L292) |
| 6 | 4 | Absolute Value Magnitude | 2 | 582 | 28 |  | Absolute Value Magnitude: Explain; Absolute Value Magnitude: Explain (L294) |
| 6 | 5 | Absolute Value Comparison | 3 | 873 | 42 |  | Absolute Value Comparison: Compare; Absolute Value Comparison: Compare (L106); Absolute Value Vs Order: Distinguish |
| 6 | 6 | Inequality Interpretation | 3 | 873 | 42 |  | Inequality Interpretation: Explain; Inequality Interpretation: Describe; Inequality Interpretation: Identify |
| 6 | 7 | Rational Number Order Statements | 3 | 873 | 42 |  | Rational Number Order Statements: Write; Rational Number Order Statements: Interpret; Rational Number Order Statements: Explain |
| 6 | 8 | Rational Number Comparison | 2 | 766 | 32 |  | Rational Number Comparison: Compare; Rational Number Comparison: Solve |
| 6 | 9 | Rational Number Comparison (2) | 2 | 766 | 32 |  | Rational Number Comparison: Compare; Rational Number Comparison: Solve |
| 6 | 10 | Rational Number Ordering | 2 | 950 | 36 |  | Rational Number Ordering: Order; Rational Number Ordering: Order (L105) |
| 6 | 11 | Absolute Value Applications | 2 | 950 | 36 |  | Absolute Value: Apply; Absolute Value Applications: Apply |
| 7 | 2 | Plotting Numbers And Points | 3 | 873 | 42 |  | Number Line Placement: Position; Number Line Placement: Position (L278); Coordinate Plane Plotting: Position |
| 7 | 3 | Quadrant Identification | 3 | 873 | 42 |  | Quadrant Identification: Identify; Quadrant Identification: Identify (L113); Quadrant Identification: Identify (L283) |
| 7 | 4 | Quadrant Identification (2) | 1 | 291 | 14 |  | Quadrant Identification: Explain |
| 7 | 5 | Identifying Axis Reflections | 3 | 873 | 42 |  | Axis Reflections: Identify; Axis Reflections: Identify (L71); Axis Reflections: Identify (L111) |
| 7 | 6 | Identifying Axis Reflections (2) | 1 | 291 | 14 |  | Axis Reflections: Identify |
| 7 | 7 | Reflection Sign Relationships | 2 | 582 | 28 |  | Axis Reflections: Recognize; Axis Reflections: Describe |
| 7 | 8 | Calculating Coordinate Distances | 3 | 873 | 42 |  | Coordinate Distance: Calculate; Coordinate Distance: Calculate (L115); Coordinate Distance: Calculate (L275) |
| 7 | 9 | Calculating Coordinate Distances - Distance | 1 | 291 | 14 |  | Coordinate Distance: Calculate |
| 7 | 10 | Four Quadrant Graphing | 2 | 950 | 36 |  | Coordinate Plane Graphing: Graph; Graphing Ordered Pairs: Graph |
| 7 | 11 | Four Quadrant Graphing - Coordinate Plane | 1 | 475 | 18 |  | Coordinate Plane Graphing: Graph |
| 7 | 12 | Real-World Distance Problems | 2 | 950 | 36 |  | Coordinate Distance: Solve; Coordinate Distance Applications: Solve |
| 8 | 2 | Statistical Question Basics | 3 | 873 | 42 |  | Statistical Questions: Write; Statistical Questions: Write (L101); Statistical Questions: Identify |
| 8 | 3 | Justifying Statistical Questions | 3 | 873 | 42 |  | Statistical Questions: Write; Statistical Questions: Explain; Statistical Questions: Write (L102) |
| 8 | 4 | Justifying Statistical Questions (2) | 1 | 291 | 14 |  | Statistical Questions: Explain |
| 8 | 5 | Central Tendency Calculations | 3 | 873 | 42 |  | Measures Of Center: Calculate; Measures Of Center: Calculate (L93); Measures Of Center: Recognize |
| 8 | 6 | Central Tendency Calculations - Measures Center | 1 | 291 | 14 |  | Measures Of Center: Calculate |
| 8 | 7 | Choosing Center Measures | 3 | 873 | 42 |  | Measures Of Center: Compare; Measures Of Center: Compare (L94); Measures Of Center: Select |
| 8 | 8 | Center Measures In Context | 2 | 582 | 28 |  | Measures Of Center: Interpret; Measures Of Center: Interpret (L95) |
| 8 | 9 | Variability Measures And Selection | 3 | 873 | 42 |  | Measures Of Variability: Recognize; Measures Of Variability: Calculate; Measures Of Variability: Select |
| 8 | 10 | Spread In Context | 2 | 582 | 28 |  | Data Variability: Interpret; Measures Of Variability: Interpret |
| 8 | 11 | Describing Data Distributions | 2 | 582 | 28 |  | Center And Spread: Describe; Statistical Summaries: Report |
| 9 | 2 | Data Distribution Fundamentals | 3 | 873 | 42 |  | Data Distribution Summary: Describe; Data Distribution: Recognize; Statistical Investigation: Describe |
| 9 | 3 | Center Spread And Shape | 3 | 873 | 42 |  | Distribution Characteristics: Identify; Distribution Characteristics: Identify (L256); Distribution Characteristics: Identify (L257) |
| 9 | 4 | Distribution Shape And Features | 3 | 873 | 42 |  | Distribution Shape: Identify; Data Graph Features: Identify; Distribution Shape: Identify (L98) |
| 9 | 5 | Distribution Shape And Features - Data Graph | 1 | 291 | 14 |  | Data Graph Features: Identify |
| 9 | 6 | Data Context And Patterns | 3 | 873 | 42 |  | Data Context Interpretation: Describe; Data Context Interpretation: Describe (L100); Distribution Patterns: Describe |
| 9 | 7 | Data Context And Patterns - Distribution | 1 | 291 | 14 |  | Distribution Patterns: Identify |
| 9 | 8 | Constructing Data Displays | 1 | 659 | 26 |  | Data Displays: Create |
| 9 | 9 | Constructing Data Displays (2) | 1 | 659 | 26 |  | Data Displays: Create |
| 9 | 10 | Constructing Data Displays (3) | 1 | 659 | 26 |  | Data Displays: Create |
| 10 | 2 | Variables As Unknowns | 2 | 582 | 28 |  | Variable Interpretation: Interpret; Variable Interpretation: Explain |
| 10 | 3 | Naming Expression Parts | 3 | 873 | 42 |  | Expression Vocabulary: Identify; Expression Vocabulary: Identify (L156); Expression Vocabulary: Identify (L157) |
| 10 | 4 | Decoding Expression Structure | 3 | 873 | 42 |  | Expression Vocabulary: Identify; Expression Vocabulary: Identify (L196); Expression Vocabulary: Recognize |
| 10 | 5 | Translating Verbal Expressions | 3 | 873 | 42 |  | Algebraic Expressions: Write; Algebraic Expressions: Write (L162); Writing Expressions: Write |
| 10 | 6 | Translating Verbal Expressions - Writing | 1 | 291 | 14 |  | Writing Expressions: Write |
| 10 | 7 | Evaluating Expressions And Formulas | 2 | 950 | 40 |  | Expression Evaluation: Substitute; Expression Evaluation: Evaluate |
| 10 | 8 | Evaluating Expressions And Formulas - Formula Evaluation | 1 | 659 | 26 |  | Formula Evaluation: Evaluate |
| 11 | 2 | Exponential Expressions Foundations | 3 | 873 | 42 |  | Whole Number Exponents: Write; Exponent Comparison: Compare; Expression Equivalence: Identify |
| 11 | 3 | Exponential Expressions Foundations (2) | 1 | 291 | 14 |  | Exponential Expressions: Write |
| 11 | 4 | Commutative Property Application | 2 | 1134 | 44 |  | Commutative Property: Generate; Commutative Property: Apply |
| 11 | 5 | Associative Property Application | 2 | 1134 | 44 |  | Associative Property: Generate; Associative Property: Apply |
| 11 | 6 | Distributive Property Application | 2 | 1134 | 44 |  | Distributive Property Expressions: Generate; Distributive Property: Apply |
| 11 | 7 | Inverse And Identity Properties | 1 | 659 | 26 |  | Inverse Property: Generate |
| 11 | 8 | Inverse And Identity Properties - Property | 1 | 659 | 26 |  | Identity Property: Generate |
| 11 | 9 | Justifying Expression Equivalence | 2 | 1134 | 44 |  | Expression Equivalence: Determine; Expression Equivalence: Justify |
| 11 | 10 | Evaluating Exponent Expressions | 1 | 659 | 26 |  | Whole Number Exponents: Evaluate |
| 11 | 11 | Evaluating Exponent Expressions (2) | 1 | 659 | 26 |  | Exponent Expressions: Evaluate |
| 11 | 12 | Evaluating Exponent Expressions - Exponential | 1 | 659 | 26 |  | Exponential Expressions: Evaluate |
| 11 | 13 | Absolute Value Exponent Evaluation | 1 | 659 | 26 |  | Absolute Value Expressions: Evaluate |
| 11 | 14 | Absolute Value Exponent Evaluation - Exponents | 1 | 659 | 26 |  | Absolute Value And Exponents: Evaluate |
| 12 | 2 | Understanding Variables | 2 | 766 | 32 |  | Variable Representation: Use; Variable Representation: Explain |
| 12 | 3 | Understanding Variables - Variable Representation | 1 | 291 | 14 |  | Variable Representation: Explain |
| 12 | 4 | Equation And Inequality Meaning | 3 | 873 | 42 |  | Equation Solutions: Interpret; Inequality Solutions: Interpret; Solution Meaning And Testing: Explain |
| 12 | 5 | Writing One-Step Equations | 2 | 582 | 28 |  | One-Step Equations: Write; One-Step Equations: Write (L200) |
| 12 | 6 | Representing Inequality Solutions | 3 | 873 | 42 |  | Inequality Solutions: Represent; Writing Inequalities: Write; Number Line Representation: Represent |
| 12 | 7 | Infinite Solution Sets | 2 | 582 | 28 |  | Inequality Solutions: Explain; Infinite Solutions: Recognize |
| 12 | 8 | Modeling Variable Relationships | 2 | 766 | 32 |  | Dependent Independent Relationships: Write; Variable Representation: Use |
| 12 | 9 | Modeling Variable Relationships - Dependent Independent | 1 | 291 | 14 |  | Dependent Independent Equations: Write |
| 12 | 10 | Solving One-Step Equations | 2 | 950 | 36 |  | One-Step Equations: Solve; One-Step Equations: Solve (L202) |
| 12 | 11 | Testing Solutions By Substitution | 2 | 950 | 36 |  | Equation Solutions: Determine; Inequality Solutions: Determine |
| 12 | 12 | Testing Solutions By Substitution - Solution Meaning | 2 | 950 | 36 |  | Solution Meaning And Testing: Apply; Solution Meaning And Testing: Apply (L205) |
| 12 | 13 | Interpreting Tables And Graphs | 2 | 950 | 36 |  | Relationship Tables: Analyze; Relationship Graphs: Analyze |
| 12 | 14 | Interpreting Tables And Graphs - Relationship Representations | 1 | 291 | 14 |  | Relationship Representations: Relate |
| 12 | 15 | Graphing Relationship Data | 1 | 659 | 26 |  | Dependent Independent Relationships: Create |
| 12 | 16 | Graphing Relationship Data - Dependent Independent | 1 | 659 | 26 |  | Dependent Independent Relationships: Create |
| 13 | 2 | Coordinate Polygon Sides | 3 | 873 | 42 |  | Coordinate Side Length: Calculate; Coordinate Side Length: Calculate (L177); Coordinate Polygons: Draw |
| 13 | 3 | Coordinate Polygon Sides - Side Lengths | 1 | 291 | 14 |  | Coordinate Side Lengths: Calculate |
| 13 | 4 | Coordinate Perimeter And Area | 2 | 582 | 28 |  | Coordinate Perimeter: Calculate; Coordinate Area: Calculate |
| 13 | 5 | Triangle Area Techniques | 2 | 582 | 28 |  | Triangle Area: Calculate; Triangle Area: Calculate (L222) |
| 13 | 6 | Polygon Area Decomposition | 2 | 582 | 28 |  | Quadrilateral Area: Calculate; Polygon Area: Calculate |
| 13 | 7 | Rectangle Missing Vertices | 2 | 950 | 36 |  | Rectangle Missing Vertices: Determine; Rectangle Missing Vertices: Determine (L175) |
| 13 | 8 | Applied Coordinate Geometry | 2 | 950 | 36 |  | Coordinate Geometry Applications: Apply; Composite Area Applications: Apply |
| 14 | 2 | Rectangular Prism Volume | 3 | 873 | 42 |  | Prism Volume: Calculate; Prism Volume: Calculate (L179); Prism Volume: Compare |
| 14 | 3 | Surface Area From Nets | 2 | 582 | 28 |  | Surface Area: Calculate; Surface Area: Calculate (L232) |
| 14 | 4 | Unit Cube Volume Modeling | 2 | 766 | 32 |  | Prism Volume: Calculate; Prism Volume: Demonstrate |
| 14 | 5 | Fractional Prism Volume Applications | 2 | 950 | 36 |  | Prism Volume: Apply; Prism Volume: Apply (L229) |
| 14 | 6 | Fractional Prism Volume Applications (2) | 1 | 475 | 18 |  | Prism Volume Applications: Apply |
| 14 | 7 | Surface Area Applications | 2 | 950 | 36 |  | Surface Area Applications: Apply; Nets Construction: Construct |
| 14 | 8 | Surface Area Applications (2) | 1 | 475 | 18 |  | Surface Area Applications: Apply |
| 14 | 9 | Composite Area Reasoning | 2 | 766 | 32 |  | Area Decomposition: Decompose; Composite Area Applications: Apply |
| 14 | 10 | Advanced Spatial Composition | 1 | 659 | 26 |  | Area Composition: Compose |
| 14 | 11 | Advanced Spatial Composition - Net Construction | 1 | 659 | 26 |  | Net Construction: Create |
| 15 | 2 | Logical Fallacies | 1 | 291 | 14 |  | Logical Fallacies: Identify |
| 15 | 3 | Argument Construction And Inference | 2 | 950 | 36 |  | Logical Argument Construction: Construct; Rules Of Inference: Apply |
| 15 | 4 | Quantifiers And Counterexamples | 2 | 950 | 36 |  | Quantifiers: Apply; Counterexamples: Construct |
| 15 | 5 | Deductive Argument Validity | 1 | 659 | 26 |  | Argument Validity: Evaluate |
| 16 | 2 | Permutations And Combinations | 2 | 582 | 28 |  | Permutations: Calculate; Combinations: Calculate |
| 16 | 3 | Recursive Sequence Foundations | 2 | 582 | 28 |  | Recursive Sequences: Define; Recursive Sequences: Calculate |
| 16 | 4 | Multi-Step Counting Methods | 2 | 950 | 36 |  | Multiplication Principle: Apply; Counting With Repetition: Solve |
| 16 | 5 | Set Counting Strategies | 2 | 950 | 36 |  | Inclusion-Exclusion Principle: Apply; Counting Technique Selection: Analyze |
| 16 | 6 | Fibonacci And Algorithmic Recursion | 2 | 950 | 36 |  | Fibonacci Sequence: Apply; Recursive Algorithms: Implement |
| 16 | 7 | Recursive Growth Modeling | 2 | 950 | 36 |  | Sequence Convergence: Analyze; Recursive Modeling: Model |
| 17 | 2 | Voting Power Indices | 2 | 582 | 28 |  | Voting Power Indices: Calculate; Voting Power Indices: Calculate (L30) |
| 17 | 3 | Apportionment Methods | 1 | 475 | 18 |  | Apportionment Methods: Analyze |
| 17 | 4 | Graph Coloring | 1 | 475 | 18 |  | Graph Coloring: Apply |
| 17 | 5 | Minimum Spanning Tree | 1 | 475 | 18 |  | Minimum Spanning Tree: Implement |
| 17 | 6 | Network Flow | 1 | 475 | 18 |  | Network Flow: Analyze |
| 17 | 7 | Shortest Path Algorithms | 1 | 475 | 18 |  | Shortest Path Algorithms: Apply |
| 17 | 8 | Traveling Salesperson Problem | 1 | 475 | 18 |  | Traveling Salesperson Problem: Solve |
| 17 | 9 | Voting Fairness Criteria | 1 | 475 | 18 |  | Voting Fairness Criteria: Apply |
| 17 | 10 | Voting Methods | 1 | 475 | 18 |  | Voting Methods: Implement |
| 17 | 11 | Network Reliability | 1 | 659 | 26 |  | Network Reliability: Evaluate |
| 17 | 12 | Voting Fairness Criteria (2) | 1 | 659 | 26 |  | Voting Fairness Criteria: Evaluate |
| 18 | 2 | Adjusted Winner Method | 1 | 291 | 14 |  | Adjusted Winner Method: Calculate |
| 18 | 3 | Divider-Chooser Method | 1 | 475 | 18 |  | Divider-Chooser Method: Apply |
| 18 | 4 | Fair Division Algorithm Selection | 1 | 475 | 18 |  | Fair Division Algorithm Selection: Analyze |
| 18 | 5 | Last-Diminisher Method | 1 | 475 | 18 |  | Last-Diminisher Method: Execute |
| 18 | 6 | Lone-Divider Method | 1 | 475 | 18 |  | Lone-Divider Method: Implement |
| 18 | 7 | Fairness Criteria | 1 | 659 | 26 |  | Fairness Criteria: Evaluate |
| 19 | 2 | Number Base Conversion | 1 | 291 | 14 |  | Number Base Conversion: Convert |
| 19 | 3 | Boolean Algebra | 1 | 475 | 18 |  | Boolean Algebra: Apply |
| 19 | 4 | Cryptographic Methods | 1 | 475 | 18 |  | Cryptographic Methods: Apply |
| 19 | 5 | Data Compression | 1 | 475 | 18 |  | Data Compression: Analyze |
| 19 | 6 | Error-Detection Codes | 1 | 475 | 18 |  | Error-Detection Codes: Implement |
| 19 | 7 | Algorithmic Efficiency | 1 | 659 | 26 |  | Algorithmic Efficiency: Evaluate |
| 19 | 8 | Truth Tables | 1 | 659 | 26 |  | Truth Tables: Design |

- Chapters over minute/word limit: **0**

## 4. Pacing

| metric | value |
| --- | --- |
| total_lesson_days | 640 |
| total_chapters | 242 |
| fill ratio | 38% |
| overrun | False |
| overrun days | None |

- Pacing check: total_chapters_in_course=242 is below the lesson-day target range (608-672) for total_lesson_days=640. Course is under-filled.
- Structure check: 18 content parts; all parts >= 4 understand chapters: True.

## 5. LLM calls

| metric | value |
| --- | --- |
| calls | 26 |
| prompt tokens | 1032812 |
| completion tokens | 131677 |
| max single prompt | 79732 |
| tokens per LO | 3881.6 |

| node | calls | prompt tokens |
| --- | --- | --- |
| annotate | 10 | 244024 |
| plan_chapters | 15 | 719082 |
| plan_parts | 1 | 69706 |

| # | role | part/batch | model | prompt | completion | ms | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | annotate |  | claude-sonnet-5 | 25004 | 2590 | 30423 | 1 |
| 2 | annotate |  | claude-sonnet-5 | 24903 | 2406 | 28662 | 1 |
| 3 | annotate |  | claude-sonnet-5 | 24991 | 2627 | 30948 | 1 |
| 4 | annotate |  | claude-sonnet-5 | 25012 | 2531 | 29135 | 1 |
| 5 | annotate |  | claude-sonnet-5 | 24884 | 1088 | 19466 | 1 |
| 6 | annotate |  | claude-sonnet-5 | 23665 | 2614 | 23261 | 1 |
| 7 | annotate |  | claude-sonnet-5 | 23654 | 3533 | 35526 | 1 |
| 8 | annotate |  | claude-sonnet-5 | 23646 | 3177 | 31323 | 1 |
| 9 | annotate |  | claude-sonnet-5 | 24697 | 2307 | 23382 | 1 |
| 10 | annotate |  | claude-sonnet-5 | 23568 | 2440 | 24538 | 1 |
| 11 | plan_parts |  | claude-sonnet-5 | 69706 | 13816 | 107571 | 1 |
| 12 | plan_chapters | P1 | claude-sonnet-5 | 25590 | 11465 | 113242 | 1 |
| 13 | plan_chapters | P2 | claude-sonnet-5 | 53277 | 4060 | 50408 | 1 |
| 14 | plan_chapters | P3 | claude-sonnet-5 | 53244 | 3783 | 44608 | 1 |
| 15 | plan_chapters | P4 | claude-sonnet-5 | 55768 | 6079 | 67950 | 1 |
| 16 | plan_chapters | P5 | claude-sonnet-5 | 60190 | 10306 | 105285 | 1 |
| 17 | plan_chapters | P6 | claude-sonnet-5 | 24171 | 4421 | 46973 | 1 |
| 18 | plan_chapters | P7 | claude-sonnet-5 | 24146 | 5476 | 56111 | 1 |
| 19 | plan_chapters | P8 | claude-sonnet-5 | 54665 | 5953 | 64351 | 1 |
| 20 | plan_chapters | P9 | claude-sonnet-5 | 54073 | 5425 | 56986 | 1 |
| 21 | plan_chapters | P10 | claude-sonnet-5 | 57366 | 8579 | 84716 | 1 |
| 22 | plan_chapters | P11 | claude-sonnet-5 | 24284 | 9489 | 94934 | 1 |
| 23 | plan_chapters | P12 | claude-sonnet-5 | 51801 | 3106 | 32048 | 1 |
| 24 | plan_chapters | P13 | claude-sonnet-5 | 23849 | 8629 | 93270 | 1 |
| 25 | plan_chapters | P14 | claude-sonnet-5 | 76926 | 2281 | 28973 | 1 |
| 26 | plan_chapters | P15 | claude-sonnet-5 | 79732 | 3496 | 36228 | 1 |

## 6. Quality signals

| signal | value |
| --- | --- |
| module titles | 300 |
| distinct titles | 278 |
| avg words per title | 3.62 |
| titles outside 2–5 words | 2 |
| titles with generic words | 0 |
| LO fallbacks by kind | {'titles_fallback': 300, 'plan_chapters_fallback': 25} |
| soft invariant failures | none |
| LLM errors | structured output failed for ChaptersOut: success; structured output failed for ChaptersOut: success; structured output failed for ChaptersOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success; structured output failed for TitlesOut: success |

## 7. Enforcement log

```
FINAL: Part 'Ratios Rates And Percents' - 15 understand chapters OK
FINAL: Part 'Fraction And Whole Number Division' - 7 understand chapters OK
FINAL: Part 'Decimals Factors And Multiples' - 8 understand chapters OK
FINAL: Part 'Integers And Signed Numbers' - 9 understand chapters OK
FINAL: Part 'Absolute Value And Number Comparison' - 10 understand chapters OK
FINAL: Part 'The Cartesian Plane' - 11 understand chapters OK
FINAL: Part 'Statistical Questions And Center Measures' - 10 understand chapters OK
FINAL: Part 'Data Distribution And Summary' - 9 understand chapters OK
FINAL: Part 'Algebraic Terms And Evaluation' - 7 understand chapters OK
FINAL: Part 'Exponents And Equivalent Expressions' - 13 understand chapters OK
FINAL: Part 'Equations Inequalities And Relationships' - 15 understand chapters OK
FINAL: Part 'Coordinate Geometry And Area' - 7 understand chapters OK
FINAL: Part 'Volume And Surface Area' - 10 understand chapters OK
FINAL: Part 'Logical Reasoning And Argumentation' - 4 understand chapters OK
FINAL: Part 'Counting Combinatorics And Recursive Sequences' - 6 understand chapters OK
FINAL: Part 'Graph Theory Voting And Apportionment' - 11 understand chapters OK
FINAL: Part 'Equitable Resource Allocation' - 6 understand chapters OK
FINAL: Part 'Number Systems And Information Theory' - 7 understand chapters OK
```

## 8. Files

- `input.json` — request as received
- `outline.json` — DCIM course outline (response)
- `report.json` — machine-readable metrics
- `enforcement.log` — pack/merge decisions
- `analysis.md` — this file
