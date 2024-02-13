from notone import tournament


def test_tournament_starts(opponents, tournament_started):
    state = tournament.play(opponents * 8, rounds=0)
    assert state.round == 0
    assert len(state.players) == 16
    assert tournament_started.called


def test_tournament_plays_one_round(
    cautious_player, game_started, tournament_round_started
):
    state = tournament.play([cautious_player] * 16, rounds=1)
    assert state.round == 1
    assert tournament_round_started.called
    assert len(state.winners) == 8
    # Might need more than 8 games if there's a tie.
    assert game_started.call_count >= 8
    assert state.champion is None


def test_tournament_crowns_winner(cautious_player, tournament_ended):
    state = tournament.play([cautious_player] * 16)
    assert state.round == 4
    assert tournament_ended.called
    assert len(state.winners) == 1
    assert state.champion is not None


def test_tournament_handles_byes(cautious_player):
    state = tournament.play([cautious_player] * 20)
    assert state.round == 5
    assert len(state.players) == 32
    assert len(state.winners) == 1
    assert state.champion is not None
