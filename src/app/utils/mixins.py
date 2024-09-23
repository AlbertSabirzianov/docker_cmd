"""
This module provides a mixin classes.
"""
from ..utils.constants import *
from ..utils.enams import Colors


class MenuMixin:
    """
    A mixin class that provides methods for rendering a menu in a curses-based terminal application.
    """

    @staticmethod
    def put_head_menu(screen: curses.window, title: str):
        """
        Renders the header menu on the given screen.

        This method draws a decorative header with a title at the top of the screen.
        It uses the curses library to handle terminal display and color.

        Args:
            screen (curses.window): The curses window object where the menu will be drawn.
            title (str): The title to display in the header menu.

        The header consists of a top border, the title centered within the available width,
        and a bottom border. The colors used are defined in the Colors enumeration.
        """
        _, width = screen.getmaxyx()

        screen.addstr(0, 0, PLUS + DASH * (width - 2) + PLUS, curses.color_pair(Colors.WHITE_ON_BLUE))
        screen.addstr(END_OF_LINE)
        screen.addstr(1, 0, title + SPACE * abs(width - len(title)),
                      curses.color_pair(Colors.WHITE_ON_BLUE))
        screen.addstr(END_OF_LINE)
        screen.addstr(2, 0, PLUS + DASH * (width - 2) + PLUS, curses.color_pair(Colors.WHITE_ON_BLUE))
        screen.addstr(END_OF_LINE)
