"""
Module: inspect_viewer

The inspect_viewer module provides a InspectViewer class for managing and interacting with
Docker images, containers Inspect Information. It provides functionality to display
information about Docker images, containers Inspect Information and manipulate them through the terminal.
"""

from .base import ABSViewer
from ..utils.constants import *
from ..utils.enams import Steps
from ..utils.index import ObjIndex
from ..utils.mixins import MenuMixin, TablesMixin


class InspectViewer(ABSViewer, MenuMixin, TablesMixin):
    """
    A viewers class for displaying inspection details of Docker entities.

    This class inherits from ABSViewer and MenuMixin, providing functionality
    to visualize the inspection data of Docker containers or images in a terminal
    interface using the curses library.
    """

    def __init__(self, screen: curses.window, tables: list[str], obj_name: str):
        """
        Initializes the InspectViewer with the given screen and inspection data.

        Args:
            screen (curses.window): The curses window object for rendering.
            tables list[str]: The list of strings containing inspection data.
            obj_name (str): The name of the Docker object being inspected.
        """
        self.stdscr = screen
        self.obj_name: str = obj_name
        self.tables: list[str] = tables
        self.index: ObjIndex = ObjIndex()
        self.key_steps_dict: dict[int, Steps] = KEY_STEPS_DICT

    def put_menu_on_screen(self):
        """
        Displays the header menu on the screen with the object name.
        """
        self.put_head_menu(
            screen=self.stdscr,
            title=self.obj_name
        )

    def change_index(self, char: int) -> None:
        """
        Changes the selected Docker entity index based on the given character input.

        Parameters:
        - char: An integer representing the character input from the user.
        """
        step: int = self.key_steps_dict[char]
        self.index.value += step
        max_value = len(self.tables) - 1
        if self.index.value > max_value:
            self.index.clear()
        elif self.index.value < 0:
            self.index.value = max_value

    def run(self):
        """
        Runs the main loop for the InspectViewer, handling user input and rendering.

        This method continuously refreshes the screen, displays the menu and
        inspection tables, and processes user input for navigation and exit.
        """
        while True:
            try:
                self.stdscr.clear()
                self.put_menu_on_screen()
                self.put_tables(
                    screen=self.stdscr,
                    tables=self.tables,
                    index=self.index.value
                )
                self.stdscr.refresh()

                char = self.stdscr.getch()

                if char in (KEY_EXIT, KEY_ESC):
                    return

                if char in (curses.KEY_DOWN, curses.KEY_UP):
                    self.change_index(char)

            except KeyboardInterrupt:
                return



