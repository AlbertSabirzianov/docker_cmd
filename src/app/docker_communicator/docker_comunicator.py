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

    @staticmethod
    def __run_command(command: str) -> None:
        subprocess.run(command, shell=True, check=False, stdout=subprocess.DEVNULL)

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

    def volumes(self) -> str:
        return self.__get_output(
            DOCKER_ALL_VOLUMES
        )

    def delete_volume_by_name(self, name: str):
        self.__run_command(
            DOCKER_VOLUME_REMOVE + name
        )

    def cache_clear(self):
        self.__get_output.cache_clear()

    def delete_containers_by_image_id(self, image_id: str):
        completed_process = subprocess.run(
            DOCKER_PS + " --filter ancestor=" + image_id + " --format '{{.ID}}'",
            shell=True,
            capture_output=True,
            text=True
        )
        container_ids = completed_process.stdout.strip().split('\n')
        for container_id in container_ids:
            container_id = container_id.replace("'", "")
            self.delete_container(container_id)

    def delete_image(self, image_id: str) -> None:
        self.delete_containers_by_image_id(image_id)
        self.__run_command(
            DOCKER_IMAGE_RM + image_id
        )

    def stop_container(self, container_id: str) -> None:
        self.__run_command(
            DOCKER_CONTAINER_STOP + container_id
        )

    def delete_container(self, container_id: str) -> None:
        self.stop_container(container_id)
        self.__run_command(
            DOCKER_CONTAINER_REMOVE + container_id
        )


docker_communicator = DockerCommunicator()

