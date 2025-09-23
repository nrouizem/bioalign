import numpy as np
from typing import Optional
from .types import Mode, FreeEnds

def init(M: np.ndarray, gap: int, mode: Mode, free: Optional[FreeEnds]) -> None:
    """
    Initialize a matrix with correct first row and column for global NW.
    
    Parameters
    ----------
    `M` : np.ndarray
        Zeros matrix.
    `gap` : int
        Gap penalty.
    
    Returns
    -------
    None
    """
    m, n = M.shape[0] - 1, M.shape[1] - 1

    if mode == "global":
        M[0, :] = np.arange(0, n+1) * gap
        M[:, 0] = np.arange(0, m+1) * gap
    elif mode == "semi-global":
        if not free.begin_S:
            M[0, :] = np.arange(0, n+1) * gap
        if not free.begin_T:
            M[:, 0] = np.arange(0, m+1) * gap
    # Local alignment starts with a matrix of 0s
    elif mode == "local":
        pass
    else:
        raise NotImplementedError("The only currently available modes are global, semi-global, and local.")