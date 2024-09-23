"""
This module provides an abstract base class for viewer management
"""
from abc import ABC, abstractmethod


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
