from importlib import import_module as add

from notone.schema import Player

"""Update the list below to change which players will play the game."""


def load() -> list[Player]:
    return [
        add("notone.players.acey_deucy"),
        add("notone.players.analytical_alec"),
        add("notone.players.gangsta_gary"),
        add("notone.players.nadire_beatrycze"),
        add("notone.players.one_dicerection"),
    ]
