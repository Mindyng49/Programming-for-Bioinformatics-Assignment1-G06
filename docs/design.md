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

START
INPUT row and params
GET depth and quality
GET gene and impact
GET minimum thresholds
GET priority genes
Rule 1 IF depth is below min_depth
     exclude variant
     return decision and reason
Rule 2 ELSE IF quality is below min_quality
     exclude variant
     return decision and reason
Rule 3 ELSE IF gene is a priority gene AND impact is high or moderate
     prioritize variant
     return decision and reason
Rule 4 ELSE IF gene is a priority gene AND impact is low or modifier
     review variant
     return decision and reason
Rule 5 ELSE IF gene is not a priority gene AND impact is high or moderate
     review variant
     return decision and reason
Rule 6 ELSE
     exclude variant
     return decision and reason
END

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

*List the cases you will test: normal, boundary (exactly at YOUR thresholds, one below, one above), invalid or
awkward input (empty list, k = 0, k larger than the data, messy text). One line per case.*

## 5. Work plan

*Who builds which function, in which order, and how you will review each other's code.*
