import random

from notone import game, signals
from notone.schema import Player


def play(players: list[Player], total_games: int = 10000) -> None:
    signals.stress_test_started.send(players, total_games=total_games)
    scoreboard: dict[str, float] = {}
    for player in random.sample(players, len(players)):
        signals.stress_test_player_started.send(player, total_games=total_games)
        cumulative_score = 0
        for x in range(total_games):
            signals.stress_test_game_started.send(
                player, game_number=x, total_games=total_games
            )
            state = game.play([player])
            signals.stress_test_game_ended.send(
                player, game_number=x, total_games=total_games, score=state.scores[0]
            )
            cumulative_score += state.scores[0]
        average_score = cumulative_score / total_games
        signals.stress_test_player_ended.send(
            player, average_score=average_score, cumulative_score=cumulative_score
        )
        brand = f"{player.emoji()} {player.name()}"
        scores = list(scoreboard.items()) + [(brand, average_score)]
        scoreboard = {
            player: score
            for (player, score) in sorted(scores, key=lambda x: x[1], reverse=True)
        }

    signals.stress_test_ended.send(scoreboard)
