from curses.ascii import ispunct, isalpha, isdigit

from .base import ABSViewer
from ..utils.constants import *
from ..utils.enams import Colors
from ..utils.mixins import MenuMixin


class GetNewNameViewer(ABSViewer, MenuMixin):
    """
    A viewers for obtaining a new name input from the user.

    This class provides a user interface for the user to input a new name
    using the curses library. It handles character input, backspace functionality,
    and displays the current input on the screen.

    Attributes:
        stdscr (curses.window): The curses window for displaying the interface.
        obj_name (str): The name of the object being renamed.
        new_name (str): The new name input by the user.
    """

    def __init__(self, screen: curses.window, obj_name: str):
        """
        Initializes the GetNewNameViewer with the given screen and object name.

        Args:
            screen (curses.window): The curses window to display the input interface.
            obj_name (str): The name of the object to be renamed.
        """
        self.stdscr = screen
        self.obj_name: str = obj_name
        self.new_name: str = EMPTY_STRING

    def backspace(self):
        """Removes the last character from the new name."""
        self.new_name = self.new_name[:-1]

    def add_char(self, char: str):
        """
        Adds a character to the new name.

        Args:
            char (str): The character to be added to the new name.
        """
        self.new_name += char

    def run(self) -> str:
        """
        Runs the viewers to get a new name from the user.

        This method displays the input interface, captures user input,
        and processes commands such as entering a new name, escaping,
        or using backspace. It returns the new name with spaces replaced by underscores.

        Returns:
            str: The new name input by the user, or an empty string if canceled.
        """
        while True:
            try:
                self.stdscr.clear()
                self.put_head_menu(screen=self.stdscr, title=self.obj_name)
                if self.new_name:
                    self.stdscr.addstr(CURS)
                    self.stdscr.addstr(self.new_name, curses.color_pair(Colors.WHITE_ON_YELLOW))
                else:
                    self.stdscr.addstr(CURS + START_TYPE_NAME)
                self.stdscr.refresh()

                char = self.stdscr.getch()

                if char == KEY_ENTER:
                    return self.new_name.replace(SPACE, DASH)
                if char == KEY_ESC:
                    return EMPTY_STRING
                if char == curses.KEY_BACKSPACE:
                    self.backspace()
                elif isalpha(char) or ispunct(char) or char == ord(SPACE) or isdigit(char):
                    self.add_char(char=chr(char))

            except KeyboardInterrupt:
                return EMPTY_STRING
