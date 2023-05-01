from random import randint

from classes.players import Player


class Computer(Player):
    def __init__(self) -> None:
        super().__init__("CPU")

    def getDecision(self, possibles: list[int]) -> int:
        return possibles[randint(0, len(possibles) - 1)]
