import pytest
from bioalign import align, GapScheme

def test_local_tiny_match():
    # S='A', T='A' with match=+1, gap=-2
    res = align("A", "A", mode="local", gap=GapScheme.linear(-2))
    assert res.score == 1
    assert res.S_aln == "A"
    assert res.T_aln == "A"

def test_local_tiny_mismatch():
    # S='A', T='T' with match=+1, gap=-2
    res = align("A", "T", mode="local", gap=GapScheme.linear(-2))
    assert res.score == 0
    assert res.S_aln == ""
    assert res.T_aln == ""

def test_local_class_example():
    # S='AGCTGC', T='CTGATGAT' with match=+1, gap=-2
    res = align("AGCTGC", "CTGATGAT", mode="local", gap=GapScheme.linear(-2))
    assert res.score == 3
    assert res.S_aln == "CTG"
    assert res.T_aln == "CTG"

def test_local_class_example2():
    # S='ATAGC', T='TCGC' with match=+1, gap=-2
    res = align("ATAGC", "TCGC", mode="local", gap=GapScheme.linear(-2))
    assert res.score == 2
    assert res.S_aln == "GC"
    assert res.T_aln == "GC"

def test_local_class_example3():
    # S='ATAGC', T='TCGC' with match=+3, gap=-5
    res = align("ATAGC", "TCGC", mode="local", match=3, gap=GapScheme.linear(-5))
    assert res.score == 8
    assert res.S_aln == "TAGC"
    assert res.T_aln == "TCGC"