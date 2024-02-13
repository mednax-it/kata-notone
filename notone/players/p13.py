from notone.types import GameState


def name() -> str:
    return "Thirteen"


def emoji() -> str:
    return "1️⃣3️⃣"


def victory_cry() -> str:
    return f"{name()} reigns supreme."


def roll_again(state: GameState) -> bool:
    return state.turn_rolls < 4
