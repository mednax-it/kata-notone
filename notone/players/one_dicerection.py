"""Describe your player and their approach."""

from notone.types import GameState


def name() -> str:
    # Return your player's name here:
    return "Harry Dicerolls"


def emoji() -> str:
    # Insert your player's emoji of choice here:
    return "🤘"


def victory_cry() -> str:
    # Insert your player's victory cry here:
    return "Best roll ever!"


opponent_previous_score = 1
did_opponent_fail = False

def roll_again(state: GameState) -> bool:
    global opponent_previous_score
    global did_opponent_fail
    opp_id = 1 - state.active
    if state.turn_rolls == 0:
        did_opponent_fail = state.active != 0 and opponent_previous_score == state.scores[opp_id]
        opponent_previous_score = state.scores[opp_id]
        return True # if it's the first roll, always roll.

    score_diff = abs(state.scores[0] - state.scores[1])
    risk_appetite = 30 + (score_diff/9)
    turn_decay = (state.turn_rolls+1) * 10

    if did_opponent_fail:
        risk_appetite = 40

    if risk_appetite - turn_decay < 0:
        return False
    return True
