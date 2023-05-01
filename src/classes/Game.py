from classes import Board
from classes.events import Move, Place, Remove
from classes.players import Computer, Human, Player
from utils import LogManager, getInput


class Game:
    def __init__(self):
        self._board = Board()
        self._logger = LogManager.get()

        self._logger.info(f"\nWelcome to Nine Man's Morris!\n{'-'*30}\n")

        numberOfPlayers = getInput("Enter the number of players: ", int, "Invalid number of players", lambda number: number in (1, 2))

        self._players: list[Player] = [Human() for _ in range(numberOfPlayers)]
        if numberOfPlayers == 1:
            self._players.append(Computer())

        self._activePlayerIndex = 0
        self._currentPlayer = self._players[self._activePlayerIndex]

    def play(self):
        self._logger.info(self._board)

        # PLACEMENT OF PIECES
        for _ in range(9 * len(self._players)):
            self._placePiece()
            self._logger.info(self._board)
            self._switchPlayer()

        # MOVING OF PIECES
        while True:
            if self._currentPlayer.pieces < 3:
                self._logger.info(f"{self._currentPlayer} has less than 3 pieces left.")
                break
            self._logger.info(f"{self._currentPlayer}'s turn to move: ")
            if not self._movePiece():  # if there were no options
                self._logger.info(f"{self._currentPlayer} has no pieces that can move.")
                break
            self._logger.info(self._board)
            self._switchPlayer()

        # WINNER DECLARATION
        self._switchPlayer()
        self._logger.info(f"{self._currentPlayer} wins!\n")

    def _switchPlayer(self):
        self._activePlayerIndex = (self._activePlayerIndex + 1) % len(self._players)
        self._currentPlayer = self._players[self._activePlayerIndex]

    def _placePiece(self):
        self._logger.info(f"{self._currentPlayer}'s turn to place a piece.")
        selection = self._currentPlayer.getDecision(self._board.getAvailablePositions())
        placeEvent = Place(selection, self._currentPlayer)
        placeEvent.execute(self._board)
        self._checkForMills(selection)

    def _removePiece(self):
        self._logger.info(f"{self._currentPlayer}'s turn to remove a piece.")
        removeablePieces = self._board.getRemoveableLocations(self._currentPlayer)
        self._logger.info(f"Available pieces to remove: {removeablePieces}")
        selection = self._currentPlayer.getDecision(removeablePieces)
        removeEvent = Remove(selection, self._currentPlayer)
        removeEvent.execute(self._board)

    def _movePiece(self) -> bool:
        piecesAdjacentSpots = self._board.getPiecesThatCanMove(self._currentPlayer)
        if not piecesAdjacentSpots:
            self._logger.info(f"{self._currentPlayer} has no pieces that can move.")
            return False

        pieceLocations = list(piecesAdjacentSpots.keys())
        self._logger.info(f"Available pieces to move: {pieceLocations}")
        selection = self._currentPlayer.getDecision(pieceLocations)

        newSpots = piecesAdjacentSpots[selection] if self._currentPlayer.pieces > 3 else self._board.getAvailablePositions()
        self._logger.info(f"Available spots: {newSpots}")
        newPlace = self._currentPlayer.getDecision(newSpots)

        moveEvent = Move(selection, newPlace, self._currentPlayer)
        moveEvent.execute(self._board)

        self._checkForMills(newPlace)

        return True

    def _checkForMills(self, position: int):
        millsFormed = self._board.getMillsFormed(position)
        if millsFormed:
            self._logger.info(f"{self._currentPlayer} formed {millsFormed} mill{'s' if millsFormed > 1 else ''}!")
        for _ in range(millsFormed):
            self._removePiece()
