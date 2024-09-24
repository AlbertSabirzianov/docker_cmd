"""
This module provides an abstract base class and a concrete implementation for communicating with the Docker API.

It includes:
- ABCDockerApi: An abstract base class defining the interface for Docker API communication.
- DockerApiCommunicator: A concrete implementation of the ABCDockerApi that handles HTTP requests to the Docker API.
"""
import functools
import http
import json
import urllib.request
from abc import ABC, abstractmethod
from typing import Union

from ..exeptions.exeptions import DockerApiError
from ..utils.enams import QueryParams, DockerApiEndpoints
from ..utils.hints import ImageResponse, TagResponse


class ABCDockerApi(ABC):
    """Abstract base class for Docker API communication."""

    @abstractmethod
    def get_repositories(self, text: str, page: int = 0) -> ImageResponse:
        """
        Fetches a list of repositories based on the search text and page number.

        Args:
            text (str): The search query for repositories.
            page (int): The page number for pagination (default is 0).

        Returns:
            ImageResponse: A structured response containing image data.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_tags(self, name: str) -> TagResponse:
        """
        Fetches tags for a specified repository.

        Args:
            name (str): The name of the repository in the format 'username/repository'.

        Returns:
            TagResponse: A structured response containing tag data.
        """
        raise NotImplementedError()


class DockerApiCommunicator(ABCDockerApi):
    """Concrete implementation of the ABCDockerApi for communicating with the Docker API."""

    @staticmethod
    @functools.lru_cache
    def __get_http_response(url: str) -> bytes:
        """
        Sends an HTTP GET request to the specified URL and returns the response data.

        Args:
            url (str): The URL to send the request to.

        Returns:
            bytes: The response data in bytes.

        Raises:
            DockerApiError: If the HTTP response status is not OK (200).
        """
        response = urllib.request.urlopen(url)
        if response.getcode() == http.HTTPStatus.OK:
            return response.read()
        raise DockerApiError()

    @staticmethod
    def __add_query_to_url(url: str, query_params: dict[QueryParams, Union[str, int]]) -> str:
        """
        Adds query parameters to the given URL.

        Args:
            url (str): The base URL to which query parameters will be added.
            query_params (dict): A dictionary of query parameters.

        Returns:
            str: The URL with the added query parameters.
        """
        query: str = "&".join([f"{key}={value}" for key, value in query_params.items()])
        return url + "?" + query

    def get_repositories(self, text: str, page: int = 1) -> ImageResponse:
        """
        Fetches repositories from the Docker API based on the search text and page number.

        Args:
            text (str): The search query for repositories.
            page (int): The page number for pagination (default is 1).

        Returns:
            ImageResponse: A structured response containing image data.
        """
        url = self.__add_query_to_url(
            url=DockerApiEndpoints.DOCKER_REPOSITORIES_ENDPOINT,
            query_params={
                QueryParams.QUERY.value: text,
                QueryParams.PAGE.value: page
            }
        )
        data: bytes = self.__get_http_response(url=url)
        return json.loads(data)

    def get_tags(self, name: str, page: int = 1) -> TagResponse:
        """
        Fetches tags for a specified repository from the Docker API.

        Args:
            name (str): The name of the repository in the format 'username/repository'.
            page (int): The page number
        Returns:
            TagResponse: A structured response containing tag data.
        """
        endpoint = DockerApiEndpoints.DOCKER_TAGS_ENDPOINT.replace(
            "{username}/{repository}",
            name
        )
        url = self.__add_query_to_url(
            url=endpoint,
            query_params={
                QueryParams.PAGE.value: page
            }
        )
        data: bytes = self.__get_http_response(url)
        return json.loads(data)

