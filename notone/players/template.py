"""Describe your player and their approach."""

from notone.types import GameState


def name() -> str:
    # Return your player's name here:
    return "Template Templeton"


def emoji() -> str:
    # Insert your player's emoji of choice here:
    return "❓"


def victory_cry() -> str:
    # Insert your player's victory cry here:
    return "I win."


def roll_again(state: GameState) -> bool:
    # Implement your player's rolling strategy here. The state instance has all
    # the data about the game that you might need to make a decision:
    #
    # - Which round we're in (out of 10)
    # - What the total scores are, both yours and your opponent's
    # - How many total rolls both you and your opponent have made
    # - What your score is within your current turn
    # - How many rolls you've made within your current turn
    #
    # Note that the strategy below is a guaranteed losing strategy. Don't do it.
    return True
