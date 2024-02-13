from __future__ import annotations
from dataclasses import asdict, dataclass
from types import ModuleType
from typing import Literal, Optional

ResetableAttribute = Literal["turn_rolls", "turn_score"]
IncrementableAttribute = Literal["round", "turn_rolls", "turn_score"]
Player = ModuleType


@dataclass(frozen=True)
class GameState:
    active: int = 0
    rolls: tuple[int, int] = (0, 0)
    round: int = 0
    scores: tuple[int, int] = (0, 0)
    turn_rolls: int = 0
    turn_score: int = 0
    roll: tuple[int, int] = (0, 0)
    winner: Optional[int] = None


@dataclass(frozen=True)
class TournamentState:
    round: int = 0
    champion: Optional[int] = None

    def update(self, **kwargs) -> TournamentState:
        new_state_as_dict = asdict(self) | kwargs
        return self.__class__(**new_state_as_dict)
