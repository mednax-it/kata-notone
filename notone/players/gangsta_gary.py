"""Gangsta Gary takes an average approach, his secret is ############, and he talks a lot of smack."""

from notone.schema import GameState
import random


def name() -> str:
    return "Gangsta Gary"


def emoji() -> str:
    return "💰💰🤬💰💰"


def victory_cry() -> str:
    return random.choice(
        [
            "You lose, bruh!",
            "I'm just looking around to see who's gonna finish second.",
            "Pay me dat money!",
            "Get your popcorn ready, 'cause I'm gonna put on a show.",
            "I'm the best ever. I'm the most brutal and vicious, the most ruthless champion there has ever been. No one can stop me.",
            "Look, everyone's laughing at you.",
            "Next time I'll open my eyes.",
        ]
    )


def roll_again(state: GameState) -> bool:
    return state.turn_score < 19
