<<<<<<< Updated upstream
"""Group tests for a1_triage.py (synthetic teaching data only)."""
from a1_triage import decision_counts, gene_summary, impact_counts


def make_result(gene="EGFR", depth="20", impact="high", decision="prioritize", variant="v1"):
    """Build one hand-made result dict (as triage() would return), without calling classify_variant."""
=======
"""Group G06 tests for a1_triage.py (synthetic teaching data only).

Boundary tests use OUR thresholds from data/params.json: min_depth = 8, min_quality = 80.
Test numbers match the test plan in docs/design.md section 4.
"""
import copy

import pytest

from a1_triage import (
    build_report,
    classify_variant,
    decision_counts,
    gene_summary,
    impact_counts,
    rank_variants,
    results_to_csv,
    triage,
)

PARAMS = {
    "min_depth": 8,
    "min_quality": 80,
    "priority_genes": ["EGFR", "KRAS", "MYC", "CFTR", "PTEN"],
    "top_k": 8,
}


def make_row(variant="v1", gene="EGFR", depth="30", quality="90", impact="high", pos="100"):
    """One raw variant row as load_variants() gives it (every value is text)."""
>>>>>>> Stashed changes
    return {
        "variant": variant, "gene": gene, "chrom": "7", "pos": pos, "ref": "A", "alt": "G",
        "depth": depth, "quality": quality, "impact": impact,
    }


def make_result(variant="v1", gene="EGFR", depth="30", quality="90", impact="high",
                decision="prioritize", pos="100"):
    """One result dict as triage() returns it, built by hand so each test checks one function."""
    result = make_row(variant, gene, depth, quality, impact, pos)
    result["decision"] = decision
    result["reason"] = "test reason"
    return result


# ---- Member 1: classify_variant and triage ---------------------------------

def test_01_depth_boundary_one_below_at_and_above_min_depth():
    decision, reason = classify_variant(make_row(depth="7"), PARAMS)
    assert decision == "exclude"
    assert "depth" in reason and "7" in reason and "8" in reason
    assert classify_variant(make_row(depth="8"), PARAMS)[0] == "prioritize"
    assert classify_variant(make_row(depth="9"), PARAMS)[0] == "prioritize"


def test_02_quality_boundary_one_below_at_and_above_min_quality():
    decision, reason = classify_variant(make_row(quality="79"), PARAMS)
    assert decision == "exclude"
    assert "quality" in reason and "79" in reason and "80" in reason
    assert classify_variant(make_row(quality="80"), PARAMS)[0] == "prioritize"
    assert classify_variant(make_row(quality="81"), PARAMS)[0] == "prioritize"


def test_03_rules_3_to_6_and_rule_order():
    assert classify_variant(make_row(gene="EGFR", impact="moderate"), PARAMS)[0] == "prioritize"
    assert classify_variant(make_row(gene="EGFR", impact="low"), PARAMS)[0] == "review"
    assert classify_variant(make_row(gene="ATM", impact="high"), PARAMS)[0] == "review"
    assert classify_variant(make_row(gene="ATM", impact="modifier"), PARAMS)[0] == "exclude"
    # depth 1 and quality 1: rule 1 (depth) fires first, not rule 2 (quality)
    decision, reason = classify_variant(make_row(depth="1", quality="1"), PARAMS)
    assert decision == "exclude"
    assert "depth" in reason
    assert "," not in reason


def test_04_messy_text_numbers_and_other_params():
    # ' egfr ' matches EGFR and 'HIGH' matches high; numbers work as well as text
    row = make_row(gene=" egfr ", impact="HIGH")
    row["depth"], row["quality"] = 30, 90
    assert classify_variant(row, PARAMS)[0] == "prioritize"
    # other parameters give other answers: thresholds are read from params, not typed in
    other_params = {"min_depth": 40, "min_quality": 80, "priority_genes": ["TP53"], "top_k": 3}
    assert classify_variant(make_row(depth="30"), other_params)[0] == "exclude"


def test_05_triage_returns_new_dicts_in_order_and_keeps_input():
    rows = [make_row(variant="v1"), make_row(variant="v2", gene="ATM", impact="low")]
    original_rows = copy.deepcopy(rows)
    original_params = copy.deepcopy(PARAMS)
    results = triage(rows, PARAMS)
    assert [result["variant"] for result in results] == ["v1", "v2"]
    assert [result["decision"] for result in results] == ["prioritize", "exclude"]
    assert all("reason" in result for result in results)
    assert rows == original_rows
    assert PARAMS == original_params


# ---- Member 2: decision_counts, impact_counts and gene_summary -------------

