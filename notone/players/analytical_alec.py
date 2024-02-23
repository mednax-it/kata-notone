from notone.schema import GameState


def name() -> str:
    return "Analytical Alec"


def emoji() -> str:
    return "🤓"


def victory_cry() -> str:
    return "This was within my calculations"


def roll_again(state: GameState) -> bool:
    return state.turn_score < 20
