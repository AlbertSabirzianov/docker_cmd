from curses.ascii import isalpha, ispunct, isdigit
from typing import Optional

from .base import ABSViewer
from ..docker_communicator.docker_api_communicator import DockerApiCommunicator
from ..utils.constants import *
from ..utils.enams import Colors, Steps, QueryParams
from ..utils.hints import ImageResponse
from ..utils.index import ObjIndex
from ..utils.mixins import MenuMixin, UrlMixin


class SearchImageViewer(ABSViewer, MenuMixin, UrlMixin):

    def __init__(self, screen: curses.window):
        self.stdscr = screen
        self.text: str = EMPTY_STRING
        self.data: Optional[ImageResponse] = None
        self.index: ObjIndex = ObjIndex()
        self.key_steps_dict: dict[int, Steps] = KEY_STEPS_DICT
        self.api_communicator = DockerApiCommunicator()
        self.page_number: int = 1

    def get_tables(self) -> list[str]:
        if self.data:
            return [d['repo_name'] for d in self.data['results']]
        return []

    def get_page_information(self) -> str:
        if self.data:
            if self.data['count']:
                if self.data['count'] % 10 == 0:
                    return f"{self.page_number}/{self.data['count'] // 10}"
                else:
                    return f"{self.page_number}/{(self.data['count'] // 10) + 1}"
        return "0/0"

    def put_tables(self):
        tables: list[str] = self.get_tables()
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

    def backspace(self):
        self.text = self.text[:-1]

    def change_index(self, char: int) -> None:
        """
        Changes the selected Docker entity index based on the given character input.

        Parameters:
        - char: An integer representing the character input from the user.
        """
        step: int = self.key_steps_dict[char]
        self.index.value += step
        max_value = len(self.get_tables()) - 1
        if self.index.value > max_value:
            self.index.clear()
        elif self.index.value < 0:
            self.index.value = max_value

    def run(self):
        while True:
            try:
                self.stdscr.clear()
                if self.text:
                    self.put_head_menu(self.stdscr, self.text)
                else:
                    self.put_head_menu(self.stdscr, CURS + START_TYPE_NAME)

                self.put_tables()
                self.put_footer(
                    screen=self.stdscr,
                    center_text=self.get_page_information()
                )

                char = self.stdscr.getch()

                if char in (KEY_EXIT, KEY_ESC):
                    return
                if char == curses.KEY_BACKSPACE:
                    self.backspace()
                    self.page_number = 1
                    self.data = self.api_communicator.get_repositories(self.text)

                if char in (curses.KEY_DOWN, curses.KEY_UP):
                    self.change_index(char)

                if char == curses.KEY_LEFT and self.data and self.data['previous']:
                    page = int(
                        self.get_query_param_from_url(
                            url=self.data['previous'],
                            query_param_name=QueryParams.PAGE.value
                        )
                    )
                    self.page_number = page
                    self.data = self.api_communicator.get_repositories(self.text, page)
                if char == curses.KEY_RIGHT and self.data and self.data['next']:
                    page = int(
                        self.get_query_param_from_url(
                            url=self.data['next'],
                            query_param_name=QueryParams.PAGE.value
                        )
                    )
                    self.page_number = page
                    self.data = self.api_communicator.get_repositories(self.text, page)



                elif isalpha(char) or ispunct(char) or isdigit(char):
                    self.text += chr(char)
                    self.data = self.api_communicator.get_repositories(self.text)
                    self.page_number = 1
            except KeyboardInterrupt:
                return