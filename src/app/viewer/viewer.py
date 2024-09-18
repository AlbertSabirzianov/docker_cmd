"""
Module: viewer

The viewer module provides a Viewer class for managing and interacting with
Docker images, containers, and volumes. It provides functionality to display
information about Docker entities and manipulate them through the terminal.

The Viewer class uses DockerCommunicator for Docker operations and MenuTable
for terminal-based user interaction. It maintains indexes and lists for tracking
Docker entities and user choices. A variety of dictionaries are used for
mapping user choices to appropriate methods, indexes, and lists.
"""
import curses
import platform
from typing import Callable, Tuple

from .index import ObjIndex
from ..docker_communicator.docker_comunicator import docker_communicator, DockerCommunicator
from ..exeptions.exeptions import DockerNotRunningError
from ..menu_table.menu_table import menu_table, MenuTable
from ..utils.constants import *
from ..utils.enams import Colors, OperatingSystems, MenuChoice, IdIndexes, NameIndexes, Steps, Extensions


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

        self.image_index: ObjIndex = ObjIndex()
        self.container_index: ObjIndex = ObjIndex()
        self.volume_index: ObjIndex = ObjIndex()

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
        self.choice_save_func_dict: dict[MenuChoice, Callable] = {
            MenuChoice.IMAGES: self.docker_communicator.save_image,
            MenuChoice.CONTAINERS: self.docker_communicator.export_container,
            MenuChoice.VOLUMES: self.docker_communicator.tar_volume_by_name
        }
        self.choice_underlines_dict: dict[MenuChoice, list[int]] = {
            MenuChoice.IMAGES: self.underlined_images,
            MenuChoice.CONTAINERS: self.underlined_containers,
            MenuChoice.VOLUMES: self.underlined_volumes
        }
        self.choice_index_dict: dict[MenuChoice, ObjIndex] = {
            MenuChoice.IMAGES: self.image_index,
            MenuChoice.CONTAINERS: self.container_index,
            MenuChoice.VOLUMES: self.volume_index
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
        self.index_number_of_objects_func_list: list[Tuple[ObjIndex, Callable]] = [
            (self.image_index, self.get_number_of_images),
            (self.container_index, self.get_number_of_containers),
            (self.volume_index, self.get_number_of_volumes)
        ]
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
        Checks and adjusts the selected Docker entity indexes to ensure they are within valid ranges.
        """
        for ind, func in self.index_number_of_objects_func_list:
            last_index = func() - 3
            if ind.value > last_index:
                ind.clear()
            if ind.value < 0:
                ind.value = last_index

    def update(self):
        """
        Updates the viewer by clearing the cache,
        resetting the selected Docker entity indexes,
        and clearing the underlined images, containers and volumes.
        """
        self.docker_communicator.cache_clear()
        self.image_index.clear()
        self.container_index.clear()
        self.volume_index.clear()

        self.underlined_images.clear()
        self.underlined_containers.clear()
        self.underlined_volumes.clear()

    def get_tables(self) -> str:
        """
        Gets the tables of the selected Docker entity based on the current choice.

        Returns:
        - A string representation of the Docker images or containers table.
        """
        return self.choice_tables_func_dict[self.menu_table.choice]()

    def change_index(self, char: int) -> None:
        """
        Changes the selected Docker entity index based on the given character input.

        Parameters:
        - char: An integer representing the character input from the user.
        """
        step: int = self.key_steps_dict[char]
        index: ObjIndex = self.choice_index_dict[self.menu_table.choice]
        index.value += step

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

    def get_index(self) -> int:
        """
        Retrieve the index corresponding to the currently selected choice in the menu.

        This method accesses the `choice_index_dict` using the current choice from
        the `menu_table`. It returns the value associated with the selected choice,
        which represents the index of that choice.

        Returns:
            int: The index of the currently selected choice.
        """
        return self.choice_index_dict[self.menu_table.choice].value

    def put_main_table(self):
        """
        Displays the main table of the selected Docker entity based on the current choice in the terminal window.
        """
        tables: list[str] = self.get_tables().split(END_OF_LINE)
        cursor_index: int = self.get_index()
        underline_indexes: list[int] = self.choice_underlines_dict[self.menu_table.choice]

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
        Adds or removes an underline to the currently selected Docker entity based on the current choice.
        """
        index = self.get_index()
        underlined = self.choice_underlines_dict[self.menu_table.choice]

        if index not in underlined:
            underlined.append(index)
        else:
            underlined.remove(index)

    def get_id_by_index(self, index: int):
        """
        Gets the ID of the selected Docker entity based on the current choice at the given index.

        Parameters:
        - index: An integer representing the index of the Docker image or container.

        Returns:
        - The ID of the selected Docker entity based on the current choice at the given index.
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
        Gets the name of the selected Docker entity based on the current choice in the menu at the given index.

        Parameters:
        - index: An integer representing the index of the Docker image or container.

        Returns:
        - The name of the selected Docker entity based on the current choice at the given index.
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
        Deletes the selected Docker entity based on the current choice in the menu.
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

    def save(self):
        """
        Save the selected Docker entity based on the current choice in the menu.

        This method retrieves the indexes associated with the currently selected choice
        from the `choice_underlines_dict`. If no indexes are found, it defaults to using
        the index obtained from the `get_index` method. For each index, it attempts to
        call the corresponding save function from `choice_save_func_dict`, passing the
        entity's ID and name (appended with a TAR archive extension) as arguments.

        If a TypeError occurs during the save operation, it is caught and ignored.

        This method does not return any value.
        """
        indexes = self.choice_underlines_dict[self.menu_table.choice]
        if not indexes:
            indexes = [self.get_index()]
        for index in indexes:
            try:
                self.choice_save_func_dict[self.menu_table.choice](
                    self.get_id_by_index(index),
                    self.get_name_by_index(index) + Extensions.TAR_EXTENSION
                )
            except TypeError:
                continue

    def inspect(self):
        """
        Inspects Docker objects based on user selection from a menu.

        This method retrieves the indexes of the selected choice from the
        `choice_underlines_dict`. If no indexes are found, it defaults to
        getting a single index using `get_index()`. For each index, it
        attempts to call the `inspect` method of the `docker_communicator`
        with the corresponding Docker ID and name, appending a JSON
        extension to the name. If a TypeError occurs during this process,
        it is caught and the loop continues to the next index.
        """
        indexes =self.choice_underlines_dict[self.menu_table.choice]
        if not indexes:
            indexes = [self.get_index()]
        for index in indexes:
            try:
                self.docker_communicator.inspect(
                    self.get_id_by_index(index),
                    self.get_name_by_index(index) + Extensions.JSON_EXTENSION
                )
            except TypeError:
                continue

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
                    self.icon_to_screen()
                    self.delete()
                    self.update()

                if char == KEY_HELP:
                    self.icon_to_screen(help_text=True)
                    self.stdscr.getch()

                if char == KEY_SAVE:
                    self.icon_to_screen()
                    self.save()

                if char == KEY_INSPECT and self.menu_table.choice in (
                    MenuChoice.IMAGES,
                    MenuChoice.CONTAINERS
                ):
                    self.icon_to_screen()
                    self.inspect()

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


