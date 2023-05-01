from classes import Board
from classes.events import Event
from classes.players import Player


class Move(Event):
    def __init__(self, old: int, new: int, player: Player) -> None:
        self._old = old
        self._new = new
        self._player = player

    def execute(self, board: Board) -> None:
        board[self._old] = None
        board[self._new] = self._player
        self._logInfo(f"{self._player} moved {self._old} to {self._new}")
