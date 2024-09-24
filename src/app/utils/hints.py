"""
This module defines TypedDicts for representing responses from an image repository API.

It includes the following TypedDicts:
- Response: A generic response structure with pagination information.
- Image: Metadata for an image repository.
- Tag: Metadata for a tag associated with an image repository.
- ImageResponse: A response containing a list of images.
- TagResponse: A response containing a list of tags.

These TypedDicts can be used for type hinting and ensuring the structure of data returned from the API.
"""
from typing import TypedDict


class Response(TypedDict):
    """Represents a generic response structure with pagination information."""
    count: int
    next: str
    previous: str


class Image(TypedDict):
    """Represents an image repository with relevant metadata."""
    repo_name: str
    short_description: str
    star_count: int
    pull_count: int
    repo_owner: str
    is_automated: bool
    is_official: bool


class Tag(TypedDict):
    """Represents a tag associated with an image repository."""
    creator: int
    id: int
    images: list
    last_updated: str
    last_updater: int
    last_updater_username: str
    name: str
    repository: int
    full_size: int
    v2: bool
    tag_status: str
    tag_last_pulled: str
    tag_last_pushed: str
    media_type: str
    content_type: str
    digest: str


class ImageResponse(Response):
    """Represents a response containing a list of images."""
    results: list[Image]


class TagResponse(Response):
    """Represents a response containing a list of tags."""
    results: list[Tag]
