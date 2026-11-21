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
| v1 | BRCA2 | 9 | 90 | high | 5 | review | Rule 5: BRCA2 is not a priority gene and has high impactt |
| v2 | EGFR | 10 | 90 | high | 3 | prioritize | Rule 3: EGFR is a priority gene and has high impact |
| v3 | KRAS | 11 | 90 | moderate | 3 | prioritize| Rule 3: KRAS is a priority gene and has moderate impact |
| v4 | TP53 | 30 | 79 | high | 2 | exclude | Rule 2: quality 79 is below min_quality 80 |
| v5 | PTEN | 30 | 80 | high | 3 | prioritize | Rule 3: PTEN is a priority gene and has high impact |
| v6 | ATM | 30 | 81 | high | 5 | review | Rule 5: ATM is not a priority gene and has high impact |
| v9 | EGFR | 32 | 100 | low | 4 | review | Rule 4: EGFR is a priority gene and has low impact |
| v12 | RB1 | 33 | 95 | modifier | 6 | exclude | Rule 6: RB1 is not a priority gene and has modifier impact |

## 4. Test plan

Our thresholds: min_depth=8, min_quality=80. Boundaries are inclusive (equal passes).

| # | Type | Function | Input | Expected |
|---|---|---|---|---|
| 1 | Boundary | classify_variant | depth 7 (one below min_depth) | exclude, reason mentions depth 7 and 8 |
| 2 | Boundary | classify_variant | depth 8 (exactly min_depth) | passes the depth rule |
| 3 | Boundary | classify_variant | depth 9 (one above) | passes the depth rule |
| 4 | Boundary | classify_variant | quality 79 (one below min_quality) | exclude, reason mentions quality 79 and 80 |
| 5 | Boundary | classify_variant | quality 80 (exactly min_quality) | passes the quality rule |
| 6 | Boundary | classify_variant | quality 81 (one above) | passes the quality rule |
| 7 | Normal | classify_variant | priority gene + high, non-priority + low, etc. | rules 3 to 6 give prioritize / review / review / exclude |
| 8 | Rule order | classify_variant | depth 1 and quality 1 | exclude for low depth (rule 1 wins) |
| 9 | Awkward | classify_variant | gene ' egfr ', impact 'HIGH' | matches EGFR and high after strip() and casefold() |
| 10 | Normal | triage | two rows | new dicts, same order, input rows unchanged |
| 11 | Normal | decision_counts | 1 prioritize, 2 review, 1 exclude | {prioritize: 1, review: 2, exclude: 1} |
| 12 | Awkward | decision_counts | empty list | all three keys present with 0, in fixed order |
| 13 | Normal | impact_counts | mix with some excluded | excluded variants are not counted |
| 14 | Awkward | impact_counts | impact ' HIGH ' / 'Moderate' | counted as high / moderate; keys in fixed order |
| 15 | Awkward | impact_counts | empty list | all four keys with 0 |
| 16 | Normal | gene_summary | genes PTEN, CFTR, KRAS | keys in alphabetical order CFTR, KRAS, PTEN |
| 17 | Normal | gene_summary | EGFR depths 7, 8, 8 (one excluded) | counts 1/1/1, mean_depth 7.7 (excluded included) |
| 18 | Awkward | gene_summary | gene ' KRAS ', depth given as int | merged under KRAS, mean_depth 9.5 |
| 19 | Awkward | gene_summary | empty list | {} |
| 20 | Normal | rank_variants | mixed results, k = 3 | at most 3, no excluded, sorted with tie-breaks |
| 21 | Awkward | rank_variants | k = 0 and k larger than the data | [] and all candidates |
| 22 | Invalid | rank_variants | k = -1 | raises ValueError (pytest.raises) |
| 23 | Normal | results_to_csv / build_report | small results list | exact header line and report line formats |
| 24 | Side effects | all summary functions | any results | input list is not modified |

**How dictionaries are used for counting and summarising.** decision_counts and impact_counts
first create a dictionary with every allowed key set to 0 (`{key: 0 for key in DECISIONS}`), so the
keys are always present, in a fixed order, even when the count is zero. Each result then adds 1 to
the key for its (cleaned) label. Both functions share one helper, count_labels, so the counting
code is not copied. gene_summary first groups results in a dictionary of lists
(`gene -> [results]`, built with setdefault), then loops over `sorted(...)` gene names so the
output dictionary is in alphabetical order (dicts keep insertion order). Each gene's value is
itself a dictionary: total, the decision counts (reusing decision_counts) and mean_depth, which
is the mean of int(depth) over ALL the gene's variants (excluded ones too), rounded to 1 decimal.

### Ranking tests

| Test case | Expected result |
|---|---|
| Normal ranking | Variants marked `"prioritize"` rank ahead of `"review"` and within the same decision tier, impacts sort in order: `"high"`, `"moderate"`, `"low"`, `"modifier"`. |
| Excluded variants | Any record with `"decision": "exclude"` is filtered out and never appears in the returned list, regardless of its impact or quality. |
| Sorting ties | When decision and impact match, ties are broken by higher `quality` first, then higher `depth` and finally smaller `pos` (using numeric, not string, comparison). |
| Zero `k` | Passing `k = 0` returns an empty list `[]` without raising an error. |
| Large `k` | When `k` exceeds the number of non-excluded records, all eligible sorted records are returned without raising an index error. |
| Negative `k` | Passing a negative integer (e.g., `k = -1`) raises a `ValueError`. |
| Empty results | Passing an empty `results` list (or a list containing only `"exclude"` records) returns an empty list `[]`. |
| Input preservation | The original `results` list and its dictionaries remain unmodified in their initial order after calling `rank_variants()`. |


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