# Variant Triage Service (SECB3203 Assignment 1)

All data in this project are **synthetic teaching data**, not clinical data. Nothing here is clinical advice.

## Group

- Group ID: G06
- Member 1: MINDY NG YU FANG, A24CS0267, designer and coordinator
- Member 2: ELEANOR TING PIK EN, A24CS0247, summary implementer
- Member 3: WONG ZI NING, A24CS0313, ranking implementer
- Member 4: HUSNA SAFIYYAH BINTI MUHAMMAD FAROUK, A24CS0083, output and testing implementer

## What this project does

The service also ranks non-excluded variants based on decision priority, impact, quality, depth and genomic position, returning the top-k candidates for further review.

<Three or four sentences: what a variant triage service is, what goes in, what comes out.>
=======
A variant triage service decides which variant calls from a gene panel an analyst should look at
first, which are kept for a second look, and which are set aside. This module reads 50 variant calls
(`data/variants.csv`) and the group's parameters (`data/params.json`), and applies six ordered rules
with named thresholds. Each variant gets a decision (`prioritize`, `review` or `exclude`) and a
recorded reason that names the rule that fired. The module also produces decision counts, impact
counts, a per-gene summary, a ranked top-k list of the variants that were not excluded, a CSV file
and a short text report.

## Set up

Needs Python 3.11 or newer.

```
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate       (macOS / Linux)
pip install -r requirements.txt
```

Only `pytest` and `ruff` are needed to test and lint. The program itself uses the standard library only.

## Run

```
python src/a1_triage.py data/variants.csv data/params.json results
```

This creates the `results/` folder (if needed) and writes two files:

- `results/triage.csv`: one line per variant with `variant,gene,chrom,pos,depth,quality,impact,decision,reason`
- `results/report.txt`: the thresholds, priority genes, decision counts and the top-k ranked variants
  (the report is also printed to the screen)

## Test and lint

```
python -m pytest
ruff check src
```

`tests/test_a1_triage.py` holds our 12 tests, and `tests/test_visible.py` holds the course's visible
tests. Our tests cover normal cases, boundary cases at our own thresholds (depth 7/8/9 and quality
79/80/81), awkward input (messy text, empty lists, k = 0 and k larger than the data) and invalid input
(negative k raises `ValueError`). The test plan is in `docs/design.md` section 4.

## Our parameters

Our thresholds, priority genes and top_k are in `data/params.json`:

| Key | Value | Meaning |
|---|---|---|
| `min_depth` | 8 | depth below 8 is excluded; depth 8 passes |
| `min_quality` | 80 | quality below 80 is excluded; quality 80 passes |
| `priority_genes` | EGFR, KRAS, MYC, CFTR, PTEN | genes the service cares about most |
| `top_k` | 8 | how many variants the report lists |

They are read at run time and passed to the functions as `params`; they are not typed into the rules.
With these values the run gives 15 prioritize, 16 review and 19 exclude.

## Design

[docs/design.md](docs/design.md) contains the design we wrote before coding: a decomposition table,
pseudocode of `classify_variant` showing all six rules, and a hand trace of v1 to v6 plus v9 and v12
with our thresholds. It also holds the 12-case test plan and the group work plan.

## Limitations

- The rules use only depth, quality, gene and impact. They ignore allele frequency, zygosity,
  population data, inheritance and published evidence, so this is not real variant classification,
  which follows published guidelines and trained specialists.
- The data are 50 synthetic variants, so the results say nothing about real patients.
- Fixed cut-offs are blunt: a variant with depth 7 is excluded while depth 8 passes, even though the
  two are almost the same.
- The ranking uses fixed tie-breaks (decision, impact, quality, depth, position), not clinical
  evidence or a predictive model, so the order is for teaching only.
- Input is not validated: a missing column or non-numeric depth, quality or pos stops the program
  with a Python error instead of a friendly message. An impact label outside high, moderate, low and
  modifier falls through to rule 6 or 4.
=======
The ranking process uses predefined decision, impact, quality, depth and position criteria rather than clinical evidence or predictive models. Therefore, ranking results are intended for educational demonstration only and should not be used for clinical decision-making.

## Who did what

Commit counts are non-merge commits under each member's own name, counted on 23 Nov 2026.

| Member | Main contributions | Commits |
|---|---|---|
| MINDY NG YU FANG (A24CS0267) | Implemented `classify_variant()` and `triage()` in `src/a1_triage.py`; wrote the decomposition, pseudocode and hand trace in `docs/design.md`; coordinated the group and set up the repository. | 8 |
| ELEANOR TING PIK EN (A24CS0247) | Implemented `decision_counts()`, `impact_counts()` and `gene_summary()` in `src/a1_triage.py`; wrote the summary tests and the final 12-test suite in `tests/test_a1_triage.py`; wrote the test plan in `docs/design.md` and this README. | 7 |
| WONG ZI NING (A24CS0313) | Implemented `rank_variants()` in `src/a1_triage.py`; wrote the ranking tests; contributed the ranking test plan and design improvements in `docs/design.md`; helped with classification fixes and integration review. | 10 |
| HUSNA SAFIYYAH BINTI MUHAMMAD FAROUK (A24CS0083) | Implemented `results_to_csv()` and `build_report()` in `src/a1_triage.py`; wrote the CSV and report tests. | 2 |
=======
| WONG ZI NING (A24CS0313) | Implemented `rank_variants()` in `src/a1_triage.py`; wrote 11 ranking tests in `tests/test_a1_triage.py`; contributed the ranking test plan and design improvements in `docs/design.md`; assisted with classification fixes and integration review. | 9 |

## AI use

The group used generative AI as a tutor (AI Level 1); every interaction is recorded in
[AI_USE_LOG.md](AI_USE_LOG.md), which every member signs.
