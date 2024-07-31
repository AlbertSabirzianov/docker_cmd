"""
This module defines a custom exception class called DockerNotRunningError.
This class can be used to raise an exception when docker not running on machine.
"""


class DockerNotRunningError(Exception):
    """Custom exception class to indicate that Docker is not running."""
    pass
