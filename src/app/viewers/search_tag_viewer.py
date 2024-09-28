from .base import ABSViewer
from .inspect_viewer import InspectViewer
from ..docker_communicators.docker_api_communicator import DockerApiCommunicator
from ..docker_communicators.docker_comunicator import DockerCommunicator
from ..utils.constants import *
from ..utils.enams import Steps, QueryParams
from ..utils.hints import TagResponse
from ..utils.index import ObjIndex
from ..utils.mixins import MenuMixin, TablesMixin, UrlMixin


class SearchTagViewer(ABSViewer, MenuMixin, TablesMixin, UrlMixin):
    """
    A viewers class for searching and displaying Docker image tags in a terminal interface.
    It handles user input, displays search results, and allows navigation through pages of tags.
    """

    def __init__(self, screen: curses.window, obj_name: str, api_communicator: DockerApiCommunicator):
        """
        Initializes the SearchTagViewer with the given curses window and object name.

        Args:
            screen (curses.window): The curses window object for rendering the interface.
            obj_name (str): The name of the Docker object (image) to search for.
            api_communicator (DockerApiCommunicator): The API communicator for fetching tags.
        """
        self.index: ObjIndex = ObjIndex()
        self.docker_communicator: DockerCommunicator = DockerCommunicator()
        self.api_communicator: DockerApiCommunicator = api_communicator
        self.stdscr = screen
        self.name = obj_name if SLASH in obj_name else LIBRARY + SLASH + obj_name
        self.data: TagResponse = self.api_communicator.get_tags(self.name)
        self.page_number: int = START_PAGE_NUMBER
        self.key_steps_dict: dict[int, Steps] = KEY_STEPS_DICT

    def get_tables(self) -> list[str]:
        """
        Retrieves the list of Docker image tags from the current data.

        Returns:
            list[str]: A list of tag names if data is available, otherwise an empty list.
        """
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
        """
        Retrieves the currently selected tag based on the index.

        Returns:
            str: The name of the currently selected tag.
        """
        return self.get_tables()[self.index.value]

    def run(self):
        """
        Main loop for running the SearchTagViewer. It handles user input,
        updates the display, and manages navigation through search results.
        """
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
                    self.index.clear()

                if char == curses.KEY_RIGHT and self.data and self.data['next']:
                    page = int(
                        self.get_query_param_from_url(
                            url=self.data['next'],
                            query_param_name=QueryParams.PAGE.value
                        )
                    )
                    self.page_number = page
                    self.data = self.api_communicator.get_tags(self.name, page)
                    self.index.clear()

                if char == KEY_ENTER:
                    self.icon_to_screen()
                    self.docker_communicator.pull(self.name + COLON + self.get_tag())

                if char == KEY_LATEST:
                    self.icon_to_screen()
                    self.docker_communicator.pull(self.name + COLON + LATEST)

                if char in (KEY_SPASE, KEY_INSPECT):
                    tags_tables: list[str] = []
                    data = self.data["results"][self.index.value]
                    self.put_tables_from_dict_or_list(data, tags_tables)
                    inspect_viewer = InspectViewer(
                        screen=self.stdscr,
                        obj_name=self.get_tables()[self.index.value],
                        tables=tags_tables
                    )
                    inspect_viewer.run()

            except KeyboardInterrupt:
                return
