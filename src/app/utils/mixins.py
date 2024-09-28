"""
This module provides a mixin classes.
"""
import curses
from typing import Union
from urllib.parse import urlparse, parse_qs

from ..utils.constants import *
from ..utils.enams import Colors


class MenuMixin:
    """
    A mixin class that provides methods for rendering a menu in a curses-based terminal application.
    """
    @staticmethod
    def put_footer(screen: curses.window, center_text: str):
        """
        Renders a footer at the bottom of the screen.

        Args:
            screen (curses.window): The curses window object where the footer will be drawn.
            center_text (str): The text to display in the center of the footer.
        """
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
    """
    A mixin class that provides methods for rendering tables in a curses-based terminal application.
    """

    @staticmethod
    def put_tables(screen: curses.window, tables: list[str], index: int):
        """
        Renders a list of tables on the given screen.

        Args:
            screen (curses.window): The curses window object where the tables will be drawn.
            tables (list[str]): A list of table strings to display.
            index (int): The index of the currently selected table.
        """
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
    """
    A mixin class that provides methods for handling URLs and their query parameters.
    """

    @staticmethod
    def put_tables_from_dict_or_list(data: Union[dict, list], result: list, indent: int = 0) -> None:
        """
        Recursively formats a dictionary or list into a string representation
        and appends it to the result list.

        Args:
            data (Union[dict, list]): The input data, which can be a dictionary or a list.
            result (list): The list to which the formatted strings will be appended.
            indent (int): The current indentation level for formatting (default is 0).

        This function handles nested dictionaries and lists, formatting them
        with appropriate indentation. Keys are followed by their values, and
        nested structures are indented further.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list) or isinstance(value, dict):
                    result.append(
                        SPACE*indent + str(key) + COLON
                    )
                    UrlMixin.put_tables_from_dict_or_list(
                        value,
                        result,
                        indent + 4
                    )
                else:
                    result.append(
                        SPACE*indent + str(key) + COLON + SPACE + str(value)
                    )
        if isinstance(data, list):
            for value in data:
                if isinstance(value, list) or isinstance(value, dict):
                    UrlMixin.put_tables_from_dict_or_list(
                        value,
                        result,
                        indent + 4
                    )
                else:
                    result.append(
                        SPACE*indent + str(value)
                    )

    @staticmethod
    def get_inspect_tables_from_json_string(string: str) -> list[str]:
        """
        Parses the inspection JSON string and extracts relevant tables.

        This private method removes unwanted characters from the JSON string
        and splits it into a list of non-empty strings representing tables.

        Args:
            string (str): The JSON string containing inspection data.

        Returns:
            list[str]: A list of parsed table strings.
        """
        replayed_strings: list[str] = [
            '"',
            ",",
            "{",
            "}",
            "[",
            "]",
        ]
        parsed_str: str = string
        for s in replayed_strings:
            parsed_str = parsed_str.replace(
                s,
                EMPTY_STRING
            )
        return [
            s[8:] for s in parsed_str.split(END_OF_LINE) if s.strip()
        ]

    @staticmethod
    def get_query_param_from_url(url: str, query_param_name: str) -> str:
        """
        Extracts a specific query parameter from a given URL.

        Args:
            url (str): The URL from which to extract the query parameter.
            query_param_name (str): The name of the query parameter to extract.

        Returns:
            str: The value of the query parameter, or None if it does not exist.
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get(query_param_name, [None])[0]




