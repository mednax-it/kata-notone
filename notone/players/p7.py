from notone.schema import GameState


def name() -> str:
    return "Seven"


def emoji() -> str:
    return "7️⃣"


def victory_cry() -> str:
    return f"{name()} reigns supreme."


def roll_again(state: GameState) -> bool:
    return state.turn_rolls < 4
