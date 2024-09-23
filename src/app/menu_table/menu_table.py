"""
This module contains the MenuTable class,
which is used to create a menu table using the curses library in Python.
"""
import curses


from ..utils.enams import MenuChoice, MenuChoiceNames
from ..utils.mixins import MenuMixin


class MenuTable(MenuMixin):
    """A class representing a menu table in a terminal using curses."""

    def __init__(self):
        """Initialize the MenuTable object."""
        self.choice: MenuChoice = MenuChoice.IMAGES

        self.choice_names_dict: dict[MenuChoice, MenuChoiceNames] = {
            MenuChoice.IMAGES: MenuChoiceNames.IMAGES,
            MenuChoice.CONTAINERS: MenuChoiceNames.CONTAINERS,
            MenuChoice.VOLUMES: MenuChoiceNames.VOLUMES
        }

        self.next_choice_dict: dict[MenuChoice, MenuChoice] = {
            MenuChoice.IMAGES: MenuChoice.CONTAINERS,
            MenuChoice.CONTAINERS: MenuChoice.VOLUMES,
            MenuChoice.VOLUMES: MenuChoice.IMAGES
        }

        self.prev_choice_dict: dict[MenuChoice, MenuChoice] = {
            value: key for key, value in self.next_choice_dict.items()
        }

    @property
    def choice_name(self) -> MenuChoiceNames:
        """
        Get the name of the current choice.

        This property retrieves the name associated with the current choice
        from the choice name's dictionary. It provides a way to access the
        human-readable name of the selected menu option.

        Returns:
            MenuChoiceNames: The name of the current choice.
        """
        return self.choice_names_dict[self.choice]

    def is_images(self) -> bool:
        """Check if the current choice is 'Images'."""
        return self.choice == MenuChoice.IMAGES

    def change_choice_next(self):
        """
        Toggle to the next choice in the selection.

        This method updates the current choice to the next one in the
        predefined dictionary of choices. It cycles between 'Images'
        and 'Containers'.
        """
        self.choice = self.next_choice_dict[self.choice]

    def change_choice_prev(self):
        """
        Toggle to the previous choice in the selection.

        This method updates the current choice to the previous one in the
        predefined dictionary of choices. It allows the user to navigate
        back through the available options.
        """
        self.choice = self.prev_choice_dict[self.choice]

    def put_table_on_screen(self, stdscr: curses.window) -> None:
        """
        Display the menu table on the screen.

        Args:
            stdscr (curses.window): The main window object.

        """
        self.put_head_menu(stdscr, self.choice_name)


menu_table = MenuTable()
