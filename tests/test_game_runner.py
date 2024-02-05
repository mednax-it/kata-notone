import pytest

from notone import game, signals
from notone.types import GameState


def test_game_starts(opponents, game_started):
    state = game.play(opponents, rounds=0)
    assert game_started.called
    assert state.round == 0
    assert state.scores == (0, 0)
    assert state.rolls == (0, 0)


def test_default_game_ends_after_10_rounds(opponents, round_ended, game_ended):
    state = game.play(opponents)
    assert game_ended.called
    assert state.round == 10
    assert round_ended.call_count == 10


def test_each_player_gets_one_turn_per_round(opponents, turn_started):
    game.play(opponents, rounds=1)
    (player_1, player_2) = opponents
    assert turn_started.call_count == 2
    assert turn_started.call_args_list[0][1]["player"] == player_1
    assert turn_started.call_args_list[1][1]["player"] == player_2


def test_turns_happen_in_proper_order(opponents, turn_ended):
    game.play(opponents)
    (player_1, player_2) = opponents
    assert turn_ended.call_args_list[0][1]["player"] == player_1
    assert turn_ended.call_args_list[1][1]["player"] == player_2
    assert turn_ended.call_args_list[2][1]["player"] == player_2
    assert turn_ended.call_args_list[3][1]["player"] == player_1
    assert turn_ended.call_args_list[4][1]["player"] == player_1
    assert turn_ended.call_args_list[5][1]["player"] == player_2


def test_each_successful_roll_adds_to_turn_score(cautious_player, roll_succeeded):
    state = game.play([cautious_player], rounds=1)
    assert roll_succeeded.called
    d1 = roll_succeeded.call_args[1]["d1"]
    d2 = roll_succeeded.call_args[1]["d2"]
    assert state.turn_score == d1 + d2


def test_failed_roll_zeros_turn_score_and_ends_turn(
    aggressive_player, roll_failed, turn_ended
):
    state = game.play([aggressive_player], rounds=1)
    assert roll_failed.called
    assert state.turn_score == 0
    assert turn_ended.called


def test_not_rolling_again_ends_turn_and_adds_turn_score_to_total(
    cautious_player, turn_ended
):
    state = game.play([cautious_player], rounds=1)
    assert turn_ended.called
    assert state.scores[0] == state.turn_score


@pytest.fixture
def opponents(aggressive_player):
    return [aggressive_player, aggressive_player]


@pytest.fixture
def aggressive_player(mocker):
    player = mocker.Mock()
    player.roll_again.return_value = True
    return player


@pytest.fixture
def cautious_player(mocker):
    player = mocker.Mock()
    player.roll_again.side_effect = [True, False]
    return player


@pytest.fixture
def game_started(mocker):
    return mocker.spy(signals.game_started, "send")


@pytest.fixture
def game_ended(mocker):
    return mocker.spy(signals.game_ended, "send")


@pytest.fixture
def round_started(mocker):
    return mocker.spy(signals.round_started, "send")


@pytest.fixture
def round_ended(mocker):
    return mocker.spy(signals.round_ended, "send")


@pytest.fixture
def turn_started(mocker):
    return mocker.spy(signals.turn_started, "send")


@pytest.fixture
def turn_ended(mocker):
    return mocker.spy(signals.turn_ended, "send")


@pytest.fixture
def rolled(mocker):
    return mocker.spy(signals.rolled, "send")


@pytest.fixture
def roll_succeeded(mocker):
    return mocker.spy(signals.roll_succeeded, "send")


@pytest.fixture
def roll_failed(mocker):
    return mocker.spy(signals.roll_failed, "send")
