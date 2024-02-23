import random
import time

from art import text2art
from rich import box
from rich.align import Align
from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.table import Table, Column
from rich.theme import Theme

from notone import game, signals
from notone.schema import SignalHandler, GameState, GameType, Player, TournamentState


default_theme = Theme(
    {
        "primary": "white",
        "secondary": "bright_black",
        "winner": "green",
        "loser": "red",
        "error": "bold red",
    }
)

console = Console(theme=default_theme)
error_console = Console(stderr=True, theme=default_theme, style="error")


def bigify(content: str, font="tarty1"):
    return str(text2art(content.upper(), font=font))


def panel(renderable: RenderableType, title=None, style="primary") -> Panel:
    return Panel(
        renderable,
        title=title,
        style=style,
        box=box.DOUBLE,
        padding=(1, 2),
    )


def echo(message: str, **kwargs):
    console.print(message, **kwargs)


def error(e: Exception):
    error_console.print(f"ERROR: {e}")


def handle_game_started(state: GameState, players: list[Player]):
    echo("NOT ONE")


def handle_round_started(state: GameState, round: int):
    echo(f"\nROUND {round}")


def handle_turn_started(state: GameState, player: Player):
    echo(f"  {player.name().upper()}")


def handle_roll_failed(state: GameState, d1: int, d2: int):
    echo(f"    🎲: {d1}+{d2} ❌ 0")


def handle_roll_succeeded(state: GameState, d1: int, d2: int):
    echo(f"    🎲: {d1}+{d2} ✅ {state.turn_score}")


def handle_turn_ended(state: GameState, player: Player):
    echo(f"    TOTAL SCORE: {state.scores[state.active]}")


def handle_game_ended(state: GameState, players: list[Player]):
    echo("\nFINAL SCORE")
    for active in range(len(players)):
        player = players[active]
        echo(
            f"{player.emoji()} {player.name()}: "
            f"{state.scores[active]} in {state.rolls[active]} rolls"
        )

    if state.winner is None:
        echo("\nTIE! Play again.\n")
    else:
        winner = players[state.winner]
        echo(f"\n🏆 WINNER: {winner.emoji()} {winner.name()}")
        echo(f"{winner.name()} YAWPS: {winner.victory_cry()}\n")
    echo("GAME OVER")


def handle_tournament_started(tournament: TournamentState):
    console.print(panel(Align.center(bigify("Not One Tournament"))))


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
    console.print(panel(Align.center(bigify(name))))


def handle_tournament_game_started(state: GameState, players: list[Player]):
    p1, p2 = players
    console.rule(
        f"[bold]{p1.emoji()} {p1.name().upper()} vs. {p2.emoji()} {p2.name().upper()}",
        style="primary",
    )


def handle_tournament_turn_started(state: GameState, player: Player):
    echo(f"\n{player.name().upper()} ROLLS")


def handle_tournament_rolled(state: GameState, d1: int, d2: int):
    with console.status("Rolling dice...", spinner="dots"):
        time.sleep(random.random())
        failed = game.failed(state, d1, d2)
        emoji = "✅" if not failed else "❌"
        score = state.turn_score + d1 + d2 if not failed else 0
        echo(f"  🎲: {d1}+{d2} {emoji} {score}")


def handle_tournament_round_ended(state: GameState, round: int, players: list[Player]):
    p1_style = "bold green" if state.scores[0] > state.scores[1] else "bold red"
    p2_style = "bold green" if state.scores[1] > state.scores[0] else "bold red"
    console.line()
    console.rule(
        f"ROUND {round}: "
        f"[{p1_style}]{players[0].name().upper()}: {state.scores[0]}[/] | "
        f"[{p2_style}]{players[1].name().upper()}: {state.scores[1]}[/]",
        align="left",
        style="secondary",
    )
    time.sleep(0.5)


