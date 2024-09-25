from curses.ascii import isalpha, ispunct, isdigit
from typing import Optional

from .base import ABSViewer
from .search_tag_viewer import SearchTagViewer
from ..docker_communicator.docker_api_communicator import DockerApiCommunicator
from ..utils.constants import *
from ..utils.enams import Steps, QueryParams
from ..utils.hints import ImageResponse
from ..utils.index import ObjIndex
from ..utils.mixins import MenuMixin, UrlMixin, TablesMixin


class SearchImageViewer(ABSViewer, MenuMixin, UrlMixin, TablesMixin):

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

                self.put_tables(
                    screen=self.stdscr,
                    tables=self.get_tables(),
                    index=self.index.value
                )
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

                if char == KEY_ENTER and self.get_tables():
                    search_tag_viewer = SearchTagViewer(
                        screen=self.stdscr,
                        obj_name=self.get_tables()[self.index.value],
                        api_communicator=self.api_communicator
                    )
                    search_tag_viewer.run()


                elif isalpha(char) or ispunct(char) or isdigit(char):
                    self.text += chr(char)
                    self.data = self.api_communicator.get_repositories(self.text)
                    self.page_number = 1
            except KeyboardInterrupt:
                return