def test_06_decision_and_impact_counts_keys_zeros_and_excluded_left_out():
    results = [
        make_result(impact=" HIGH ", decision="prioritize"),
        make_result(impact="low", decision="review"),
        make_result(impact="high", decision="exclude"),
    ]
    assert decision_counts(results) == {"prioritize": 1, "review": 1, "exclude": 1}
    counts = impact_counts(results)
    assert counts == {"high": 1, "moderate": 0, "low": 1, "modifier": 0}
    assert list(counts) == ["high", "moderate", "low", "modifier"]
    assert decision_counts([]) == {"prioritize": 0, "review": 0, "exclude": 0}


def test_07_gene_summary_alphabetical_counts_mean_depth_and_empty():
    # EGFR depths 7, 8, 8 sit around min_depth = 8; the excluded variant still counts in the mean
    results = [
        make_result(gene="PTEN", depth="30", decision="review"),
        make_result(gene="EGFR", depth="7", decision="exclude"),
        make_result(gene="EGFR", depth="8", decision="prioritize"),
        make_result(gene="EGFR", depth="8", decision="review"),
    ]
    summary = gene_summary(results)
    assert list(summary) == ["EGFR", "PTEN"]
    assert summary["EGFR"] == {
        "total": 3, "prioritize": 1, "review": 1, "exclude": 1, "mean_depth": 7.7,
    }
    assert gene_summary([]) == {}


<<<<<<< Updated upstream
def test_summaries_do_not_modify_input():
    results = [make_result(gene="CFTR", impact=" LOW ", decision="review")]
    snapshot = [dict(result) for result in results]
    decision_counts(results)
    impact_counts(results)
    gene_summary(results)
    assert results == snapshot
=======
# ---- Member 3: rank_variants -------------------------------------------------

def test_08_rank_variants_sort_order_and_tie_breaks():
    results = [
        make_result(variant="v1", decision="review", impact="high"),
        make_result(variant="v2", decision="prioritize", impact="moderate"),
        make_result(variant="v3", decision="prioritize", impact="high", quality="85"),
        make_result(variant="v4", decision="prioritize", impact="high", quality="95"),
        make_result(variant="v5", decision="prioritize", impact="high", quality="95", depth="50"),
        make_result(variant="v6", decision="prioritize", impact="high", quality="95", depth="50",
                    pos="9"),
        make_result(variant="v7", decision="exclude", impact="high", quality="100"),
    ]
    ranked = rank_variants(results, len(results))
    assert [record["variant"] for record in ranked] == ["v6", "v5", "v4", "v3", "v2", "v1"]


def test_09_rank_variants_k_zero_k_too_large_and_input_unchanged():
    results = [make_result(variant="v1"), make_result(variant="v2", decision="exclude")]
    original = copy.deepcopy(results)
    assert rank_variants(results, 0) == []
    assert [record["variant"] for record in rank_variants(results, 10)] == ["v1"]
    assert rank_variants([], 3) == []
    assert results == original


def test_10_rank_variants_negative_k_raises_value_error():
    with pytest.raises(ValueError):
        rank_variants([make_result()], -1)


# ---- Member 4: results_to_csv and build_report ------------------------------

def test_11_results_to_csv_header_and_lines():
    csv_text = results_to_csv([make_result(variant="v1"), make_result(variant="v2", gene="KRAS")])
    lines = csv_text.splitlines()
    assert lines[0] == "variant,gene,chrom,pos,depth,quality,impact,decision,reason"
    assert lines[1] == "v1,EGFR,7,100,30,90,high,prioritize,test reason"
    assert lines[2].startswith("v2,KRAS,")
    assert csv_text.endswith("\n")
    assert results_to_csv([]) == "variant,gene,chrom,pos,depth,quality,impact,decision,reason\n"


def test_12_build_report_format_and_top_k_lists_only_qualifying():
    results = [
        make_result(variant="v1", impact="high", decision="prioritize"),
        make_result(variant="v2", impact="low", decision="review"),
        make_result(variant="v3", decision="exclude"),
    ]
    lines = build_report(results, PARAMS).splitlines()
    assert lines[0] == "Variant triage report (synthetic teaching data)"
    assert lines[1] == "Thresholds: min_depth=8 min_quality=80"
    assert lines[2] == "Priority genes: EGFR, KRAS, MYC, CFTR, PTEN"
    assert lines[3:7] == ["Variants: 3", "prioritize: 1", "review: 1", "exclude: 1"]
    assert lines[7] == ""
    assert lines[8] == "Top 8 variants"
    # top_k is 8 but only 2 variants qualify, so only those 2 are listed
    assert lines[9:] == ["1. v1 | EGFR | high | prioritize", "2. v2 | EGFR | low | review"]
>>>>>>> Stashed changes
