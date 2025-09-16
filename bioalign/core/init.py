import numpy as np

def init_global(M: np.ndarray, gap: int) -> None:
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
    M[0, :] = np.arange(0, n+1) * gap
    M[:, 0] = np.arange(0, m+1) * gap