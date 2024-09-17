"""
Module: docker_communicator

This module provides a DockerCommunicator class that facilitates communication with Docker using subprocess.
It also defines a custom exception class called DockerNotRunningError, which is raised when Docker is not running.
"""
import functools
import subprocess

from .commands import *
from ..exeptions.exeptions import DockerNotRunningError


class DockerCommunicator:
    """A class for communicating with Docker using subprocess."""

    @staticmethod
    @functools.lru_cache
    def __get_output(command: str) -> str:
        """
        Execute a command and return the output as a string.

        Args:
            command (str): The command to execute.

        Returns:
            str: The output of the command.

        Raises:
            DockerNotRunningError: If the command execution fails.
        """
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
        """
        Execute a command without capturing the output.

        Args:
            command (str): The command to execute.
        """
        subprocess.run(command, shell=True, check=False, stdout=subprocess.DEVNULL)

    def check_version(self) -> str:
        """
        Check the version of Docker.

        Returns:
            str: The version of Docker.
        """
        return self.__get_output(
            DOCKER_VERSION
        )

    def images(self) -> str:
        """
        Get information about all Docker images.

        Returns:
            str: Information about all Docker images.

        """
        return self.__get_output(
            DOCKER_ALL_IMAGES
        )

    def containers(self) -> str:
        """
        Get information about all Docker containers.

        Returns:
            str: Information about all Docker containers.

        """
        return self.__get_output(
            DOCKER_ALL_CONTAINERS
        )

    def volumes(self) -> str:
        """
        Get information about all Docker volumes.

        Returns:
            str: Information about all Docker volumes.

        """
        return self.__get_output(
            DOCKER_ALL_VOLUMES
        )

    def delete_volume_by_name(self, name: str):
        """
        Delete a Docker volume by name.

        Args:
            name (str): The name of the volume to delete.

        """
        self.__run_command(
            DOCKER_VOLUME_REMOVE + name
        )

    def tar_volume_by_name(self, name: str, filename: str):
        """
        Save a Docker volume to a file.

        Args:
            name (str): The name of the Docker volume to be exported.
            filename (str): The name of the file to save the volume to.
        """
        self.__run_command(
            DOCKER_TAR_VOLUME_BY_NAME.replace(
                "<volume_name>",
                name
            ).replace(
                "<file_name>",
                filename
            )
        )

    def cache_clear(self):
        """Clear the cache used for command output."""
        self.__get_output.cache_clear()

    def delete_containers_by_image_id(self, image_id: str):
        """
        Delete all containers associated with a specific image ID.

        Args:
            image_id (str): The ID of the image.

        """
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
        """
        Delete a Docker image by ID.

        Args:
            image_id (str): The ID of the image to delete.

        """
        self.delete_containers_by_image_id(image_id)
        self.__run_command(
            DOCKER_IMAGE_RM + image_id
        )

    def stop_container(self, container_id: str) -> None:
        """
        Stop a Docker container by ID.

        Args:
            container_id (str): The ID of the container to stop.

        """
        self.__run_command(
            DOCKER_CONTAINER_STOP + container_id
        )

    def delete_container(self, container_id: str) -> None:
        """
        Delete a Docker container by ID.

        Args:
            container_id (str): The ID of the container to delete.

        """
        self.stop_container(container_id)
        self.__run_command(
            DOCKER_CONTAINER_REMOVE + container_id
        )

    def save_image(self, image_id: str, file_name: str) -> None:
        """
        Save a Docker image to a file.

        Args:
            image_id (str): The ID of the Docker image to be saved.
            file_name (str): The name of the file to save the image to.

        """
        self.__run_command(
            DOCKER_SAVE_IMAGE_BY_ID.replace("<file_name>", file_name).replace("<image_id>", image_id)
        )

    def export_container(self, container_id: str, file_name: str) -> None:
        """
        Export a Docker container to a file.

        Args:
            container_id (str): The ID of the Docker container to be exported.
            file_name (str): The name of the file to save the container to.
        """
        self.__run_command(
            DOCKER_EXPORT_CONTAINER.replace("<file_name>", file_name).replace("<container_id>", container_id)
        )


docker_communicator = DockerCommunicator()

