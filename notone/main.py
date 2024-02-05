"""Not One

This script is a basic runner for playing the Not One dice game via the console.
It will let you exercise your Not One player. See the README for more details
on how to work with this code, including setting up your Not One player:

https://github.com/mednax-it/kata-notone#creating-your-own-player
"""
import sys

from notone import console, game, players


def main() -> int:
    try:
        opponents = players.load()
        game.play(opponents)
    except Exception as e:
        console.error(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
