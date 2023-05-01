from classes import Game
from utils import LogManager

if __name__ == "__main__":
    LogManager.init()
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        LogManager.get().info("\n\nGame exited")
