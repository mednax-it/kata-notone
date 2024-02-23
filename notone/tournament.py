import math
import random
from typing import Iterator, Optional

from notone import game, signals
from notone.schema import Player, TournamentState


def rounds_necessary_for_winner(num_players: int) -> int:
    """
    Does the maths to calculate how many rounds will be required to produce a
    winner, given the number of players involved.

    Args:
        num_players int: The number of players in the tournament.

    Returns:
        int: The number of rounds that need to be played to get a winner.
    """
    return math.ceil(math.log2(num_players))


def seed_players(players: list[Player], rounds: int) -> list[Optional[Player]]:
    """
    Seeds all the players for a blind-seeded, single-elimination tournament.
    Each player's seed is represented by their index in the list, so players[0]
    is the #1 seed and so forth.

    Args:
        players (list[Player]): A list of players to generate the bracket from.
        rounds (int): The number of rounds to be played.

    Returns:
        list[Optional[Player]]: A list of seeded players, with None occupying
        enough seeds to setup a power of 2 field size. These Nones represent
        byes for their first round opponents.
    """
    num_of_players = len(players)
    # Since this is a blind-seeded tournament, we'll give everyone a shuffle.
    players = random.sample(players, num_of_players)
    # Single elimination tournaments need the number of slots to be a power of 2
    # (2, 4, 8, 16, 32), so we may need to award some byes to get to the
    # required number.
    num_of_bracket_slots = int(math.pow(2, rounds))
    # We need to fill the empty slots with Nones, which equate to a bye for the
    # opposing team.
    num_of_byes = num_of_bracket_slots - num_of_players
    return players + [None] * num_of_byes


def matchup_players(
    players: list[Optional[Player]],
) -> Iterator[tuple[Optional[Player], Optional[Player]]]:
    """
    Matches up the seeded players with their opponents. For example, in a 16
    player tournament, the #1 seed should play the #16 seed, the #2 vs. #15, and
    so on.

    Args:
        players (list[Optional[Player]]): A list of the players in the
        tournament; some players may be None to meet the necessary power of 2
        field size.

    Returns:
        tuple[list[Optional[Player]], list[Optional[Player]]]: The right and left brackets
    """
    half_length = len(players) // 2
    left_bracket = players[:half_length]
    right_bracket = players[half_length:]
    right_bracket = list(reversed(right_bracket))
    return zip(left_bracket, right_bracket)


def play_matchup(
    matchup: tuple[Optional[Player], Optional[Player]],
) -> Player:
    """
    Plays a matchup/game between two players. If one of the playes is None, this
    match is treated as a bye and their opponent is automatically passed
    through. In the case of a tie, we play another game until the tie is broken.

    Args:
        matchup (tuple[Optional[Player], Optional[Player]]): _description_

    Returns:
        Optional[Player]: _description_
    """
    p1, p2 = matchup
    if p1 is None:
        return p2  # type: ignore
    if p2 is None:
        return p1
    winner: Optional[Player] = None
    while winner is None:
        game_state = game.play([p1, p2])
        winner = p2 if game_state.winner else p1
    return winner


def crown_champion(
    state: TournamentState,
    winners: list[Optional[Player]],
    initial_field: list[Player],
) -> TournamentState:
    """
    Check to see if a champion has been chosen. If it has, update the state with
    the index of the champion in the initial list of players. Note that we put
    the index in the state because it's easily serializable, whereas players are
    not.

    Args:
        state (TournamentState): The current tournament state.
        winners (list[Optional[Player]]): The list of all the winners.
        initial_field (list[Player]): The initial list of all the players
        entered in the tournament.

    Returns:
        TournamentState: The tournament state with a champion selected; note
        there may be no champion if not enough rounds have been played.
    """
    # There can be only one…
    if len(winners) > 1:
        return state
    if winners[0] is None:
        return state
    return state.update(champion=initial_field.index(winners[0]))


def play(players: list[Player], rounds: Optional[int] = None) -> TournamentState:
    rounds = rounds or rounds_necessary_for_winner(len(players))
    active_players: list[Optional[Player]] = seed_players(players, rounds)

    state = TournamentState()
    signals.tournament_started.send(state)

    # Play the games
    round = 1
    while round <= rounds:
        state = state.update(round=round)
        signals.tournament_round_started.send(state, players=active_players)

        round_winners: list[Player] = []
        for matchup in matchup_players(active_players):
            winner = play_matchup(matchup)
            round_winners += [winner]

        active_players = round_winners.copy()  # type: ignore
        signals.tournament_round_ended.send(state, players=active_players)
        round += 1

    state = crown_champion(state, winners=active_players, initial_field=players)
    signals.tournament_ended.send(state, players=players)
    return state
