import sys

from rich import print

from notone import signals
from notone.types import SignalHandler, GameState, GameType, Player, TournamentState


def echo(message: str, **kwargs):
    print(message, **kwargs)


def error(e: Exception):
    echo(f"ERROR: {e}", file=sys.stderr)


def handle_game_started(game: GameState):
    echo("NOT ONE")


def handle_round_started(game: GameState, round: int):
    echo(f"\nROUND {round}")


def handle_turn_started(game: GameState, player: Player):
    echo(f"  {player.name().upper()}")


def handle_roll_failed(game: GameState, d1: int, d2: int):
    echo(f"    🎲: {d1}+{d2} ❌ 0")


def handle_roll_succeeded(game: GameState, d1: int, d2: int):
    echo(f"    🎲: {d1}+{d2} ✅ {game.turn_score}")


def handle_turn_ended(game: GameState, player: Player):
    echo(f"    TOTAL SCORE: {game.scores[game.active]}")


def handle_game_ended(game: GameState, players: list[Player]):
    echo("\nFINAL SCORE")
    for active in range(len(players)):
        player = players[active]
        echo(
            f"{player.emoji()} {player.name()}: "
            f"{game.scores[active]} in {game.rolls[active]} rolls"
        )

    if game.winner is None:
        echo("\nTIE! Play again.\n")
    else:
        winner = players[game.winner]
        echo(f"\n🏆 WINNER: {winner.emoji()} {winner.name()}")
        echo(f"{winner.name()} YAWPS: {winner.victory_cry()}\n")
    echo("GAME OVER")


def handle_tournament_started(tournament: TournamentState):
    echo("NOT ONE TOURNAMENT")


def handle_tournament_round_started(tournament: TournamentState, players: list[Player]):
    num_players = len(players)
    if None in players:
        name = "Play-in Round"
    elif num_players == 2:
        name = "Championship"
    elif num_players == 4:
        name = "Final Four"
    elif num_players == 8:
        name = "Elite Eight"
    elif num_players == 16:
        name = "Sweet Sixteen"
    else:
        name = f"Round of {num_players}"
    echo(f"\n{name.upper()}")


def handle_tournament_round_ended(tournament: TournamentState, players: list[Player]):
    if len(players) <= 1:
        return
    input("\n  Press enter to play the next round...")


def handle_tournament_game_ended(game: GameState, players: list[Player]):
    if game.winner is None:
        return

    winner_idx = game.winner
    loser_idx = 1 - winner_idx

    winner = players[winner_idx]
    winning_score = game.scores[winner_idx]

    loser = players[loser_idx]
    losing_score = game.scores[loser_idx]

    echo(f"  {winner.name()} defeats {loser.name()}, {winning_score} to {losing_score}")


def handle_tournament_ended(tournament: TournamentState, players: list[Player]):
    if tournament.champion is not None:
        champion = players[tournament.champion]
        echo(f"\n🏆 THE CHAMPION IS: {champion.emoji()} {champion.name()}")
        echo(f"{champion.name()} YAWPS: {champion.victory_cry()}\n")
    echo("TOURNAMENT OVER")


signal_handlers: dict[GameType, SignalHandler] = {
    "game": SignalHandler(
        game_started=handle_game_started,
        round_started=handle_round_started,
        turn_started=handle_turn_started,
        roll_failed=handle_roll_failed,
        roll_succeeded=handle_roll_succeeded,
        turn_ended=handle_turn_ended,
        game_ended=handle_game_ended,
    ),
    "tournament": SignalHandler(
        tournament_started=handle_tournament_started,
        tournament_round_started=handle_tournament_round_started,
        tournament_round_ended=handle_tournament_round_ended,
        game_ended=handle_tournament_game_ended,
        tournament_ended=handle_tournament_ended,
    ),
}


def connect_output(type: GameType):
    handle = signal_handlers[type]

    signals.game_started.connect(handle.game_started)
    signals.game_ended.connect(handle.game_ended)

    signals.round_started.connect(handle.round_started)
    signals.round_ended.connect(handle.round_ended)

    signals.turn_started.connect(handle.turn_started)
    signals.turn_ended.connect(handle.turn_ended)

    signals.rolled.connect(handle.rolled)
    signals.roll_succeeded.connect(handle.roll_succeeded)
    signals.roll_failed.connect(handle.roll_failed)

    signals.tournament_started.connect(handle.tournament_started)
    signals.tournament_ended.connect(handle.tournament_ended)

    signals.tournament_round_started.connect(handle.tournament_round_started)
    signals.tournament_round_ended.connect(handle.tournament_round_ended)
