from __future__ import annotations
import numpy as np
from typing import Optional
from .types import AlignResult, GapScheme, FreeEnds, Mode, ScoreFn
from .init import init_global
from .traceback import traceback_global

def mat_fill_global(M: np.ndarray, S: str, T: str, gap: int, delta: ScoreFn):
    """
    Forward matrix-filling step.

    Parameters
    ----------
    `M` : np.ndarray
        Initialized alignment matrix.
    `S` : str
        First string to align.
    `T` : str
        Second string to align.
    `gap` : int
        Gap penalty.
    `delta` : `ScoreFn`
        Scoring function for matches and mismatches.

    Returns
    -------
    None
    """
    for m in range(1, len(S)+1):
        for n in range(1, len(T)+1):
            from_up = M[m-1, n] + gap
            from_left = M[m, n-1] + gap
            from_diag = M[m-1, n-1] + delta(S[m-1], T[n-1])
            M[m, n] = max(from_up, from_left, from_diag)

def align(
        S: str,
        T: str,
        mode: Mode = "global",
        gap: GapScheme = GapScheme.linear(-2),
        free: Optional[FreeEnds] = None,
        delta: Optional[ScoreFn] = None,
        return_matrix: bool = False,
        return_cigar: bool = False,
) -> AlignResult:
    """
    Functional alignment API (v0: global only).
    """
    if mode != "global":
        raise NotImplementedError("Only global NW is currently implemented.")
    if delta is None:
        from .scoring import make_delta
        delta = make_delta()
    
    gap = gap.open
    m, n = len(S), len(T)
    M = np.zeros((m+1, n+1), dtype=np.int32)
    
    # Initialize matrix
    init_global(M, gap)

    # Forward-filling step
    mat_fill_global(M, S, T, gap, delta)

    # Traceback
    S_aln, T_aln = traceback_global(M, S, T, gap, delta)
    score = M[m, n]

    result = AlignResult(
        score = score,
        S_aln = S_aln,
        T_aln = T_aln,
        cigar = None,
        matrix = M if return_matrix else None,
        meta = None
    )

    return result