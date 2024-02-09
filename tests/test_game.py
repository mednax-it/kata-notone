from notone.game import (
    end_turn,
    failed,
    increment,
    reset,
    roll,
    roll_die,
    select_winner,
    start_round,
    start_turn,
    turn_order,
)
from notone.types import GameState


def test_roll_die_does_not_exceed_range():
    for _ in range(100):
        rolled = roll_die()
        assert rolled >= 1 and rolled <= 6


def test_roll_returns_results_for_two_dice():
    assert len(roll(GameState()).roll) == 2


def test_failed_fails_if_first_die_is_one():
    assert failed(GameState(turn_rolls=2), 1, 2)


def test_failed_fails_if_second_die_is_one():
    assert failed(GameState(turn_rolls=2), 2, 1)


def test_failed_fails_if_both_dice_are_ones():
    assert failed(GameState(turn_rolls=2), 1, 1)


def test_failed_does_not_fail_if_no_ones():
    assert not failed(GameState(turn_rolls=2), 2, 2)


def test_failed_does_not_fail_if_first_turn():
    assert not failed(GameState(turn_rolls=1), 1, 1)


def test_start_round_updates_round_count():
    state = start_round(GameState(round=2), 3)
    assert state.round == 3


def test_start_turn_resets_turn_data():
    state = start_turn(GameState(turn_rolls=2, turn_score=20, active=1), active=0)
    assert state.turn_rolls == 0
    assert state.turn_score == 0
    assert state.active == 0


def test_increment_bumps_property_by_one_by_default():
    state = increment(GameState(turn_score=20), "turn_score")
    assert state.turn_score == 21


def test_increment_bumps_property_by_given_amount():
    state = increment(GameState(turn_score=20), "turn_score", 10)
    assert state.turn_score == 30


def test_increment_does_not_change_other_attributes():
    state = increment(GameState(turn_rolls=2, turn_score=20, round=2), "turn_score")
    assert state.round == 2
    assert state.turn_rolls == 2


def test_reset_zeroes_out_attribute():
    state = reset(GameState(turn_score=20), "turn_score")
    assert state.turn_score == 0


def test_reset_does_not_change_other_attributes():
    state = reset(GameState(turn_rolls=2, turn_score=20), "turn_score")
    assert state.turn_rolls == 2


def test_end_turn_updates_score_with_turn_score():
    state = end_turn(GameState(turn_score=20, scores=(20, 30)), active=0)
    assert state.scores == (40, 30)


def test_end_turn_updates_rolls_with_turn_rolls():
    state = end_turn(GameState(turn_rolls=5, rolls=(10, 20)), active=1)
    assert state.rolls == (10, 25)


def test_turn_order_is_normal_for_odd_rounds():
    assert list(turn_order(num_players=2, round=1)) == [0, 1]


def test_turn_order_is_reversed_for_even_rounds():
    assert list(turn_order(num_players=2, round=2)) == [1, 0]


def test_select_winner_p1_wins():
    state = select_winner(GameState(scores=(30, 20)))
    assert state.winner == 0


def test_select_winner_p2_wins():
    state = select_winner(GameState(scores=(20, 30)))
    assert state.winner == 1


def test_select_winner_tie():
    state = select_winner(GameState(scores=(20, 20)))
    assert state.winner is None
