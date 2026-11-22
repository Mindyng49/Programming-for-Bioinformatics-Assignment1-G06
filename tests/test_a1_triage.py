import copy
import pytest

from a1_triage import decision_counts, gene_summary, impact_counts, rank_variants

def test_rank_variants_decision_priority():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "high",
            "quality": "100",
            "depth": "50",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "prioritize",
            "impact": "high",
            "quality": "80",
            "depth": "20",
            "pos": "200",
        },
    ]

    ranked = rank_variants(results, 2)

    assert ranked[0]["variant"] == "v2"
    assert ranked[1]["variant"] == "v1"


def test_rank_variants_impact_priority():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "low",
            "quality": "90",
            "depth": "30",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "review",
            "impact": "modifier",
            "quality": "95",
            "depth": "30",
            "pos": "200",
        },
        {
            "variant": "v3",
            "decision": "review",
            "impact": "high",
            "quality": "80",
            "depth": "30",
            "pos": "300",
        },
        {
            "variant": "v4",
            "decision": "review",
            "impact": "moderate",
            "quality": "85",
            "depth": "30",
            "pos": "400",
        },
    ]

    ranked = rank_variants(results, 4)
    variant_ids = [record["variant"] for record in ranked]

    assert variant_ids == ["v3", "v4", "v1", "v2"]


def test_rank_variants_quality_priority():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "high",
            "quality": "80",
            "depth": "50",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "review",
            "impact": "high",
            "quality": "95",
            "depth": "20",
            "pos": "200",
        },
        {
            "variant": "v3",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "40",
            "pos": "300",
        },
    ]

    ranked = rank_variants(results, 3)
    variant_ids = [record["variant"] for record in ranked]

    assert variant_ids == ["v2", "v3", "v1"]


def test_rank_variants_depth_priority():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "20",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "50",
            "pos": "300",
        },
        {
            "variant": "v3",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "35",
            "pos": "200",
        },
    ]

    ranked = rank_variants(results, 3)
    variant_ids = [record["variant"] for record in ranked]

    assert variant_ids == ["v2", "v3", "v1"]


def test_rank_variants_position_priority():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "30",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "30",
            "pos": "20",
        },
        {
            "variant": "v3",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "30",
            "pos": "9",
        },
    ]

    ranked = rank_variants(results, 3)
    variant_ids = [record["variant"] for record in ranked]

    assert variant_ids == ["v3", "v2", "v1"]


def test_rank_variants_excludes_variants():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "30",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "exclude",
            "impact": "high",
            "quality": "100",
            "depth": "50",
            "pos": "200",
        },
        {
            "variant": "v3",
            "decision": "prioritize",
            "impact": "moderate",
            "quality": "85",
            "depth": "25",
            "pos": "300",
        },
    ]

    ranked = rank_variants(results, 3)
    variant_ids = [record["variant"] for record in ranked]

    assert variant_ids == ["v3", "v1"]


def test_rank_variants_zero_k():
    results = [
        {
            "variant": "v1",
            "decision": "prioritize",
            "impact": "high",
            "quality": "90",
            "depth": "30",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "review",
            "impact": "moderate",
            "quality": "85",
            "depth": "25",
            "pos": "200",
        },
    ]

    ranked = rank_variants(results, 0)

    assert ranked == []


def test_rank_variants_large_k():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "moderate",
            "quality": "85",
            "depth": "30",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "prioritize",
            "impact": "high",
            "quality": "90",
            "depth": "40",
            "pos": "200",
        },
        {
            "variant": "v3",
            "decision": "exclude",
            "impact": "high",
            "quality": "100",
            "depth": "50",
            "pos": "300",
        },
    ]

    ranked = rank_variants(results, 10)
    variant_ids = [record["variant"] for record in ranked]

    assert variant_ids == ["v2", "v1"]


def test_rank_variants_negative_k():
    with pytest.raises(ValueError):
        rank_variants([], -1)


def test_rank_variants_empty_results():
    assert rank_variants([], 3) == []


