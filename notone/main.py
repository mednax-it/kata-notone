"""Not One

This script is a basic runner for playing the Not One dice game via the console.
It will let you exercise your Not One player. See the README for more details
on how to work with this code, including setting up your Not One player:

https://github.com/mednax-it/kata-notone#creating-your-own-player
"""
import typer

from notone import (
    console,
    game as game_runner,
    players,
    tournament as tournament_runner,
)

app = typer.Typer()


@app.command()
def game():
    opponents = players.load()
    if len(opponents) > 2:
        console.echo(
            f"{len(opponents)} players registered; a game can only by played "
            "by 2 players. Try [primary]`notone tournament`[/] or modify the "
            "[primary]`notone/players/__init__.py`[/] file to register fewer "
            "players.",
            style="error",
        )
        raise typer.Exit(1)
    console.connect_output("game")
    game_runner.play(opponents)


@app.command()
def tournament():
    console.connect_output("tournament")
    tournament_runner.play(players.load())


if __name__ == "__main__":
    app()
