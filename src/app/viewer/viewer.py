import curses
from typing import TYPE_CHECKING

from ..docker_communicator.docker_comunicator import docker_communicator, DockerCommunicator
from ..exeptions.exeptions import DockerNotRunningError
from ..menu_table.menu_table import menu_table, MenuTable, MenuChoice
from ..utils.constants import DOCKER_NOT_INSTALL_TEXT, KEY_EXIT, KEY_ESC, KEY_REFRESH, KEY_ENTER, KEY_SPASE, \
    MAKE_FULL_SCREEN_TEXT, KEY_DELETE
from ..utils.utils import get_image
from ..utils.enams import Colors


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

    def get_number_of_images(self) -> int:
        return len(self.docker_communicator.images().split("\n"))

    def get_number_of_containers(self) -> int:
        return len(self.docker_communicator.containers().split("\n"))

    def check_indexes(self):
        if self.image_index < 0 or self.image_index > self.get_number_of_images() - 3:
            self.image_index = 0
        if (self.container_index < 0
                or self.container_index > self.get_number_of_containers() - 3):
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

    def is_images(self) -> bool:
        return self.menu_table.choice == MenuChoice.IMAGES

    def put_main_table(self):
        tables: list[str] = self.get_tables().split("\n")
        cursor_index = self.image_index if self.is_images() \
            else self.container_index
        underline_indexes = self.underlined_images if self.is_images() \
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
                self.stdscr.addstr(table[:width-8], curses.A_BLINK)
            else:
                self.stdscr.addstr(table[:width-8])
            self.stdscr.addstr("\n")

    def add_underline(self):
        index = self.image_index if self.is_images() else self.container_index
        underlined = self.underlined_images if self.is_images() else self.underlined_containers

        if index not in underlined:
            underlined.append(index)
        else:
            underlined.remove(index)

    def get_id_by_index(self, index: int):
        tables: list[str] = self.get_tables().split("\n")
        tables.pop(0)
        if self.is_images():
            try:
                items = [item for item in tables[index].split() if item]
                return items[2]
            except IndexError:
                return None

    def delete(self):
        if self.is_images():
            if not self.underlined_images:
                self.docker_communicator.delete_image(
                    self.get_id_by_index(self.image_index)
                )

    def put_icon_on_screen(self):
        self.stdscr.addstr(get_image())

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

                if char == KEY_REFRESH:
                    self.update()
                if char in (KEY_SPASE, KEY_ENTER):
                    self.add_underline()

                if char == KEY_DELETE:
                    self.stdscr.clear()
                    self.put_icon_on_screen()
                    self.stdscr.refresh()
                    self.delete()
                    self.update()

                self.check_indexes()

            except curses.error:
                self.stdscr.clear()
                self.stdscr.addstr(MAKE_FULL_SCREEN_TEXT)
                self.stdscr.refresh()
                if self.stdscr.getch() in (KEY_EXIT, KEY_ESC):
                    return
            except DockerNotRunningError:
                self.stdscr.clear()
                self.stdscr.addstr(DOCKER_NOT_INSTALL_TEXT)
                self.stdscr.refresh()
                self.stdscr.getch()
                return
