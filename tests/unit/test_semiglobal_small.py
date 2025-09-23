import pytest
from bioalign import align, GapScheme, FreeEnds


def test_semiglobal_matches_global_without_free_ends():
    res = align("AC", "AC", mode="semi-global", gap=GapScheme.linear(-2), free=FreeEnds())
    assert res.score == 2
    assert res.S_aln == "AC"
    assert res.T_aln == "AC"


def test_semiglobal_free_begin_trims_prefix_of_S():
    free = FreeEnds(begin_S=True, begin_T=True)
    res = align("GGAC", "AC", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 2
    assert res.S_aln == "AC"
    assert res.T_aln == "AC"


def test_semiglobal_free_begin_trims_prefix_of_T():
    free = FreeEnds(begin_S=True, begin_T=True)
    res = align("AC", "GGAC", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 2
    assert res.S_aln == "AC"
    assert res.T_aln == "AC"


def test_semiglobal_free_end_trims_suffix_of_S():
    free = FreeEnds(end_T=True)
    res = align("ACGG", "AC", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 2
    assert res.S_aln == "ACGG"
    assert res.T_aln == "AC--"


def test_semiglobal_free_end_trims_suffix_of_T():
    free = FreeEnds(end_S=True)
    res = align("AC", "ACGG", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 2
    assert res.S_aln == "AC--"
    assert res.T_aln == "ACGG"


def test_semiglobal_free_both_ends_finds_best_substring():
    free = FreeEnds(begin_S=True, begin_T=True, end_S=True, end_T=True)
    res = align("TAGC", "GGAC", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 1
    assert res.S_aln == "G"
    assert res.T_aln == "G"


def test_semiglobal_class_example():
    free = FreeEnds(end_T=True)
    res = align("TCACG", "TC", mode="semi-global", gap=GapScheme.linear(-3), free=free)
    assert res.score == 2
    assert res.S_aln == "TCACG"
    assert res.T_aln == "TC---"

def test_semiglobal_class_ignore_endS():
    free = FreeEnds(end_S=True)
    res = align("AC", "ACTC", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 2
    assert res.S_aln == "AC--"
    assert res.T_aln == "ACTC"

def test_semiglobal_class_ignore_endT():
    free = FreeEnds(end_T=True)
    res = align("ATGAC", "AC", mode="semi-global", gap=GapScheme.linear(-2), free=free)
    assert res.score == 0
    assert res.S_aln == "ATGAC"
    assert res.T_aln == "AC---"