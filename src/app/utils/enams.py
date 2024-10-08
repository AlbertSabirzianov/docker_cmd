"""
Module: enums

This module defines Enum classes
"""
from enum import Enum


class Colors(int, Enum):
    """An enumeration of color options with corresponding integer values."""
    WHITE_ON_BLUE = 1
    WHITE_ON_BLACK = 2
    WHITE_ON_YELLOW = 3


class MenuChoice(int, Enum):
    """An enumeration of menu choices with corresponding integer values."""
    IMAGES = 1
    CONTAINERS = 0
    VOLUMES = 2


class IdIndexes(int, Enum):
    """An enumeration of ID indexes with corresponding integer values."""
    IMAGE_ID_INDEX = 2
    CONTAINER_ID_INDEX = 0
    VOLUME_ID_INDEX = -1


class NameIndexes(int, Enum):
    """An enumeration of Name indexes with corresponding integer values."""
    IMAGE_NAME_INDEX = 0
    CONTAINER_NAME_INDEX = -1
    VOLUME_NAME_INDEX = -1


class Steps(int, Enum):
    """An enumeration of Steps with corresponding integer values."""
    STEP_UP = -1
    STEP_DOWN = 1


class MenuChoiceNames(str, Enum):
    """An enumeration of menu choices with corresponding string values."""
    IMAGES = "Images"
    CONTAINERS = "Containers"
    VOLUMES = "Volumes"


class OperatingSystems(str, Enum):
    """An enumeration of Operating systems with corresponding string values."""
    WINDOWS = "Windows"
    LINUX = "Linux"
    JAVA = "Java"


class Extensions(str, Enum):
    """
    An enumeration for file extensions.

    This class defines a set of string-based constants representing
    common file extensions used in the application. It inherits from
    both `str` and `Enum`, allowing the members to be used as strings
    while also providing the benefits of enumeration.
    """
    TAR_EXTENSION = ".tar"
    JSON_EXTENSION = ".json"


class DockerApiEndpoints(str, Enum):
    """Enumeration of Docker API endpoints."""
    DOCKER_REPOSITORIES_ENDPOINT = "https://hub.docker.com/v2/search/repositories/"
    DOCKER_TAGS_ENDPOINT = "https://hub.docker.com/v2/repositories/{username}/{repository}/tags/"


class QueryParams(str, Enum):
    """Enumeration of common query parameters for API requests."""
    QUERY = "query"
    PAGE = "page"
    PAGE_SIZE = "page_size"


