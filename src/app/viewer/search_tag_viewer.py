import curses

from .base import ABSViewer
from ..docker_communicator.docker_api_communicator import DockerApiCommunicator
from ..docker_communicator.docker_comunicator import DockerCommunicator
from ..utils.constants import KEY_EXIT, KEY_ESC, KEY_STEPS_DICT, KEY_ENTER, ICON, HELP_TEXT, KEY_LATEST
from ..utils.enams import Steps, QueryParams
from ..utils.hints import TagResponse
from ..utils.index import ObjIndex
from ..utils.mixins import MenuMixin, TablesMixin, UrlMixin


class SearchTagViewer(ABSViewer, MenuMixin, TablesMixin, UrlMixin):

    def __init__(self, screen: curses.window, obj_name: str, api_communicator: DockerApiCommunicator):
        self.index: ObjIndex = ObjIndex()
        self.docker_communicator: DockerCommunicator = DockerCommunicator()
        self.api_communicator: DockerApiCommunicator = api_communicator
        self.stdscr = screen
        self.name = obj_name if '/' in obj_name else "library" + "/" + obj_name
        self.data: TagResponse = self.api_communicator.get_tags(self.name)
        self.page_number: int = 1
        self.key_steps_dict: dict[int, Steps] = KEY_STEPS_DICT

    def get_tables(self) -> list[str]:
        tags = [
            d['name'] for d in self.data['results']
        ]
        return tags

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

    def get_page_information(self) -> str:
        if self.data:
            if self.data['count']:
                if self.data['count'] % 10 == 0:
                    return f"{self.page_number}/{self.data['count'] // 10}"
                else:
                    return f"{self.page_number}/{(self.data['count'] // 10) + 1}"
        return "0/0"

    def icon_to_screen(self, help_text: bool = False):
        """
        Displays an icon on the screen and optionally adds help text.

        This method clears the current content of the screen and adds
        the specified icon to the screen. If the `help_text` parameter
        is set to True, it also adds additional help text below the icon.
        After updating the screen with the new content, it refreshes
        the display to show the icon and any help text.

        Args:
            help_text (bool): A flag indicating whether to display
                              additional help text. Defaults to False.
        """
        self.stdscr.clear()
        self.stdscr.addstr(ICON)
        if help_text:
            self.stdscr.addstr(HELP_TEXT)
        self.stdscr.refresh()

    def get_tag(self) -> str:
        return self.get_tables()[self.index.value]

    def run(self):
        while True:
            try:
                self.stdscr.clear()
                self.put_head_menu(screen=self.stdscr, title=self.name)
                self.put_tables(screen=self.stdscr, tables=self.get_tables(), index=self.index.value)
                self.put_footer(screen=self.stdscr, center_text=self.get_page_information())

                char = self.stdscr.getch()

                if char in (KEY_EXIT, KEY_ESC):
                    return

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
                    self.data = self.api_communicator.get_tags(self.name, page)
                if char == curses.KEY_RIGHT and self.data and self.data['next']:
                    page = int(
                        self.get_query_param_from_url(
                            url=self.data['next'],
                            query_param_name=QueryParams.PAGE.value
                        )
                    )
                    self.page_number = page
                    self.data = self.api_communicator.get_tags(self.name, page)

                if char == KEY_ENTER:
                    self.icon_to_screen()
                    self.docker_communicator.pull(self.name + ":" + self.get_tag())

                if char == KEY_LATEST:
                    self.icon_to_screen()
                    self.docker_communicator.pull(self.name + ":" + "latest")

            except KeyboardInterrupt:
                return