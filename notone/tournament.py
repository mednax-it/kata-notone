import math
import random
from typing import Optional

from notone import game, signals
from notone.types import Player, TournamentState


def play(players: list[Player], rounds: Optional[int] = None) -> TournamentState:
    num_of_players = len(players)
    # Since this is a blind-seeded tournament, we'll give everyone a shuffle.
    players = random.sample(players, num_of_players)
    # Calculate the number of rounds necessary to find a winner.
    if rounds is None:
        rounds = math.ceil(math.log2(num_of_players))
    # Single elimination tournaments need the number of slots to be a power of 2
    # (2, 4, 8, 16, 32), so we may need to award some byes to get to the
    # required number.
    num_of_bracket_slots = int(math.pow(2, rounds))
    num_of_byes = num_of_bracket_slots - num_of_players
    competitors = players + [None] * num_of_byes

    state = TournamentState()
    signals.tournament_started.send(state)

    # Play the games
    round = 1
    while round <= rounds:
        state = state.update(round=round)
        signals.tournament_round_started.send(state, players=competitors)

        half_length = len(competitors) // 2
        left_bracket = competitors[:half_length]
        right_bracket = competitors[half_length:]
        right_bracket = list(reversed(right_bracket))

        round_winners: list[Player] = []
        for matchup in zip(left_bracket, right_bracket):
            p1, p2 = matchup
            if p1 is None and p2 is None:
                continue
            if p1 is None:
                round_winners += [p2]  # type: ignore
                continue
            if p2 is None:
                round_winners += [p1]
                continue
            winner: Optional[Player] = None
            while winner is None:
                game_state = game.play([p1, p2])
                winner = p2 if game_state.winner else p1
            round_winners += [winner]

        competitors = round_winners.copy()
        signals.tournament_round_ended.send(state, round=round)
        round += 1

    if len(competitors) == 1 and competitors[0] is not None:
        state = state.update(champion=players.index(competitors[0]))
    signals.tournament_ended.send(state, players=players)
    return state
