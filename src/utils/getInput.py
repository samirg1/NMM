from typing import Callable, Type, TypeVar

from utils.LogManager import LogManager

_T = TypeVar("_T")


def getInput(prompt: str, type: Type[_T], error: str = "", criteria: Callable[[_T], bool] = lambda _: True) -> _T:
    while True:
        try:
            LogManager.get().info(prompt, end="")
            value = type(input())
            if not criteria(value):
                raise ValueError
            return value
        except ValueError:
            LogManager.get().error(error)
