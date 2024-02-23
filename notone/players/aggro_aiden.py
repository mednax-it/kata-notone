"""Aggro Aiden takes an aggressive-but-naive approach, rolling until their
turn score is over 40."""

from notone.schema import GameState


def name() -> str:
    return "Aggro Aiden"


def emoji() -> str:
    return "😤"


def victory_cry() -> str:
    return "I WILL DESTROY ALL WHO DARE OPPOSE ME!!!"


def roll_again(state: GameState) -> bool:
    return state.turn_score < 40
