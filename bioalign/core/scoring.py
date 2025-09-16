from typing import Callable

def make_delta(match: int = 1, mismatch: int = -1) -> Callable[[str, str], int]:
    def delta(x: str, y: str) -> int:
        return match if x == y else mismatch
    return delta
