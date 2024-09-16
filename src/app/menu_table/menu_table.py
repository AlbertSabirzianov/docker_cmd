"""
This module contains the MenuTable class,
which is used to create a menu table using the curses library in Python.
"""
import curses

from ..utils.constants import END_OF_LINE, PLUS, DASH, SPACE
from ..utils.enams import MenuChoice, Colors, MenuChoiceNames


class MenuTable:
    """A class representing a menu table in a terminal using curses."""

    def __init__(self):
        """Initialize the MenuTable object."""
        self.choice: MenuChoice = MenuChoice.IMAGES

        self.choice_names_dict: dict[MenuChoice, MenuChoiceNames] = {
            MenuChoice.IMAGES: MenuChoiceNames.IMAGES,
            MenuChoice.CONTAINERS: MenuChoiceNames.CONTAINERS,
            MenuChoice.VOLUMES: MenuChoiceNames.VOLUMES
        }

        self.next_choice_dict: dict[MenuChoice, MenuChoice] = {
            MenuChoice.IMAGES: MenuChoice.CONTAINERS,
            MenuChoice.CONTAINERS: MenuChoice.VOLUMES,
            MenuChoice.VOLUMES: MenuChoice.IMAGES
        }

        self.prev_choice_dict: dict[MenuChoice, MenuChoice] = {
            value: key for key, value in self.next_choice_dict.items()
        }

    @property
    def choice_name(self) -> MenuChoiceNames:
        return self.choice_names_dict[self.choice]

    def is_images(self) -> bool:
        """Check if the current choice is 'Images'."""
        return self.choice == MenuChoice.IMAGES

    def change_choice_next(self):
        """Toggle between 'Images' and 'Containers' choices."""
        self.choice = self.next_choice_dict[self.choice]

    def change_choice_prev(self):
        self.choice = self.prev_choice_dict[self.choice]

    def put_table_on_screen(self, stdscr: curses.window) -> None:
        """
        Display the menu table on the screen.

        Args:
            stdscr (curses.window): The main window object.

        """
        _, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, PLUS + DASH * (width - 2) + PLUS, curses.color_pair(Colors.WHITE_ON_BLUE))
        stdscr.addstr(END_OF_LINE)
        stdscr.addstr(1, 0, self.choice_name + SPACE * abs(width - len(self.choice_name)), curses.color_pair(Colors.WHITE_ON_BLUE))
        stdscr.addstr(END_OF_LINE)
        stdscr.addstr(2, 0, PLUS + DASH * (width - 2) + PLUS, curses.color_pair(Colors.WHITE_ON_BLUE))
        stdscr.addstr(END_OF_LINE)


menu_table = MenuTable()
