"""
Module: enums

This module defines two Enum classes: Colors and MenuChoice.

Colors:
    An enumeration of color options with corresponding integer values.

MenuChoice:
    An enumeration of menu choices with corresponding integer values.
"""
from enum import Enum


class Colors(int, Enum):
    """An enumeration of color options with corresponding integer values."""
    WHITE_ON_BLUE = 1
    WHITE_ON_BLACK = 2
    WHITE_ON_YELLOW = 3


class MenuChoice(int, Enum):
    """An enumeration of menu choices with corresponding integer values."""
    IMAGES = 1
    CONTAINERS = 0
