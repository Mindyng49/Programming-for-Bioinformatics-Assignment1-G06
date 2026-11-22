# Design - Variant Triage Service

Write this BEFORE you write the code, then keep it up to date. It is marked by the lecturer.
Use your own words, your own thresholds and your own data. Delete the guidance in italics.

Group ID: G06     
Thresholds from data/params.json: min_depth = 8, min_quality = 80, top_k = 8, priority_genes = EGFR, KRAS, MYC, CFTR, PTEN

## 1. Decomposition

| Question | Our answer |
|---|---|
| Input | 50 synthetic variants from CSV and parameters from JSON | 
| Output | Decisions, reasons, summaries, ranking, CSV and text report |
| Constraints (named thresholds, what happens at exactly the threshold) | Named thresholds, inclusive boundaries, correct rule order, unchanged input |
| Rule order and why the order matters | Six rules, starting with depth and ending with impact or gene classification |
| Out of scope | Real patient data, clinical diagnosis and actual clinical decision-making |

## 2. Pseudocode or flowchart of classify_variant


```text
START

INPUT row and params

GET depth and quality
GET gene and impact
GET minimum thresholds
GET priority genes

Rule 1:
IF depth is below min_depth
     exclude variant
     return decision and reason
Rule 2:
ELSE IF quality is below min_quality
     exclude variant
     return decision and reason
Rule 3:
ELSE IF gene is a priority gene AND impact is high or moderate
     prioritize variant
     return decision and reason
Rule 4:
ELSE IF gene is a priority gene AND impact is low or modifier
     review variant
     return decision and reason
Rule 5:
ELSE IF gene is not a priority gene AND impact is high or moderate
     review variant
     return decision and reason
Rule 6:
ELSE
     exclude variant
     return decision and reason

END

```

## 3. Hand trace

| Variant | Gene | Depth | Quality | Impact | Rule that fires | Decision | Reason |
|---|---|---|---|---|---|---|---|
| v1 | BRCA2 | 9 | 90 | high | 5 | review | Rule 5: non-priority gene BRCA2 has high impact |
| v2 | EGFR | 10 | 90 | high | 3 | prioritize | Rule 3: priority gene EGFR has high impact |
| v3 | KRAS | 11 | 90 | moderate | 3 | prioritize | Rule 3: priority gene KRAS has moderate impact |
| v4 | TP53 | 30 | 79 | high | 2 | exclude | Rule 2: quality 79 is below min_quality 80 |
| v5 | PTEN | 30 | 80 | high | 3 | prioritize | Rule 3: priority gene PTEN has high impact |
| v6 | ATM | 30 | 81 | high | 5 | review | Rule 5: non-priority gene ATM has high impact |
| v9 | EGFR | 32 | 100 | low | 4 | review | Rule 4: priority gene EGFR has low impact |
| v12 | RB1 | 33 | 95 | modifier | 6 | exclude | Rule 6: non-priority gene RB1 has modifier impact |

## 4. Test plan

Our thresholds: `min_depth = 8`, `min_quality = 80`. Boundaries are inclusive: a value equal to the
threshold passes. The 12 tests below are in `tests/test_a1_triage.py` (same numbers). Each test checks
one requirement of the brief; together they cover normal, boundary, awkward and invalid input for every
function. The hand trace in section 3 was checked against `results/triage.csv`: all 8 rows match.

