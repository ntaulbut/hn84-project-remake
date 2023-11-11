from os import system
from sys import platform


def clear() -> None:
    if platform == "win32":
        _ = system("cls")
    else:
        _ = system("clear")
