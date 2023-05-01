from typing import Literal

TCOLOUR = Literal["green", "yellow", "blue", "magenta", "cyan", "white"]

COLOURS: dict[TCOLOUR, str] = {
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}


def colourText(text: str, colour: TCOLOUR) -> str:
    return f"{COLOURS[colour]}{text}\033[0m"
