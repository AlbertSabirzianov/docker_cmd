from enum import Enum


class Colors(int, Enum):
    WHITE_ON_BLUE = 1
    WHITE_ON_BLACK = 2
    WHITE_ON_YELLOW = 3


class MenuChoice(int, Enum):
    IMAGES = 1
    CONTAINERS = 0
