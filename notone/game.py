import random
from dataclasses import asdict
from typing import Iterator

from notone import signals
from notone.schema import (
    GameState,
    IncrementableAttribute,
    Player,
    ResetableAttribute,
)


def roll_die() -> int:
    """Rolls a single die by randomly selecting a value from 1-6.

    Returns:
        int: The face value for the die.
    """
    return random.randint(1, 6)


def roll(state: GameState) -> GameState:
    """Simulates rolling two dice.

    Args:
        state (GameState): The current game state.

    Returns:
        GameState: The new game state, with the roll results saved and roll
        counter incremented.
    """
    increment_turn_rolls = increment(state, "turn_rolls", 1)
    new_state = asdict(increment_turn_rolls) | {"roll": (roll_die(), roll_die())}
    return GameState(**new_state)


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


def select_winner(state: GameState) -> GameState:
    """Sets the winner—the player with the highest total points—of the game.

    Args:
        state (GameState): The current game state.

    Returns:
        GameState: The new game state with the winner set.
    """
    if state.scores[0] > state.scores[1]:
        winner = 0
    elif state.scores[1] > state.scores[0]:
        winner = 1
    else:
        winner = None
    new_state = asdict(state) | {"winner": winner}
    return GameState(**new_state)


def play(players: list[Player], rounds=10) -> GameState:
    state = GameState()
    signals.game_started.send(state, players=players)

    for round in range(1, rounds + 1):
        state = start_round(state, round)
        signals.round_started.send(state, round=round)

        for active in turn_order(len(players), round):
            player = players[active]
            state = start_turn(state, active)
            signals.turn_started.send(state, player=player)

            while player.roll_again(state):
                state = roll(state)
                d1, d2 = state.roll
                signals.rolled.send(state, d1=d1, d2=d2)
                if failed(state, d1, d2):
                    state = reset(state, "turn_score")
                    signals.roll_failed.send(state, d1=d1, d2=d2)
                    break
                state = increment(state, "turn_score", d1 + d2)
                signals.roll_succeeded.send(state, d1=d1, d2=d2)
            state = end_turn(state, active)
            signals.turn_ended.send(state, player=player)

        end_round(state)
        signals.round_ended.send(state, round=round, players=players)

    state = select_winner(state)
    signals.game_ended.send(state, players=players)
    return state
