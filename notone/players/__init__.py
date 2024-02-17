from importlib import import_module as add

from notone.types import Player

"""Update the list below to change which players will play the game."""


def load() -> list[Player]:
    return [
        add("notone.players.aggro_aiden"),
        add("notone.players.cautious_carter"),
        # add("notone.players.p1"),
        # add("notone.players.p2"),
        # add("notone.players.p3"),
        # add("notone.players.p4"),
        # add("notone.players.p5"),
        # add("notone.players.p6"),
        # add("notone.players.p7"),
        # add("notone.players.p8"),
        # add("notone.players.p9"),
        # add("notone.players.p10"),
        # add("notone.players.p11"),
        # add("notone.players.p12"),
        # add("notone.players.p13"),
        # add("notone.players.p14"),
        # add("notone.players.p15"),
        # add("notone.players.p16"),
    ]