| # | Owner | Type | Function | Input | Expected |
|---|---|---|---|---|---|
| 1 | M1 | Boundary | classify_variant | depth 7 / 8 / 9 (one below, at, one above min_depth) | 7 is excluded, and the reason names depth, 7 and 8; 8 and 9 pass |
| 2 | M1 | Boundary | classify_variant | quality 79 / 80 / 81 (one below, at, one above min_quality) | 79 is excluded, and the reason names quality, 79 and 80; 80 and 81 pass |
| 3 | M1 | Normal | classify_variant | priority + moderate, priority + low, other + high, other + modifier; and depth 1 with quality 1 | prioritize / review / review / exclude; depth 1 and quality 1 gives a depth reason (rule order); no comma in the reason |
| 4 | M1 | Awkward | classify_variant | gene `' egfr '`, impact `'HIGH'`, depth and quality given as numbers; other params (min_depth 40, gene TP53) | matches EGFR and high; other params give a different answer (exclude), so nothing is hard-coded |
| 5 | M1 | Normal | triage | two rows | new dicts with decision and reason, same order; input rows and params unchanged |
| 6 | M2 | Normal + awkward | decision_counts, impact_counts | prioritize (impact `' HIGH '`), review (low), exclude (high); empty list | {1, 1, 1}; impacts {high 1, moderate 0, low 1, modifier 0} with the excluded variant left out, keys in fixed order; empty list gives all zeros |
| 7 | M2 | Normal + awkward | gene_summary | PTEN, then EGFR with depths 7, 8, 8 (one excluded); empty list | genes in alphabetical order EGFR, PTEN; EGFR total 3, 1/1/1, mean_depth 7.7 (the excluded variant still counts); empty list gives {} |
| 8 | M3 | Normal | rank_variants | variants that tie on decision, impact, quality and depth in turn, plus one excluded variant | order v6, v5, v4, v3, v2, v1: prioritize before review, then high before moderate, higher quality, higher depth, smaller pos; excluded variant never listed |
| 9 | M3 | Awkward | rank_variants | k = 0; k = 10 with 1 candidate; empty list | []; only the 1 candidate; []; the input list is not changed |
| 10 | M3 | Invalid | rank_variants | k = -1 | raises ValueError (`pytest.raises`) |
| 11 | M4 | Normal + awkward | results_to_csv | two results; empty list | header line exactly as specified, one line per result in order, ends with a newline; empty list gives only the header |
| 12 | M4 | Normal + awkward | build_report | 3 results (one excluded), top_k 8 | title, Thresholds, Priority genes, Variants and count lines in the fixed format, a blank line, `Top 8 variants`, then only the 2 qualifying variants |

**How dictionaries are used for counting and summarising.** decision_counts and impact_counts
first create a dictionary with every allowed key set to 0 (`{key: 0 for key in DECISIONS}`), so the
keys are always present, in a fixed order, even when the count is zero. Each result then adds 1 to
<<<<<<< Updated upstream
the key for its (cleaned) label. Both functions share one helper, count_labels, so the counting
code is not copied. gene_summary first groups results in a dictionary of lists
(`gene -> [results]`, built with setdefault), then loops over `sorted(...)` gene names so the
output dictionary is in alphabetical order (dicts keep insertion order). Each gene's value is
itself a dictionary: total, the decision counts (reusing decision_counts) and mean_depth, which
is the mean of int(depth) over ALL the gene's variants (excluded ones too), rounded to 1 decimal.
=======
the key for its cleaned label (`strip()` and `casefold()`). Both functions share one helper,
count_labels, so the counting code is not copied. gene_summary first groups results in a dictionary
of lists (`gene -> [results]`, built with setdefault), then loops over `sorted(...)` gene names so the
output dictionary is in alphabetical order (dicts keep insertion order). Each gene's value is itself
a dictionary: total, the decision counts (reusing decision_counts) and mean_depth, which is the mean
of int(depth) over ALL the gene's variants (excluded ones too), rounded to 1 decimal.
>>>>>>> Stashed changes

## 5. Work plan

- Member 1 (Mindy): Responsible for  implementing classify_variant() and triage()
- Member 2 (Eleanor): Responsible for implementing decision_counts(), impact_counts() and gene_summary(), together with related tests.
- Member 3 (Zi Ning): Responsible for implementing rank_variants(), preparing the ranking pseudocode and developing ranking tests.
- Member 4 (Husna): Responsible for implementing results_to_csv() and build_report(), testing output functions 

- Order of Implementation
- 1. Complete the design in docs/design.md before coding: All members finalize function signatures, input/output formats, and edge-case rules together so every module connects cleanly.
- 2. Each member implements their assigned functions: Following the build order above, members develop their assigned functions according to docs/design.md.
- 3. Each member writes tests for their functions: Each member writes unit tests covering normal inputs, boundary cases, and invalid data for their own functions.
- 4. Combine all functions into the main project: Once individual functions pass local tests, all branches are merged into main to connect the full pipeline.
- 5. Run the tests and fix errors: All members run the complete test suite on the integrated codebase to catch integration issues and fix any remaining bugs.

- Code Review
- Cross-member review before merging: Every pull request is reviewed by at least one other member before being merged into main.
- Check assignment requirements: Reviewers verify that function names, parameters, return types, and logic strictly match docs/design.md and the assignment specifications.
- Check function outputs and edge cases: Reviewers test how functions handle empty lists, ties, missing fields, and unexpected inputs.
- Give feedback and correct errors together: Reviewers leave clear comments on pull requests, and the group collaborates to fix issues before approving the merge.

- Git and Final Checking
- Personal Git identity: Each member commits their own work using their own configured Git username and email.
- Feature branches and pull requests: Members push their work to separate feature branches and open pull requests rather than committing directly to main.
- Group review before merging: Pull requests are checked and approved by the team before merging into main.
- Final project verification: After all code is merged into main, all members run pytest to confirm all tests pass and ruff check src to ensure there are no linting or formatting errors.