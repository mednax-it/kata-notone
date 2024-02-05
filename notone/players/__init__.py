from importlib import import_module as add

from notone.types import Player

"""Update the list below to change which players will play the game."""


def load() -> list[Player]:
    return [
        add("notone.players.aggro_aiden"),
        add("notone.players.cautious_carter"),
    ]
