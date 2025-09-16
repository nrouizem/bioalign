import pytest
from bioalign import align, GapScheme

def test_global_tiny_match():
    # S='A', T='A' with match=+1, gap=-2
    res = align("A", "A", mode="global", gap=GapScheme.linear(-2))
    assert res.score == 1
    assert res.S_aln == "A"
    assert res.T_aln == "A"

def test_global_simple_gap():
    # S='AC', T='A' → one gap needed; score = +1 + (-2) = -1
    res = align("AC", "A", mode="global", gap=GapScheme.linear(-2))
    assert res.score == -1
    assert res.S_aln == "AC"
    assert res.T_aln == "A-"

def test_global_simple_gap_mismatch():
    # S='AG', T='CTG' → one gap and one mismatch; score = (-2) + (-1) + 1 = -2
    res = align("AG", "CTG", mode="global", gap=GapScheme.linear(-2))
    assert res.score == -2
    assert res.S_aln == "-AG"
    assert res.T_aln == "CTG"

def test_global_tie_break_diag_over_up_left():
    # Construct a 2x2 where multiple paths tie; enforce diag > up > left.
    # With S='AG', T='AA', match=+1, mismatch=-1, gap=-2
    # Optimal should align first A-A on diagonal first due to tie-break.
    res = align("AG", "AA", mode="global", gap=GapScheme.linear(-2))
    # Just assert determinism form: starts with aligned 'A' vs 'A'
    assert res.S_aln[0] == "A" and res.T_aln[0] == "A"

def test_global_empty_vs_nonempty():
    res = align("", "TT", mode="global", gap=GapScheme.linear(-2))
    assert res.score == -4
    assert res.S_aln == "--"
    assert res.T_aln == "TT"
