from abc import ABC, abstractmethod

from classes import Board
from utils import LogManager


class Event(ABC):
    def _logInfo(self, info: str):
        LogManager.get().info(info)

    @abstractmethod
    def execute(self, board: Board) -> None:
        pass
