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
    """
    A viewer class for searching and displaying Docker images in a terminal interface.
    It handles user input, displays search results, and allows navigation through pages of results.
    """

    def __init__(self, screen: curses.window):
        """
        Initializes the SearchImageViewer with the given curses window.

        Args:
            screen (curses.window): The curses window object for rendering the interface.
        """
        self.stdscr = screen
        self.text: str = EMPTY_STRING
        self.data: Optional[ImageResponse] = None
        self.index: ObjIndex = ObjIndex()
        self.key_steps_dict: dict[int, Steps] = KEY_STEPS_DICT
        self.api_communicator = DockerApiCommunicator()
        self.page_number: int = START_PAGE_NUMBER

    def get_tables(self) -> list[str]:
        """
        Retrieves the list of Docker image repository names from the current data.

        Returns:
            list[str]: A list of repository names if data is available, otherwise an empty list.
        """
        if self.data:
            return [d['repo_name'] for d in self.data['results']]
        return []

    def get_page_information(self) -> str:
        """
        Generates a string representing the current page information.

        Returns:
            str: A string in the format "current_page/total_pages".
        """
        if self.data:
            if self.data['count']:
                if self.data['count'] % PAGE_SIZE == 0:
                    return f"{self.page_number}/{self.data['count'] // PAGE_SIZE}"
                else:
                    return f"{self.page_number}/{(self.data['count'] // PAGE_SIZE) + 1}"
        return NO_PAGES

    def backspace(self):
        """
        Removes the last character from the current search text.
        """
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
        """
        Main loop for running the SearchImageViewer. It handles user input,
        updates the display, and manages navigation through search results.
        """
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
                    self.page_number = START_PAGE_NUMBER
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
                    self.page_number = START_PAGE_NUMBER

            except KeyboardInterrupt:
                return
