import numpy as np
from .types import ScoreFn, Mode, FreeEnds

def traceback(M: np.ndarray, S: str, T: str, gap: int, delta: ScoreFn, mode: Mode, free: FreeEnds) -> tuple[tuple[str, str], int]:
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
    elif mode == "semi-global":
        # Both ends free -> effectively local alignment
        if free.end_S and free.end_T:
            m, n = np.unravel_index(np.argmax(M), M.shape)
        # Ignore the space after S: need max value in last row of M
        elif free.end_S:
            m = M.shape[0] - 1
            n = np.argmax(M[-1])
        # Ignore the space after T: need max value in last column of M
        elif free.end_T:
            m = np.argmax(M[:, -1])
            n = M.shape[1] - 1
        # Effectively global mode
        else:
            m, n = M.shape[0] - 1, M.shape[1] - 1
    elif mode == "local":
        m, n = np.unravel_index(np.argmax(M), M.shape)
    else:
        raise NotImplementedError("No semi-global in traceback yet.")
    
    # casting to int from np.int64 for clarity
    m, n = int(m), int(n)
    score = int(M[m, n])

    # initializing aligned strings
    S_aln = ""
    T_aln = ""
    if mode == "semi-global":
        # if both ends are free, we're picking the best score in the matrix,
        # so there's no need to fill in gaps before looping
        if free.end_S and free.end_T:
            pass
        elif free.end_S:
            S_aln = "-" * (len(T) - n)
            T_aln = T[n:]
        elif free.end_T:
            S_aln = S[m:]
            T_aln = "-" * (len(S) - m)

    current_score = None
    while m > 0 or n > 0:
        if mode == "semi-global":
            if (free.begin_T and m == 0) or (free.begin_S and n == 0):
                break
        if mode == "local" or (mode == "semi-global" 
                               and current_score is not None 
                               and current_score == 0):
            if M[m, n] == 0:
                break
        if m > 0 and n > 0:
            current_score = M[m, n]

            gap_up_penalty = gap
            if mode == "semi-global" and free.end_T and m >= len(S):
                gap_up_penalty = 0

            gap_left_penalty = gap
            if mode == "semi-global" and free.end_S and n >= len(T):
                gap_left_penalty = 0

            score_up = M[m-1, n] + gap_up_penalty
            score_left = M[m, n-1] + gap_left_penalty
            score_diag = M[m-1, n-1] + delta(S[m-1], T[n-1])

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