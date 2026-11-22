# Variant Triage Service (SECB3203 Assignment 1)

> Replace the text in this template. The README must let a stranger install, run and test the
> project with the exact commands below. All data are synthetic teaching data, not clinical data.

## Group

- Group ID: G06
- Member 1: MINDY NG YU FANG, A24CS0267, designer and coordinator
- Member 2: ELEANOR TING PIK EN, A24CS0247, summary implementer
- Member 3: WONG ZI NING, A24CS0313, ranking implementer
- Member 4: HUSNA SAFIYYAH BINTI MUHAMMAD FAROUK, A24CS0083, output and testing implementer

## What this project does

The service also ranks non-excluded variants based on decision priority, impact, quality, depth and genomic position, returning the top-k candidates for further review.

<Three or four sentences: what a variant triage service is, what goes in, what comes out.>


## Set up

```
python -m venv .venv
<activate command for your system>
pip install -r requirements.txt
```

## Run

<Write the exact command. The course command is: python src/a1_triage.py data/variants.csv data/params.json results>
<Say which files appear in results/.>

## Test and lint

```
python -m pytest
ruff check src
```

## Our parameters

Our thresholds, priority genes and top_k are in data/params.json (<write the values here>).
They are read at run time and passed to the functions; they are not typed into the rules.

## Design

<Link to docs/design.md and say in two sentences what it contains.>

## Limitations

<At least two honest limitations, for example: rules use depth, quality and impact only; the data are synthetic.>
The ranking process uses predefined decision, impact, quality, depth and position criteria rather than clinical evidence or predictive models. Therefore, ranking results are intended for educational demonstration only and should not be used for clinical decision-making.

## Who did what

| Member | Main contributions | Commits |
|---|---|---|
| <name> | <files or functions> | <number> |
| WONG ZI NING (A24CS0313) | Implemented `rank_variants()` in `src/a1_triage.py`; wrote 11 ranking tests in `tests/test_a1_triage.py`; contributed the ranking test plan and design improvements in `docs/design.md`; assisted with classification fixes and integration review. | 9 |

## AI use

<One sentence: see AI_USE_LOG.md. Say whether the group used AI.>
