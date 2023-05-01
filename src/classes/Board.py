from typing import Generator

from classes.players import Player
from utils import colourText

MILL_POSITIONS: list[tuple[list[int], list[int]]] = [
    ([1, 2], [9, 21]),
    ([0, 2], [4, 7]),
    ([0, 1], [14, 23]),
    ([4, 5], [10, 18]),
    ([3, 5], [1, 7]),
    ([3, 4], [13, 20]),
    ([7, 8], [11, 15]),
    ([6, 8], [1, 4]),
    ([6, 7], [12, 17]),
    ([10, 11], [0, 21]),
    ([9, 11], [3, 18]),
    ([9, 10], [6, 15]),
    ([13, 14], [8, 17]),
    ([12, 14], [5, 20]),
    ([12, 13], [2, 23]),
    ([16, 17], [6, 11]),
    ([15, 17], [19, 22]),
    ([15, 16], [8, 12]),
    ([19, 20], [3, 10]),
    ([18, 20], [16, 22]),
    ([18, 19], [5, 13]),
    ([22, 23], [0, 9]),
    ([21, 23], [16, 19]),
    ([21, 22], [2, 14]),
]

ADJACENT_POSITIONS: list[tuple[int, ...]] = [
    (1, 9),
    (0, 2, 4),
    (1, 14),
    (4, 10),
    (1, 3, 5, 7),
    (4, 13),
    (7, 11),
    (4, 6, 8),
    (7, 12),
    (0, 10, 21),
    (3, 9, 11, 18),
    (6, 10, 15),
    (8, 13, 17),
    (5, 12, 14, 20),
    (2, 13, 23),
    (11, 16),
    (15, 17, 19),
    (12, 16),
    (10, 19),
    (16, 18, 20, 22),
    (13, 19),
    (9, 22),
    (19, 21, 23),
    (14, 22),
]


class Board:
    def __init__(self):
        self._positions: list[Player | None] = [None] * 24

    def __repr__(self) -> str:
        coloured_positions = (f"{i:02}" if player is None else colourText(f"{i:02}", player.colour) for i, player in enumerate(self._positions))
        return """
            {} ============== {} ============== {}
            ||                ||                ||
            ||    {} ======== {} ======== {}    ||
            ||    ||          ||          ||    ||
            ||    ||    {} == {} == {}    ||    ||
            ||    ||    ||          ||    ||    ||
            {} == {} == {}          {} == {} == {}
            ||    ||    ||          ||    ||    ||
            ||    ||    {} == {} == {}    ||    ||
            ||    ||          ||          ||    ||
            ||    {} ======== {} ======== {}    ||
            ||                ||                ||
            {} ============== {} ============== {}
            """.format(
            *coloured_positions
        )

    def __getitem__(self, index: int):
        return self._positions[index]

    def __setitem__(self, index: int, player: Player | None):
        self._positions[index] = player

    def getAvailablePositions(self) -> list[int]:
        return [i for i, p in enumerate(self._positions) if p is None]

    def getRemoveableLocations(self, player: Player) -> list[int]:
        return [pos for pos, p in enumerate(self._positions) if p not in (player, None) and not self.getMillsFormed(pos)]
    
    def _getPlayerLocations(self, player: Player) -> Generator[int, None, None]:
        return (i for i, p in enumerate(self._positions) if p is player)

    def getPiecesThatCanMove(self, player: Player) -> dict[int, list[int]]:
        pieceLocations = self._getPlayerLocations(player)
        piecesThatCanMove: dict[int, list[int]] = {}
        for piece in pieceLocations:
            adjacents = ADJACENT_POSITIONS[piece]
            empty_adjacents = [adjacent for adjacent in adjacents if self[adjacent] is None]

            if len(empty_adjacents) > 0:
                piecesThatCanMove[piece] = empty_adjacents

        return piecesThatCanMove

    def getMillsFormed(self, position: int) -> int:
        playerAtPosition = self[position]
        if playerAtPosition is None:
            return 0
        return sum(all(self[pos] is playerAtPosition for pos in mill) for mill in MILL_POSITIONS[position])
