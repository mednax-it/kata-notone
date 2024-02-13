from notone.types import GameState


def name() -> str:
    return "Four"


def emoji() -> str:
    return "️4️⃣"


def victory_cry() -> str:
    return f"{name()} reigns supreme."


def roll_again(state: GameState) -> bool:
    return state.turn_rolls < 4
