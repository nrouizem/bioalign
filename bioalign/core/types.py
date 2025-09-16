from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Literal, Optional, Dict, Any

Mode = Literal["global", "local", "semi-global"]

@dataclass(frozen=True)
class GapScheme:
    open: int
    extend: int  # for linear gaps in v0, keep open == extend

    @classmethod
    def linear(cls, g: int) -> "GapScheme":
        return cls(open=g, extend=g)

@dataclass(frozen=True)
class FreeEnds:
    begin_S: bool = False
    begin_T: bool = False
    end_S: bool = False
    end_T: bool = False

ScoreFn = Callable[[str, str], int]

@dataclass
class AlignResult:
    score: int
    S_aln: str
    T_aln: str
    cigar: Optional[str] = None
    matrix: Optional["np.ndarray"] = None  # type: ignore[name-defined]
    meta: Optional[Dict[str, Any]] = None