def handle_tournament_game_ended(state: GameState, players: list[Player]):
    if state.winner is None:
        return

    winner_idx = state.winner
    loser_idx = 1 - winner_idx

    winner = players[winner_idx]
    winning_score = state.scores[winner_idx]

    loser = players[loser_idx]
    losing_score = state.scores[loser_idx]

    console.print(
        panel(
            Align.center(
                f"[b]{winner.emoji()} {winner.name().upper()} ({winning_score})[/b]"
                f" defeats "
                f"[b]{loser.emoji()} {loser.name().upper()} ({losing_score})[/b]"
            ),
        )
    )
    console.input("Press enter to continue...")


def handle_tournament_ended(tournament: TournamentState, players: list[Player]):
    if tournament.champion is not None:
        champion = players[tournament.champion]

        def generate_panel(content: Group, title: str = ""):
            # Can't use the theme colors in a Live display.
            return panel(content, title=title, style="white")

        header = Align.center("🏆 THE CHAMPION IS:")
        champ_title = "A champion is crowned".upper()
        champ_name = Align.center(bigify(champion.name()))
        victory_cry_title = f"{champion.name()} yawps".upper()

        with Live(generate_panel(Group(), title=champ_title)) as live:
            live.update(generate_panel(Group(header), title=champ_title))
            time.sleep(0.5)
            live.update(generate_panel(Group(header, champ_name), title=champ_title))
            time.sleep(0.25)

        with Live(generate_panel(Group(), title=victory_cry_title)) as live:
            victory_cry = champion.victory_cry()
            quote = ""
            font = "tarty1" if len(victory_cry) < 30 else "minion"
            for word in victory_cry.split():
                time.sleep(0.5)
                quote += word + " "
                live.update(
                    generate_panel(
                        Group(Align.center(bigify(quote, font=font))),
                        title=victory_cry_title,
                    )
                )
    else:
        console.print(panel(Align.center("Tournament Over".upper())))


def handle_stress_test_started(players: list[Player], total_games: int):
    console.print(
        panel(
            Group(
                Align.center(bigify("Stress Test")),
                Align.center(f"Each player plays {total_games:,} games"),
            )
        )
    )


def handle_stress_test_ended(scoreboard: dict[str, float]):
    scores = Table(
        "Player", Column(header="Avg. Score", justify="right"), box=box.SIMPLE_HEAVY
    )
    for player, score in scoreboard.items():
        scores.add_row(player, f"{score:.2f}")
    console.print(panel(Align.center(scores)))


def handle_stress_test_player_started(player: Player, total_games: int):
    brand = player.name()
    padding = " " * (35 - len(brand))
    console.print(f"{brand}:{padding}", end="")


def handle_stress_test_game_ended(
    player: Player, game_number: int, total_games: int, score: int
):
    increment = total_games // 100
    if game_number % increment == 0:
        console.print("🁢", end="")


def handle_stress_test_player_ended(
    player: Player, average_score: int, cumulative_score: int
):
    console.print(f" {cumulative_score:,} pts")


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
        game_started=handle_tournament_game_started,
        turn_started=handle_tournament_turn_started,
        rolled=handle_tournament_rolled,
        round_ended=handle_tournament_round_ended,
        game_ended=handle_tournament_game_ended,
        tournament_ended=handle_tournament_ended,
    ),
    "stress_test": SignalHandler(
        stress_test_started=handle_stress_test_started,
        stress_test_ended=handle_stress_test_ended,
        stress_test_player_started=handle_stress_test_player_started,
        stress_test_player_ended=handle_stress_test_player_ended,
        stress_test_game_ended=handle_stress_test_game_ended,
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

    signals.stress_test_started.connect(handle.stress_test_started)
    signals.stress_test_ended.connect(handle.stress_test_ended)

    signals.stress_test_player_started.connect(handle.stress_test_player_started)
    signals.stress_test_player_ended.connect(handle.stress_test_player_ended)

    signals.stress_test_game_started.connect(handle.stress_test_game_started)
    signals.stress_test_game_ended.connect(handle.stress_test_game_ended)
