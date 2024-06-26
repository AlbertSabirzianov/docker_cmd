import curses
from typing import TYPE_CHECKING

from ..colors.colors import Colors
from ..docker_communicator.docker_comunicator import docker_communicator, DockerCommunicator
from ..exeptions.exeptions import DockerNotRunningError
from ..menu_table.menu_table import menu_table, MenuTable, MenuChoice
from ..utils.constants import DOCKER_NOT_INSTALL_TEXT, KEY_EXIT, KEY_ESC
from ..utils.utils import put_icon_on_screen


class Viewer:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        if TYPE_CHECKING:
            self.stdscr = curses.initscr()

        self.docker_communicator: DockerCommunicator = docker_communicator
        self.menu_table: MenuTable = menu_table

        self.image_index: int = 0
        self.container_index: int = 0

        self.underlined_images: list[int] = list()
        self.underlined_containers: list[int] = list()

    def check_indexes(self):
        if self.image_index < 0 or self.image_index > len(self.docker_communicator.images().split("\n")) - 3:
            self.image_index = 0
        if (self.container_index < 0
                or self.container_index > len(self.docker_communicator.containers().split("\n")) - 3):
            self.container_index = 0

    def update(self):
        self.docker_communicator.cache_clear()
        self.image_index = 0
        self.container_index = 0
        self.underlined_images = list()
        self.underlined_containers = list()

    def get_tables(self) -> str:
        if self.menu_table.choice == MenuChoice.IMAGES:
            return self.docker_communicator.images()
        else:
            return self.docker_communicator.containers()

    def change_index(self, char: int) -> None:
        if char == curses.KEY_DOWN:
            if self.menu_table.choice == MenuChoice.IMAGES:
                self.image_index += 1
            else:
                self.container_index += 1
        if char == curses.KEY_UP:
            if self.menu_table.choice == MenuChoice.IMAGES:
                self.image_index -= 1
            else:
                self.container_index -= 1

    def put_main_table(self):
        tables: list[str] = self.get_tables().split("\n")
        cursor_index = self.image_index if self.menu_table.choice == MenuChoice.IMAGES \
            else self.container_index
        underline_indexes = self.underlined_images if self.menu_table.choice == MenuChoice.IMAGES \
            else self.underlined_containers

        height, width = self.stdscr.getmaxyx()
        headers = tables.pop(0)
        self.stdscr.addstr(headers + "\n")

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
                self.stdscr.addstr(table[:width-8], curses.color_pair(Colors.WHITE_ON_YELLOW))
            elif ind in underline_indexes:
                self.stdscr.addstr(table[:width-8], curses.A_BOLD)
            else:
                self.stdscr.addstr(table[:width-8])
            self.stdscr.addstr("\n")


    def run(self):

        while True:
            try:
                self.stdscr.clear()

                self.menu_table.put_table_on_screen(self.stdscr)
                self.put_main_table()

                self.stdscr.refresh()
                char = self.stdscr.getch()

                if char in (KEY_EXIT, KEY_ESC):
                    return
                if char in (curses.KEY_RIGHT, curses.KEY_LEFT):
                    menu_table.change_choice()

                if char in (curses.KEY_DOWN, curses.KEY_UP):
                    self.change_index(char)
                self.check_indexes()

            except curses.error:
                self.stdscr.clear()
                # put_icon_on_screen(self.stdscr)
                self.stdscr.addstr("make the terminal full screen, please")
                self.stdscr.refresh()
                if self.stdscr.getch() in (KEY_EXIT, KEY_ESC):
                    return
            except DockerNotRunningError:
                self.stdscr.clear()
                self.stdscr.addstr(DOCKER_NOT_INSTALL_TEXT)
                self.stdscr.refresh()
                self.stdscr.getch()
                return
