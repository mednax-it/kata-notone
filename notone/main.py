"""Not One

This script is a basic runner for the Not One dice game. It will let you
exercise your Not One algorithm; you may need to modify the import below to
point at it if you use a file besides player1.py.
"""
import sys

from notone import game
from notone.players import players
from notone.types import GameState


def play() -> int:
    print("NOT ONE")

    num_players = len(players)
    state = GameState()
    for round in range(1, 11):
        state = game.start_round(state, round)
        print(f"\nROUND {state.round}")

        for active in game.turn_order(num_players, round):
            player = players[active]
            print(f"  {player.name().upper()}")
            state = game.start_turn(state, active)

            while players[active].roll_again(state):
                d1, d2 = game.roll()
                state = game.increment(state, "turn_rolls", 1)
                if game.failed(state, d1, d2):
                    print(f"    🎲: {d1}+{d2} ❌ 0")
                    state = game.reset(state, "turn_score")
                    break
                state = game.increment(state, "turn_score", d1 + d2)
                print(f"    🎲: {d1}+{d2} ✅ {state.turn_score}")
            state = game.end_turn(state, active)
            print(f"    SCORE: {state.scores[active]}")

        game.end_round(state)

    print("\nGAME OVER")
    print("\nFINAL SCORE")
    for active in range(num_players):
        player = players[active]
        print(
            f"{player.emoji()} {player.name()}: "
            f"{state.scores[active]} in {state.rolls[active]} rolls"
        )

    if state.scores[0] > state.scores[1]:
        winner = players[0]
    elif state.scores[1] > state.scores[0]:
        winner = players[1]
    else:
        print("TIE! Play again.")
        return 1
    print(f"\nWINNER: {winner.emoji()} {winner.name()}")
    print(winner.victory_cry())
    return 0


if __name__ == "__main__":
    sys.exit(play())
