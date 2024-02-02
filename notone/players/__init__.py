from importlib import import_module as add

from types import ModuleType

"""Update the list below to change which players will play the game."""

players: list[ModuleType] = [
    add("notone.players.aggro_aiden"),
    add("notone.players.cautious_carter"),
]
