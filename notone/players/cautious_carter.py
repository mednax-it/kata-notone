"""Cautious Carter takes an cautious-but-naive approach, only rolling 3
times."""

from notone.schema import GameState


def name() -> str:
    return "Cautious Carter"


def emoji() -> str:
    return "😳"


def victory_cry() -> str:
    return "Oh I won? That's good, right?"


def roll_again(state: GameState) -> bool:
    return state.turn_rolls < 1
