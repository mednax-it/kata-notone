from __future__ import annotations
from dataclasses import asdict, dataclass
from types import ModuleType
from typing import Callable, Literal, Optional

ResetableAttribute = Literal["turn_rolls", "turn_score"]
IncrementableAttribute = Literal["round", "turn_rolls", "turn_score"]
GameType = Literal["game", "tournament"]
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


def do_nothing(*args, **kwargs):
    """A placeholder function to be used as a default, do-nothing event
    handler"""


@dataclass
class SignalHandler:
    game_started: Callable = do_nothing
    game_ended: Callable = do_nothing

    round_started: Callable = do_nothing
    round_ended: Callable = do_nothing

    turn_started: Callable = do_nothing
    turn_ended: Callable = do_nothing

    rolled: Callable = do_nothing
    roll_succeeded: Callable = do_nothing
    roll_failed: Callable = do_nothing

    tournament_started: Callable = do_nothing
    tournament_ended: Callable = do_nothing

    tournament_round_started: Callable = do_nothing
    tournament_round_ended: Callable = do_nothing
