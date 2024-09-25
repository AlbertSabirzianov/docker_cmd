"""
This module provides an abstract base class for viewer management
"""
import curses
from abc import ABC, abstractmethod

from app.utils.constants import END_OF_LINE
from app.utils.enams import Colors


class ABSViewer(ABC):
    """
    Abstract Base Class for viewers.

    This class defines an interface for viewer implementations.
    Any subclass must implement the `run` method.
    """

    @abstractmethod
    def run(self):
        """
        Execute the viewer's main functionality.

        This method must be implemented by any subclass of ABSViewer.
        It defines the behavior of the viewer when it is run.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()


class ABSNodeViewer(ABSViewer, ABC):

    @abstractmethod
    def get_tables(self) -> list[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_index(self) -> int:
        raise NotImplementedError()

    def put_tables(self, stdscr: curses.window):
        tables: list[str] = self.get_tables()
        cursor_index: int = self.get_index()

        height, width = stdscr.getmaxyx()

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
                stdscr.addstr(table[:width - 8], curses.color_pair(Colors.WHITE_ON_YELLOW))
            else:
                stdscr.addstr(table[:width - 8])
            stdscr.addstr(END_OF_LINE)

