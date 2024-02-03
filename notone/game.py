import random
from dataclasses import asdict
from typing import Iterator

from notone.types import GameState, IncrementableAttribute, ResetableAttribute


def roll_die() -> int:
    """Rolls a single die by randomly selecting a value from 1-6.

    Returns:
        int: The face value for the die.
    """
    return random.randint(1, 6)


def roll() -> tuple[int, int]:
    """Simulates rolling two dice.

    Returns:
        tuple[int, int]: The face values for each die.
    """
    return (roll_die(), roll_die())


def failed(state: GameState, d1: int, d2: int) -> bool:
    """Check whether the player has failed their turn.

    Args:
        state (GameState): The current game state.
        d1 (int): The face value of die 1.
        d2 (int): The face value of die 2.

    Returns:
        bool: Whether the player has failed.
    """
    if state.turn_rolls == 1:
        return False
    return d1 == 1 or d2 == 1


def start_round(state: GameState, round: int) -> GameState:
    """Starts a new round.

    Args:
        state (GameState): The current game state.
        round (int): The new round number.

    Returns:
        GameState: The new game state, ready for the new round.
    """
    new_state = asdict(state) | {"round": round}
    return GameState(**new_state)


def turn_order(num_players: int, round: int) -> Iterator:
    """Generates the turn order for a given round.

    Args:
        round (int): The round number.

    Returns:
        iter: An iterator of the player indices in the order of turn.
    """
    order = range(num_players)
    order = order if round % 2 == 1 else reversed(order)
    return iter(order)


def start_turn(state: GameState, active: int) -> GameState:
    """Starts a new turn.

    Args:
        state (GameState): The current game state.

    Returns:
        GameState: The new game state, ready for the new turn.
    """
    reset_turn_rolls = reset(state, "turn_rolls")
    reset_turn_score = reset(reset_turn_rolls, "turn_score")
    new_state = asdict(reset_turn_score) | {"active": active}
    return GameState(**new_state)


def increment(
    state: GameState, attribute: IncrementableAttribute, amount: int = 1
) -> GameState:
    """Bumps a game state attribute by a given amount.

    Args:
        state (GameState): The current game state.
        attriburte (IncrementableAttribute): The attribute in the game state to increment.
        amount (int, optional): The amount to increment the attribute by. Defaults to 1.

    Returns:
        GameState: The game state with the incremented attribute.
    """
    new_state = asdict(state) | {attribute: getattr(state, attribute) + amount}
    return GameState(**new_state)


def reset(state: GameState, attribute: ResetableAttribute) -> GameState:
    """Resets a game state attribute to zero.

    Args:
        state (GameState): The current game state.
        attriburte (ResetableAttribute): The attribute in the game state to reset.

    Returns:
        GameState: The game state with the reset attribute.
    """
    new_state = asdict(state) | {attribute: 0}
    return GameState(**new_state)


def end_turn(state: GameState, active: int) -> GameState:
    """Ends a turn.

    Args:
        state (GameState): The current game state.
        active (int): The active player for this turn.

    Returns:
        GameState: The new game state, cleaned up for the end of the turn.
    """
    new_score = state.scores[active] + state.turn_score
    new_roll = state.rolls[active] + state.turn_rolls
    new_scores = (
        (state.scores[0], new_score) if active else (new_score, state.scores[1])
    )
    new_rolls = (state.rolls[0], new_roll) if active else (new_roll, state.rolls[1])
    new_state = asdict(state) | {
        "scores": new_scores,
        "rolls": new_rolls,
    }
    return GameState(**new_state)


def end_round(state: GameState) -> GameState:
    """Ends a round.

    Args:
        state (GameState): The current game state.

    Returns:
        GameState: The new game state, cleaned up for the end of the round.
    """
    # Doesn't actually do anything at the moment.
    return state
