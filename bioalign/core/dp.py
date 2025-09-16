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
    # Convention: M has shape (len(S)+1, len(T)+1); rows index S, cols index T
    assert M.shape == (len(S)+1, len(T)+1)
    for i in range(1, len(S)+1):
        for j in range(1, len(T)+1):
            from_up = M[i-1, j] + gap
            from_left = M[i, j-1] + gap
            from_diag = M[i-1, j-1] + delta(S[i-1], T[j-1])
            M[i, j] = max(from_up, from_left, from_diag)

# TODO: implement `free` and `return_cigar`
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

    Returns
    -------
    `AlignResult`
        Custom class containing `score`, `S_aln`, `T_aln`, and optionally `cigar`, `matrix`, and `meta`.
    """
    if mode != "global":
        raise NotImplementedError("Only global NW is currently implemented.")
    if delta is None:
        from .scoring import make_delta
        delta = make_delta()
    if free and mode != "semi-global":
        raise RuntimeError("Parameter `free` can only be used in semi-global mode.")
    
    gap = gap.open
    m, n = len(S), len(T)
    M = np.zeros((m+1, n+1), dtype=np.int32)
    
    # Initialize matrix
    init_global(M, gap)

    # Forward-filling step
    mat_fill_global(M, S, T, gap, delta)

    # Traceback
    S_aln, T_aln = traceback_global(M, S, T, gap, delta)
    score = int(M[m, n])

    result = AlignResult(
        score = score,
        S_aln = S_aln,
        T_aln = T_aln,
        cigar = None,
        matrix = M if return_matrix else None,
        meta = None
    )

    return result