from abc import ABC, abstractmethod
from typing import cast

from utils import COLOURS, TCOLOUR, colourText, getInput

_COLOURS_LEFT = list(COLOURS.keys())


class Player(ABC):
    def __init__(self, name: str) -> None:
        self._playerName = name
        self._playerColour: TCOLOUR = cast(
            TCOLOUR,
            getInput(
                f"Possible colours: {_COLOURS_LEFT}\nEnter {name}'s colour: ",
                str,
                "Invalid colour",
                lambda colour: colour in COLOURS,
            ),
        )
        _COLOURS_LEFT.remove(self._playerColour)
        self._piecesOnBoard = 0

    def __str__(self) -> str:
        return colourText(self._playerName, self._playerColour)

    @property
    def colour(self) -> TCOLOUR:
        return self._playerColour

    @property
    def pieces(self) -> int:
        return self._piecesOnBoard

    @pieces.setter
    def pieces(self, value: int) -> None:
        self._piecesOnBoard = value

    @abstractmethod
    def getDecision(self, possibles: list[int]) -> int:
        pass
