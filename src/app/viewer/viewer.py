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
from ..utils.constants import *
from ..utils.enams import Colors, OperatingSystems, MenuChoice, IdIndexes, NameIndexes, Steps


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

        self.docker_communicator: DockerCommunicator = docker_communicator
        self.menu_table: MenuTable = menu_table

        self.image_index: int = 0
        self.container_index: int = 0
        self.volume_index: int = 0

        self.underlined_images: list[int] = list()
        self.underlined_containers: list[int] = list()
        self.underlined_volumes: list[int] = list()

        self.choice_tables_func_dict: dict[MenuChoice, Callable] = {
            MenuChoice.IMAGES: self.docker_communicator.images,
            MenuChoice.CONTAINERS: self.docker_communicator.containers,
            MenuChoice.VOLUMES: self.docker_communicator.volumes
        }
        self.choice_delete_func_dict: dict[MenuChoice, Callable] = {
            MenuChoice.IMAGES: self.docker_communicator.delete_image,
            MenuChoice.CONTAINERS: self.docker_communicator.delete_container,
            MenuChoice.VOLUMES: self.docker_communicator.delete_volume_by_name
        }
        self.choice_underlines_dict: dict[MenuChoice, list[int]] = {
            MenuChoice.IMAGES: self.underlined_images,
            MenuChoice.CONTAINERS: self.underlined_containers,
            MenuChoice.VOLUMES: self.underlined_volumes
        }
        self.choice_id_index_dict: dict[MenuChoice, IdIndexes] = {
            MenuChoice.IMAGES: IdIndexes.IMAGE_ID_INDEX,
            MenuChoice.CONTAINERS: IdIndexes.CONTAINER_ID_INDEX,
            MenuChoice.VOLUMES: IdIndexes.VOLUME_ID_INDEX
        }
        self.choice_name_index_dict: dict[MenuChoice, NameIndexes] = {
            MenuChoice.IMAGES: NameIndexes.IMAGE_NAME_INDEX,
            MenuChoice.CONTAINERS: NameIndexes.CONTAINER_NAME_INDEX,
            MenuChoice.VOLUMES: NameIndexes.VOLUME_NAME_INDEX
        }
        self.key_steps_dict: dict[int, Steps] = {
            curses.KEY_DOWN: Steps.STEP_DOWN,
            curses.KEY_UP: Steps.STEP_UP
        }

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
        return len(self.docker_communicator.images().split(END_OF_LINE))

    def get_number_of_containers(self) -> int:
        """
        Gets the number of Docker containers.

        Returns:
        - The number of Docker containers.
        """
        return len(self.docker_communicator.containers().split(END_OF_LINE))

    def get_number_of_volumes(self) -> int:
        """
        Gets the number of Docker volumes.

        Returns:
        - The number of Docker containers.
        """
        return len(self.docker_communicator.volumes().split(END_OF_LINE))

    def check_indexes(self):
        """
        Checks and adjusts the image and container indexes to ensure they are within valid ranges.
        """
        if self.image_index < 0 or self.image_index > self.get_number_of_images() - 3:
            self.image_index = 0
        if (
                self.container_index < 0
                or self.container_index > self.get_number_of_containers() - 3
        ):
            self.container_index = 0
        if self.volume_index < 0 or self.volume_index > self.get_number_of_volumes() -3:
            self.volume_index = 0

    def update(self):
        """
        Updates the viewer by clearing the cache, resetting the image and container indexes,
        and clearing the underlined images and containers.
        """
        self.docker_communicator.cache_clear()
        self.image_index = 0
        self.container_index = 0
        self.volume_index = 0

        self.underlined_images = list()
        self.underlined_containers = list()
        self.underlined_volumes = list()

        self.choice_underlines_dict: dict[MenuChoice, list[int]] = {
            MenuChoice.IMAGES: self.underlined_images,
            MenuChoice.CONTAINERS: self.underlined_containers,
            MenuChoice.VOLUMES: self.underlined_volumes
        }

    def get_tables(self) -> str:
        """
        Gets the tables of Docker images or containers.

        Returns:
        - A string representation of the Docker images or containers table.
        """
        return self.choice_tables_func_dict[self.menu_table.choice]()

    def change_index(self, char: int) -> None:
        """
        Changes the image or container index based on the given character input.

        Parameters:
        - char: An integer representing the character input from the user.
        """
        step = self.key_steps_dict[char]

        if self.is_images():
            self.image_index += step
        elif self.is_containers():
            self.container_index += step
        else:
            self.volume_index += step

    def is_images(self) -> bool:
        """
        Checks if the current choice is to display Docker images.

        Returns:
        - A boolean value indicating whether the current choice is to display Docker images.
        """
        return self.menu_table.is_images()

    def is_containers(self) -> bool:
        """
        Checks if the current choice is to display Docker containers.

        Returns:
        - A boolean value indicating whether the current choice is to display Docker images.
        """
        return self.menu_table.choice == MenuChoice.CONTAINERS

    def is_volumes(self) -> bool:
        """
        Checks if the current choice is to display Docker volumes.

        Returns:
        - A boolean value indicating whether the current choice is to display Docker images.
        """
        return self.menu_table.choice == MenuChoice.VOLUMES

    def get_index(self):
        if self.is_images():
            return self.image_index
        elif self.is_containers():
            return self.container_index
        else:
            return self.volume_index

    def put_main_table(self):
        """
        Displays the main table of Docker images or containers in the terminal window.
        """
        tables: list[str] = self.get_tables().split(END_OF_LINE)
        cursor_index =  self.get_index()
        underline_indexes = self.choice_underlines_dict[self.menu_table.choice]

        height, width = self.stdscr.getmaxyx()
        headers = tables.pop(0)
        self.stdscr.addstr(headers + END_OF_LINE)

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
            self.stdscr.addstr(END_OF_LINE)

    def add_underline(self):
        """
        Adds or removes an underline to the currently selected image or container.
        """
        index = self.get_index()
        underlined = self.choice_underlines_dict[self.menu_table.choice]

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
        tables: list[str] = self.get_tables().split(END_OF_LINE)
        tables.pop(0)
        id_index = self.choice_id_index_dict[self.menu_table.choice]

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
        tables: list[str] = self.get_tables().split(END_OF_LINE)
        tables.pop(0)
        id_index = self.choice_name_index_dict[self.menu_table.choice]

        try:
            items = [item for item in tables[index].split() if item]
            return items[id_index]
        except IndexError:
            return None

    def delete(self):
        """
        Deletes the selected Docker image or container.
        """
        index: int = self.get_index()
        underlines: list[int] = self.choice_underlines_dict[self.menu_table.choice]
        docker_func: Callable = self.choice_delete_func_dict[self.menu_table.choice]

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
        indexes = self.underlined_images if self.underlined_images else [self.image_index]
        for index in indexes:
            try:
                self.docker_communicator.save_image(
                    self.get_id_by_index(index),
                    self.get_name_by_index(index) + TAR_ARCHIVE_EXTENSION
                )
            except TypeError:
                continue

    def export_container(self):
        """
        Exports the Docker container specified by the `container_index` attribute to a tar archive file.
        """
        indexes = self.underlined_containers if self.underlined_containers else [self.container_index]
        for index in indexes:
            try:
                self.docker_communicator.export_container(
                    self.get_id_by_index(index),
                    self.get_name_by_index(index) + TAR_ARCHIVE_EXTENSION
                )
            except TypeError:
                continue

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
                if char == curses.KEY_RIGHT:
                    menu_table.change_choice_next()
                if char == curses.KEY_LEFT:
                    menu_table.change_choice_prev()

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
