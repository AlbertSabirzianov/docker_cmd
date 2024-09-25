"""
This module provides a mixin classes.
"""
import curses
from urllib.parse import urlparse, parse_qs

from pexpect.screen import screen

from ..utils.constants import *
from ..utils.enams import Colors


class MenuMixin:
    """
    A mixin class that provides methods for rendering a menu in a curses-based terminal application.
    """
    @staticmethod
    def put_footer(screen: curses.window, center_text: str):
        height, width = screen.getmaxyx()

        # Значения для вывода
        left_value = "<"
        center_value = center_text
        right_value = ">"

        screen.addstr(height - 1, 0, left_value, curses.color_pair(Colors.WHITE_ON_YELLOW))  # Внизу слева
        screen.addstr(height - 1, (width // 2) - (len(center_value) // 2), center_value, curses.color_pair(Colors.WHITE_ON_YELLOW))  # По центру
        screen.addstr(height - 1, width - len(right_value) - 1, right_value, curses.color_pair(Colors.WHITE_ON_YELLOW))

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


class TablesMixin:

    @staticmethod
    def put_tables(screen: curses.window, tables: list[str], index: int):
        tables: list[str] = tables
        cursor_index: int = index

        height, width = screen.getmaxyx()

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
                screen.addstr(table[:width - 8], curses.color_pair(Colors.WHITE_ON_YELLOW))
            else:
                screen.addstr(table[:width - 8])
            screen.addstr(END_OF_LINE)


class UrlMixin:

    @staticmethod
    def get_query_param_from_url(url: str, query_param_name: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get(query_param_name, [None])[0]




