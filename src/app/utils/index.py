"""
This module provides an abstract base class for index management and a concrete implementation.

Classes:
- BaseIndex: An abstract base class that defines the interface for index classes.
- ObjIndex: A concrete implementation of BaseIndex that manages an integer value.

Usage:
- Subclasses of BaseIndex must implement the `clear` method to define how the index is cleared.
- ObjIndex can be used to store an integer value and reset it to zero using the `clear` method.
"""
from abc import ABC, abstractmethod


class BaseIndex(ABC):
    """
    An abstract base class for index management.

    This class defines the interface for index classes, requiring
    the implementation of the `clear` method.
    """

    @abstractmethod
    def clear(self):
        """
        Clear the index.

        This method should be implemented by subclasses to define
        how the index is cleared.
        """
        raise NotImplementedError()


class ObjIndex(BaseIndex):
    """
    A concrete implementation of BaseIndex that manages an integer value.

    This class provides functionality to clear the stored value.
    """

    def __init__(self):
        """
        Initialize the ObjIndex with a default value of 0.
        """
        self.value: int = 0

    def clear(self):
        """
        Clear the stored value by resetting it to 0.
        """
        self.value = 0

