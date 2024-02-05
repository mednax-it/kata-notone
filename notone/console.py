from notone import signals
from notone.types import GameState, Player


def echo(message: str):
    print(message)


def error(e: Exception):
    echo(f"ERROR: {e}")


@signals.game_started.connect
def handle_game_started(game: GameState):
    echo("NOT ONE")


@signals.round_started.connect
def handle_round_started(game: GameState, round: int):
    echo(f"\nROUND {round}")


@signals.turn_started.connect
def handle_turn_started(game: GameState, player: Player):
    echo(f"  {player.name().upper()}")


@signals.roll_failed.connect
def handle_roll_failed(game: GameState, d1: int, d2: int):
    echo(f"    🎲: {d1}+{d2} ❌ 0")


@signals.roll_succeeded.connect
def handle_roll_succeeded(game: GameState, d1: int, d2: int):
    echo(f"    🎲: {d1}+{d2} ✅ {game.turn_score}")


@signals.turn_ended.connect
def handle_turn_ended(game: GameState, player: Player):
    echo(f"    SCORE: {game.scores[game.active]}")


@signals.game_ended.connect
def handle_game_ended(game: GameState, players: list[Player]):
    echo("\nFINAL SCORE")
    for active in range(len(players)):
        player = players[active]
        echo(
            f"{player.emoji()} {player.name()}: "
            f"{game.scores[active]} in {game.rolls[active]} rolls"
        )

    if game.winner is None:
        echo("TIE! Play again.")
    else:
        winner = players[game.winner]
        echo(f"\n🏆 WINNER: {winner.emoji()} {winner.name()}")
        echo(f"{winner.name()} YAWPS: {winner.victory_cry()}\n")
    echo("GAME OVER")
