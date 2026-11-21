"""Group tests for a1_triage.py (synthetic teaching data only)."""
from a1_triage import decision_counts, gene_summary, impact_counts


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
