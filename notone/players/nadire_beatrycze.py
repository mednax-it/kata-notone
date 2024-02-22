"""Nadire Beatrycze does not roll more than 6 times and a score no more than 16"""

from random import choice
from notone.types import GameState


def name() -> str:
    return "Nadire Beatrycze"


def emoji() -> str:
    emojis = [
        "😃",
        "🤪",
        "😫",
        "😐",
        "😵‍💫",
    ]
    return choice(emojis)


def victory_cry() -> str:
    victory_cries = [
        "UGH, AS IF!",
        "YOU CAN'T HANDLE THE TRUTH!",
        "YOU'RE KILLING ME, SMALLS!",
        "SHOW ME THE MONEY!",
        "WITH GREAT POWER, COMES GREAT RESPONSIBILITY.",
    ]
    return choice(victory_cries)


def roll_again(state: GameState) -> bool:
    return state.turn_rolls < 6 and state.turn_score < 16
