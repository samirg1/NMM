from typing import cast
from classes import Board
from classes.events import Event
from classes.players import Player


class Remove(Event):
    def __init__(self, at: int, player: Player) -> None:
        self._at = at
        self._player = player

    def execute(self, board: Board) -> None:
        self._removed = cast(Player, board[self._at])
        self._removed.pieces -= 1
        board[self._at] = None
        self._logInfo(f"{self._player} removed {self._removed}'s piece from {self._at}")
