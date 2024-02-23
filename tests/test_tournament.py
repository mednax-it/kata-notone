import random
from typing import Optional

import pytest

from notone.tournament import (
    crown_champion,
    matchup_players,
    play_matchup,
    rounds_necessary_for_winner,
    seed_players,
)
from notone.schema import Player, TournamentState


@pytest.mark.parametrize(
    "num_players,rounds",
    [
        (1, 0),
        (2, 1),
        (3, 2),
        (4, 2),
        (5, 3),
        (8, 3),
        (9, 4),
        (16, 4),
        (17, 5),
        (32, 5),
        (33, 6),
        (64, 6),
    ],
)
def test_rounds_necessary_for_winner(num_players: int, rounds: int):
    assert rounds_necessary_for_winner(num_players) == rounds


def test_seed_players_seeds_randomly():
    # Seed random for deterministic behavior.
    random.seed(666)
    players = [
        Player("p1"),
        Player("p2"),
        Player("p3"),
        Player("p4"),
        Player("p5"),
        Player("p6"),
    ]
    seeded = seed_players(players, rounds=3)
    assert seeded != players


def test_seed_players_handles_byes():
    players = [Player("p1"), Player("p2"), Player("p3")]
    assert seed_players(players, rounds=2).count(None) == 1


def test_seed_players_handles_short_tournaments():
    players = [Player("p1"), Player("p2"), Player("p3")]
    assert seed_players(players, rounds=1).count(None) == 0


def test_matchup_players_for_two():
    players: list[Optional[Player]] = [Player("p1"), Player("p2")]
    assert list(matchup_players(players)) == [tuple(players)]


def test_matchup_players_with_bye():
    p1 = Player("p1")
    p2 = Player("p2")
    p3 = Player("p3")
    players: list[Optional[Player]] = [p1, p2, p3, None]
    assert list(matchup_players(players)) == [
        (p1, None),
        (p2, p3),
    ]


def test_matchup_players_highest_seed_with_lowest():
    p1 = Player("p1")
    p2 = Player("p2")
    p3 = Player("p3")
    p4 = Player("p4")
    players: list[Optional[Player]] = [p1, p2, p3, p4]
    assert list(matchup_players(players)) == [
        (p1, p4),
        (p2, p3),
    ]


def test_play_matchup():
    # Seed random for deterministic behavior.
    random.seed(666)

    def roll_once(state):
        return state.turn_rolls < 1

    p1 = Player("p1")
    setattr(p1, "roll_again", roll_once)
    p2 = Player("p2")
    setattr(p2, "roll_again", roll_once)
    assert play_matchup((p1, p2)) == p1


def test_play_matchup_handles_p1_bye():
    p1 = Player("p1")
    assert play_matchup((p1, None)) == p1


def test_play_matchup_handles_p2_bye():
    p2 = Player("p2")
    assert play_matchup((p2, None)) == p2


def test_crown_champion_picks_champ():
    champ = Player("champ")
    players: list[Player] = [Player("p1"), Player("p2"), champ, Player("p4")]
    winners: list[Optional[Player]] = [champ]
    state = crown_champion(TournamentState(), winners, players)
    assert state.champion == 2


def test_crown_champion_multiple_winners_no_champ():
    champ1 = Player("champ1")
    champ2 = Player("champ2")
    players: list[Player] = [Player("p1"), champ1, champ2, Player("p4")]
    winners: list[Optional[Player]] = [champ1, champ2]
    state = crown_champion(TournamentState(), winners, players)
    assert state.champion is None
