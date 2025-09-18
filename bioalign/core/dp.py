from __future__ import annotations
import numpy as np
from typing import Optional
from .types import AlignResult, GapScheme, FreeEnds, Mode, ScoreFn
from .init import init
from .traceback import traceback

def mat_fill(M: np.ndarray, S: str, T: str, gap: int, delta: ScoreFn, mode: Mode):
    """
    In-place forward matrix-filling step.

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
            if mode == "local":
                M[i, j] = max(from_up, from_left, from_diag, 0)
            else:
                M[i, j] = max(from_up, from_left, from_diag)

# TODO: implement `free` and `return_cigar`
# TODO: add match + mismatch score args
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
    Functional alignment API (v0: global and local only).

    Returns
    -------
    `AlignResult`
        Custom class containing `score`, `S_aln`, `T_aln`, and optionally `cigar`, `matrix`, and `meta`.
    """
    if mode not in ["global", "local"]:
        raise NotImplementedError(f"Mode {mode} has not been implemented.")
    if delta is None:
        from .scoring import make_delta
        delta = make_delta()
    if free and mode != "semi-global":
        raise RuntimeError("Parameter `free` can only be used in semi-global mode.")
    
    gap = gap.open
    m, n = len(S), len(T)
    M = np.zeros((m+1, n+1), dtype=np.int32)
    
    # Initialize matrix
    init(M, gap, mode, free)

    # Forward-filling step
    mat_fill(M, S, T, gap, delta, mode)

    # Traceback
    (S_aln, T_aln), score = traceback(M, S, T, gap, delta, mode)

    result = AlignResult(
        score = score,
        S_aln = S_aln,
        T_aln = T_aln,
        cigar = None,
        matrix = M if return_matrix else None,
        meta = None
    )

    return result