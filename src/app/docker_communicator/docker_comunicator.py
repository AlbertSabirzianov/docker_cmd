import functools
import subprocess

from .commands import *
from ..exeptions.exeptions import DockerNotRunningError


class DockerCommunicator:

    @staticmethod
    @functools.lru_cache
    def __get_output(command: str) -> str:
        try:
            return subprocess.check_output(
                command,
                shell=True,
                text=True
            )
        except subprocess.CalledProcessError:
            raise DockerNotRunningError()

    def check_version(self) -> str:
        return self.__get_output(
            DOCKER_VERSION
        )

    def images(self) -> str:
        return self.__get_output(
            DOCKER_ALL_IMAGES
        )

    def containers(self) -> str:
        return self.__get_output(
            DOCKER_ALL_CONTAINERS
        )

    def cache_clear(self):
        self.__get_output.cache_clear()


docker_communicator = DockerCommunicator()

