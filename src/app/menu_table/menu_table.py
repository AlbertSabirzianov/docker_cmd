"""
This module contains the MenuTable class,
which is used to create a menu table using the curses library in Python.
"""
import curses

from ..utils.enams import MenuChoice, Colors


class MenuTable:
    """A class representing a menu table in a terminal using curses."""

    def __init__(self):
        """Initialize the MenuTable object."""
        self.choice: int = MenuChoice.IMAGES

    def is_images(self) -> bool:
        """Check if the current choice is 'Images'."""
        return self.choice == MenuChoice.IMAGES

    def change_choice(self):
        """Toggle between 'Images' and 'Containers' choices."""
        if self.is_images():
            self.choice = MenuChoice.CONTAINERS
        else:
            self.choice = MenuChoice.IMAGES

    def put_table_on_screen(self, stdscr: curses.window) -> None:
        """
        Display the menu table on the screen.

        Args:
            stdscr (curses.window): The main window object.

        """
        _, width = stdscr.getmaxyx()
        center = width // 2

        images_color = Colors.WHITE_ON_BLUE if self.is_images() else Colors.WHITE_ON_BLACK
        containers_color = Colors.WHITE_ON_BLACK if self.is_images() else Colors.WHITE_ON_BLUE

        stdscr.addstr(0, 0, "+" + "-" * (center - 1), curses.color_pair(images_color))
        stdscr.addstr(0, center, "+" + "-" * (width - 1), curses.color_pair(containers_color))
        stdscr.addstr("\n")
        stdscr.addstr(1, 0, "Images" + " " * abs(center - 6), curses.color_pair(images_color))
        stdscr.addstr(1, center, "Containers" + " " * abs(center - 10), curses.color_pair(containers_color))
        stdscr.addstr("\n")


menu_table = MenuTable()
