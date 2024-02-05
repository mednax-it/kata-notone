import pytest

from notone import game


@pytest.fixture
def player(mocker, faker):
    p = mocker.Mock()
    p.name.return_value = faker.first_name_nonbinary()
    p.emoji.return_value = faker.emoji()
    p.victory_cry.return_value = faker.sentence()
    p.roll_again.return_value = faker.boolean()
    return p


def test_player_roll_again(player):
    players = [player]
    game.play(players)
    assert player.roll_again.called
    assert len(player.roll_again.call_args[0]) == 1
    (state,) = player.roll_again.call_args[0]
    assert hasattr(state, "active")
    assert hasattr(state, "rolls")
    assert len(state.rolls) == 2
    assert hasattr(state, "round")
    assert hasattr(state, "scores")
    assert len(state.scores) == 2
    assert hasattr(state, "turn_rolls")
    assert hasattr(state, "turn_score")
