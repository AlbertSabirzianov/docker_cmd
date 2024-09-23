"""
Module: inspect_viewer

The inspect_viewer module provides a InspectViewer class for managing and interacting with
Docker images, containers Inspect Information. It provides functionality to display
information about Docker images, containers Inspect Information and manipulate them through the terminal.
"""

from .base import ABSViewer
from ..utils.constants import *
from ..utils.enams import Colors, Steps
from ..utils.index import ObjIndex
from ..utils.mixins import MenuMixin


class InspectViewer(ABSViewer, MenuMixin):
    """
    A viewer class for displaying inspection details of Docker entities.

    This class inherits from ABSViewer and MenuMixin, providing functionality
    to visualize the inspection data of Docker containers or images in a terminal
    interface using the curses library.
    """

    REPLAYED_STRINGS: list[str] = [
        '"',
        ",",
        "{",
        "}",
        "[",
        "]",
    ]

    def __get_inspect_tables(self, string: str) -> list[str]:
        """
        Parses the inspection JSON string and extracts relevant tables.

        This private method removes unwanted characters from the JSON string
        and splits it into a list of non-empty strings representing tables.

        Args:
            string (str): The JSON string containing inspection data.

        Returns:
            list[str]: A list of parsed table strings.
        """
        parsed_str: str = string
        for s in self.REPLAYED_STRINGS:
            parsed_str = parsed_str.replace(
                s,
                EMPTY_STRING
            )
        return [
            s[8:] for s in parsed_str.split(END_OF_LINE) if s.strip()
        ]

    def __init__(self, screen: curses.window, tables_in_json: str, obj_name: str):
        """
        Initializes the InspectViewer with the given screen and inspection data.

        Args:
            screen (curses.window): The curses window object for rendering.
            tables_in_json (str): The JSON string containing inspection data.
            obj_name (str): The name of the Docker object being inspected.
        """
        self.stdscr = screen
        self.obj_name: str = obj_name
        self.tables: list[str] = self.__get_inspect_tables(tables_in_json)
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

    def put_main_table_in_screen(self):
        """
        Displays the main table of the selected Docker entity based on the current choice in the terminal window.

        This method handles the rendering of the inspection tables, highlighting
        the currently selected table based on the user's navigation.
        """
        tables: list[str] = self.tables
        cursor_index: int = self.index.value

        height, width = self.stdscr.getmaxyx()

        start = 0
        end = height - 9

        if cursor_index > end:
            start = cursor_index - height + 10
            end = start + end

        for ind, table in enumerate(tables):
            if ind < start:
                continue
            if ind > end:
                break
            if ind == cursor_index:
                self.stdscr.addstr(table[:width - 8], curses.color_pair(Colors.WHITE_ON_YELLOW))
            else:
                self.stdscr.addstr(table[:width - 8])
            self.stdscr.addstr(END_OF_LINE)

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
                self.put_main_table_in_screen()
                self.stdscr.refresh()

                char = self.stdscr.getch()

                if char in (KEY_EXIT, KEY_ESC):
                    return

                if char in (curses.KEY_DOWN, curses.KEY_UP):
                    self.change_index(char)

            except KeyboardInterrupt:
                return



