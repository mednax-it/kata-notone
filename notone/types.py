from dataclasses import dataclass
from typing import Literal

ResetableAttribute = Literal["turn_rolls", "turn_score"]


@dataclass
class GameState:
    active: int = 0
    rolls: tuple[int, int] = (0, 0)
    round: int = 0
    scores: tuple[int, int] = (0, 0)
    turn_rolls: int = 0
    turn_score: int = 0
