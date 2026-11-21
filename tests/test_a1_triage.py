import pytest
import copy

from src.a1_triage import rank_variants

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

