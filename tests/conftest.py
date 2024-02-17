from unittest.mock import Mock
import pytest


from notone import signals


@pytest.fixture
def opponents(aggressive_player, cautious_player) -> list[Mock]:
    return [aggressive_player, cautious_player]


@pytest.fixture
def aggressive_player(mocker) -> Mock:
    player: Mock = mocker.Mock()
    player.roll_again.return_value = True
    return player


@pytest.fixture
def cautious_player(mocker) -> Mock:
    player = mocker.Mock()
    player.roll_again.side_effect = lambda s: s.turn_rolls < 1
    return player


@pytest.fixture
def game_started(mocker) -> Mock:
    return mocker.spy(signals.game_started, "send")


@pytest.fixture
def game_ended(mocker) -> Mock:
    return mocker.spy(signals.game_ended, "send")


@pytest.fixture
def round_started(mocker) -> Mock:
    return mocker.spy(signals.round_started, "send")


@pytest.fixture
def round_ended(mocker) -> Mock:
    return mocker.spy(signals.round_ended, "send")


@pytest.fixture
def turn_started(mocker) -> Mock:
    return mocker.spy(signals.turn_started, "send")


@pytest.fixture
def turn_ended(mocker) -> Mock:
    return mocker.spy(signals.turn_ended, "send")


@pytest.fixture
def rolled(mocker) -> Mock:
    return mocker.spy(signals.rolled, "send")


@pytest.fixture
def roll_succeeded(mocker) -> Mock:
    return mocker.spy(signals.roll_succeeded, "send")


@pytest.fixture
def roll_failed(mocker) -> Mock:
    return mocker.spy(signals.roll_failed, "send")


@pytest.fixture
def tournament_started(mocker) -> Mock:
    return mocker.spy(signals.tournament_started, "send")


@pytest.fixture
def tournament_ended(mocker) -> Mock:
    return mocker.spy(signals.tournament_ended, "send")


@pytest.fixture
def tournament_round_started(mocker) -> Mock:
    return mocker.spy(signals.tournament_round_started, "send")


@pytest.fixture
def tournament_round_ended(mocker) -> Mock:
    return mocker.spy(signals.tournament_round_ended, "send")
