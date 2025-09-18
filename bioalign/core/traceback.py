import numpy as np
from .types import ScoreFn, Mode

def traceback(M: np.ndarray, S: str, T: str, gap: int, delta: ScoreFn, mode: Mode) -> tuple[tuple[str, str], int]:
    """
    NW traceback step.

    Parameters
    ----------
    `M` : np.ndarray
        Forward-filled alignment matrix.
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
    `(str, str)`
        2-tuple of aligned sequences.
    `int`
        Alignment score.
    """
    # Convention: M has shape (len(S)+1, len(T)+1); rows index S, cols index T
    if mode == "global":
        m, n = M.shape[0] - 1, M.shape[1] - 1
    elif mode == "local":
        m, n = np.unravel_index(np.argmax(M), M.shape)
    else:
        raise NotImplementedError("No semi-global in traceback yet.")
    S_aln = ""
    T_aln = ""
    score = int(M[m, n])

    while m > 0 or n > 0:
        if mode == "local":
            if M[m, n] == 0:
                break
        if m > 0 and n > 0:
            current_score = M[m, n]
            score_diag = M[m-1, n-1] + delta(S[m-1], T[n-1])
            score_up = M[m-1, n] + gap
            score_left = M[m, n-1] + gap

            # Use deterministic tie-breaking: diag > up > left
            if current_score == score_diag:
                S_aln = S[m-1] + S_aln
                T_aln = T[n-1] + T_aln
                m -= 1
                n -= 1
            elif current_score == score_up:
                S_aln = S[m-1] + S_aln
                T_aln = "-" + T_aln
                m -= 1
            elif current_score == score_left:
                S_aln = "-" + S_aln
                T_aln = T[n-1] + T_aln
                n -= 1
            else:
                raise RuntimeError(f"Traceback error at ({m}, {n}). Score: {current_score}. Parents (D,U,L): {score_diag}, {score_up}, {score_left}")
            
        elif m > 0:
            S_aln = S[m-1] + S_aln
            T_aln = "-" + T_aln
            m -= 1
        else:
            S_aln = "-" + S_aln
            T_aln = T[n-1] + T_aln
            n -= 1
    
    if len(S_aln) != len(T_aln):
            raise RuntimeError("Aligned sequences aren't the same length; something went wrong.")
    
    return (S_aln, T_aln), score