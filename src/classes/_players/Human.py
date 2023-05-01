from classes.players import Player
from utils import getInput


class Human(Player):
    def __init__(self) -> None:
        super().__init__(getInput("Enter name: ", str))

    def getDecision(self, possibles: list[int]) -> int:
        return getInput(
            f"Enter decision: ",
            int,
            "Invalid selection",
            lambda possible: possible in possibles,
        )