def test_rank_variants_input_preservation():
    results = [
        {
            "variant": "v1",
            "decision": "review",
            "impact": "high",
            "quality": "90",
            "depth": "30",
            "pos": "100",
        },
        {
            "variant": "v2",
            "decision": "prioritize",
            "impact": "moderate",
            "quality": "85",
            "depth": "40",
            "pos": "200",
        },
    ]

    original_results = copy.deepcopy(results)
    ranked = rank_variants(results, 2)
    variant_ids = [record["variant"] for record in ranked]

    assert results == original_results
    assert variant_ids == ["v2", "v1"]

"""Group tests for a1_triage.py (synthetic teaching data only)."""

def make_result(gene="EGFR", depth="20", impact="high", decision="prioritize", variant="v1"):
    """Build one hand-made result dict (as triage() would return), without calling classify_variant."""
    return {
        "variant": variant, "gene": gene, "chrom": "chr1", "pos": "100", "ref": "A", "alt": "G",
        "depth": depth, "quality": "90", "impact": impact, "decision": decision, "reason": "test",
    }


# ---- decision_counts -------------------------------------------------------

def test_decision_counts_normal():
    results = [
        make_result(decision="prioritize"),
        make_result(decision="review"),
        make_result(decision="review"),
        make_result(decision="exclude"),
    ]
    assert decision_counts(results) == {"prioritize": 1, "review": 2, "exclude": 1}


def test_decision_counts_empty_list_has_all_keys_in_order():
    counts = decision_counts([])
    assert counts == {"prioritize": 0, "review": 0, "exclude": 0}
    assert list(counts) == ["prioritize", "review", "exclude"]


# ---- impact_counts ---------------------------------------------------------

def test_impact_counts_leaves_out_excluded():
    results = [
        make_result(impact="high", decision="prioritize"),
        make_result(impact="low", decision="review"),
        make_result(impact="high", decision="exclude"),
        make_result(impact="modifier", decision="exclude"),
    ]
    assert impact_counts(results) == {"high": 1, "moderate": 0, "low": 1, "modifier": 0}


def test_impact_counts_messy_text_and_key_order():
    results = [make_result(impact=" HIGH "), make_result(impact="Moderate", decision="review")]
    counts = impact_counts(results)
    assert counts == {"high": 1, "moderate": 1, "low": 0, "modifier": 0}
    assert list(counts) == ["high", "moderate", "low", "modifier"]


def test_impact_counts_empty_list_gives_zeros():
    assert impact_counts([]) == {"high": 0, "moderate": 0, "low": 0, "modifier": 0}


# ---- gene_summary ----------------------------------------------------------

def test_gene_summary_genes_alphabetical():
    results = [make_result(gene="PTEN"), make_result(gene="CFTR"), make_result(gene="KRAS")]
    assert list(gene_summary(results)) == ["CFTR", "KRAS", "PTEN"]


def test_gene_summary_counts_and_mean_depth_include_excluded():
    # Depths 7, 8, 8 sit around our min_depth = 8; the excluded depth-7 variant still counts.
    results = [
        make_result(gene="EGFR", depth="7", decision="exclude"),
        make_result(gene="EGFR", depth="8", decision="prioritize"),
        make_result(gene="EGFR", depth="8", decision="review"),
        make_result(gene="MYC", depth="30", decision="review"),
    ]
    summary = gene_summary(results)
    assert summary["EGFR"] == {
        "total": 3, "prioritize": 1, "review": 1, "exclude": 1, "mean_depth": 7.7,
    }
    assert summary["MYC"] == {"total": 1, "prioritize": 0, "review": 1, "exclude": 0, "mean_depth": 30.0}
    assert list(summary["EGFR"]) == ["total", "prioritize", "review", "exclude", "mean_depth"]


def test_gene_summary_accepts_numbers_and_strips_gene():
    results = [make_result(gene=" KRAS ", depth=9), make_result(gene="KRAS", depth=10)]
    assert gene_summary(results) == {
        "KRAS": {"total": 2, "prioritize": 2, "review": 0, "exclude": 0, "mean_depth": 9.5},
    }


def test_gene_summary_empty_list():
    assert gene_summary([]) == {}


def test_summaries_do_not_modify_input():
    results = [make_result(gene="CFTR", impact=" LOW ", decision="review")]
    snapshot = [dict(result) for result in results]
    decision_counts(results)
    impact_counts(results)
    gene_summary(results)
    assert results == snapshot
