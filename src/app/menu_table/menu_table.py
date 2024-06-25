import curses
from enum import Enum
from typing import TYPE_CHECKING


class MenuChoice(Enum, int):
    IMAGES = 0
    CONTAINERS = 1


class MenuTable:

    def __init__(self):
        self.choice: int = MenuChoice.IMAGES

    def change_choice(self):
        if bool(self.choice):
            self.choice = MenuChoice.IMAGES
        else:
            self.choice = MenuChoice.CONTAINERS

    def put_table_on_screen(self, stdscr):
        if TYPE_CHECKING:
            stdscr = curses.initscr()


