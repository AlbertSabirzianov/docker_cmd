import logging
import subprocess

from .commands import *


class DockerCommunicator:

    @staticmethod
    def __get_output(command: str) -> str:
        return subprocess.check_output(
            command,
            shell=True,
            text=True
        )

    def check_version(self) -> str:
        return self.__get_output(
            DOCKER_VERSION
        )

    def images(self) -> str:
        return self.__get_output(
            DOCKER_ALL_IMAGES
        )

    def containers(self) -> str:
        logging.warning(self.__get_output(
            DOCKER_ALL_CONTAINERS
        ))
        return self.__get_output(
            DOCKER_ALL_CONTAINERS
        )


docker_communicator = DockerCommunicator()

