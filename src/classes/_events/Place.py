from classes import Board
from classes.events import Event
from classes.players import Player


class Place(Event):
    def __init__(self, location: int, player: Player) -> None:
        self._location = location
        self._player = player

    def execute(self, board: Board) -> None:
        board[self._location] = self._player
        self._player.pieces += 1
        self._logInfo(f"{self._player} placed a piece at {self._location}")
