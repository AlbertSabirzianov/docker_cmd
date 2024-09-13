"""
Module: viewer

This module provides a Viewer class that represents a viewer for Docker images and containers.
It provides functionality for displaying and interacting with the Docker images and containers in a terminal window.
"""
import curses
import platform
from typing import Callable

from ..docker_communicator.docker_comunicator import docker_communicator, DockerCommunicator
from ..exeptions.exeptions import DockerNotRunningError
from ..menu_table.menu_table import menu_table, MenuTable
from ..utils.constants import DOCKER_NOT_INSTALL_TEXT, KEY_EXIT, KEY_ESC, KEY_REFRESH, KEY_ENTER, KEY_SPASE, \
    MAKE_FULL_SCREEN_TEXT, KEY_DELETE, KEY_HELP, ICON, HELP_TEXT, KEY_SAVE, KEY_EXPORT, TAR_ARCHIVE_EXTENSION
from ..utils.enams import Colors, OperatingSystems


class Viewer:
    """
    The Viewer class represents a viewer for Docker images and containers.
    """

    def __init__(self, stdscr: curses.window):
        """
        Initializes an instance of the Viewer class.

        Parameters:
        - stdscr: A curses.window object representing the terminal window.
        """
        self.stdscr: curses.window = stdscr
        self.underline_color: int = curses.A_BLINK if self.is_windows() else curses.A_DIM

        self.image_id_index: int = 2
        self.image_name_index: int = 0
        self.container_id_index: int = 0
        self.container_name_index: int = -1

        self.docker_communicator: DockerCommunicator = docker_communicator
        self.menu_table: MenuTable = menu_table

        self.image_index: int = 0
        self.container_index: int = 0

        self.underlined_images: list[int] = list()
        self.underlined_containers: list[int] = list()

    @staticmethod
    def is_windows() -> bool:
        """
        Checks if the current platform is Windows.

        Returns:
        - A boolean value indicating whether the current platform is Windows.
        """
        return platform.system() == OperatingSystems.WINDOWS

    def get_number_of_images(self) -> int:
        """
        Gets the number of Docker images.

        Returns:
        - The number of Docker images.
        """
        return len(self.docker_communicator.images().split("\n"))

    def get_number_of_containers(self) -> int:
        """
        Gets the number of Docker containers.

        Returns:
        - The number of Docker containers.
        """
        return len(self.docker_communicator.containers().split("\n"))

    def check_indexes(self):
        """
        Checks and adjusts the image and container indexes to ensure they are within valid ranges.
        """
        if self.image_index < 0 or self.image_index > self.get_number_of_images() - 3:
            self.image_index = 0
        if (self.container_index < 0
                or self.container_index > self.get_number_of_containers() - 3):
            self.container_index = 0

    def update(self):
        """
        Updates the viewer by clearing the cache, resetting the image and container indexes,
        and clearing the underlined images and containers.
        """
        self.docker_communicator.cache_clear()
        self.image_index = 0
        self.container_index = 0
        self.underlined_images = list()
        self.underlined_containers = list()

    def get_tables(self) -> str:
        """
        Gets the tables of Docker images or containers.

        Returns:
        - A string representation of the Docker images or containers table.
        """
        if self.is_images():
            return self.docker_communicator.images()
        else:
            return self.docker_communicator.containers()

    def change_index(self, char: int) -> None:
        """
        Changes the image or container index based on the given character input.

        Parameters:
        - char: An integer representing the character input from the user.
        """
        step = 1 if char == curses.KEY_DOWN else -1

        if self.is_images():
            self.image_index += step
        else:
            self.container_index += step

    def is_images(self) -> bool:
        """
        Checks if the current choice is to display Docker images.

        Returns:
        - A boolean value indicating whether the current choice is to display Docker images.
        """
        return self.menu_table.is_images()

    def put_main_table(self):
        """
        Displays the main table of Docker images or containers in the terminal window.
        """
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
                self.stdscr.addstr(table[:width-8], self.underline_color)
            else:
                self.stdscr.addstr(table[:width-8])
            self.stdscr.addstr("\n")

    def add_underline(self):
        """
        Adds or removes an underline to the currently selected image or container.
        """
        index = self.image_index if self.is_images() else self.container_index
        underlined = self.underlined_images if self.is_images() else self.underlined_containers

        if index not in underlined:
            underlined.append(index)
        else:
            underlined.remove(index)

    def get_id_by_index(self, index: int):
        """
        Gets the ID of the Docker image or container at the given index.

        Parameters:
        - index: An integer representing the index of the Docker image or container.

        Returns:
        - The ID of the Docker image or container at the given index.
        """
        tables: list[str] = self.get_tables().split("\n")
        tables.pop(0)
        id_index = self.image_id_index if self.is_images() else self.container_id_index

        try:
            items = [item for item in tables[index].split() if item]
            return items[id_index]
        except IndexError:
            return None

    def get_name_by_index(self, index: int):
        """
        Gets the name of the Docker image or container at the given index.

        Parameters:
        - index: An integer representing the index of the Docker image or container.

        Returns:
        - The name of the Docker image or container at the given index.
        """
        tables: list[str] = self.get_tables().split("\n")
        tables.pop(0)
        id_index = self.image_name_index if self.is_images() else self.container_name_index

        try:
            items = [item for item in tables[index].split() if item]
            return items[id_index]
        except IndexError:
            return None

    def delete(self):
        """
        Deletes the selected Docker image or container.
        """
        index: int = self.image_index if self.is_images() else self.container_index
        underlines: list[int] = self.underlined_images if self.is_images() else self.underlined_containers
        docker_func: Callable = self.docker_communicator.delete_image if self.is_images() \
            else self.docker_communicator.delete_container

        if not underlines:
            docker_func(
                self.get_id_by_index(index)
            )
        else:
            for under_index in underlines:
                if self.get_id_by_index(under_index):
                    docker_func(
                        self.get_id_by_index(under_index)
                    )

    def save_image(self):
        """
        Saves the Docker image specified by the `image_index` attribute to a tar archive file.
        """
        try:
            self.docker_communicator.save_image(
                self.get_id_by_index(self.image_index),
                self.get_name_by_index(self.image_index) + TAR_ARCHIVE_EXTENSION
            )
        except TypeError:
            return

    def export_container(self):
        """
        Exports the Docker container specified by the `container_index` attribute to a tar archive file.
        """
        try:
            self.docker_communicator.export_container(
                self.get_id_by_index(self.container_index),
                self.get_name_by_index(self.container_index) + TAR_ARCHIVE_EXTENSION
            )
        except TypeError:
            return

    def run(self):
        """
        Runs the viewer in an infinite loop, continuously updating and refreshing the display based on user input.
        """

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
                    self.stdscr.addstr(ICON)
                    self.stdscr.refresh()
                    self.delete()
                    self.update()

                if char == KEY_HELP:
                    self.stdscr.clear()
                    self.stdscr.addstr(ICON)
                    self.stdscr.addstr(HELP_TEXT)
                    self.stdscr.refresh()
                    self.stdscr.getch()

                if char == KEY_SAVE and self.is_images():
                    self.stdscr.clear()
                    self.stdscr.addstr(ICON)
                    self.stdscr.refresh()
                    self.save_image()

                if char == KEY_EXPORT and not self.is_images():
                    self.stdscr.clear()
                    self.stdscr.addstr(ICON)
                    self.stdscr.refresh()
                    self.export_container()

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
