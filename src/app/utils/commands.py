"""
This module provides constants for various Docker commands.
"""
DOCKER_VERSION = "docker --version"
DOCKER_PS = "docker ps"
DOCKER_ALL_IMAGES = "docker images -a"
DOCKER_ALL_CONTAINERS = "docker container ls -a"
DOCKER_ALL_VOLUMES = "docker volume ls"
DOCKER_CONTAINER_STOP = "docker stop "
DOCKER_CONTAINER_REMOVE = "docker rm -f "
DOCKER_VOLUME_REMOVE = "docker volume rm -f "
DOCKER_IMAGE_RM = "docker rmi -f "
DOCKER_CONTAINERS_IDS = "docker ps -aq"
DOCKER_VOLUME_IDS = "docker volume ls -aq"
DOCKER_SAVE_IMAGE_BY_ID = "docker save -o <file_name> <image_id>"
DOCKER_EXPORT_CONTAINER = "docker export -o <file_name> <container_id>"
DOCKER_TAR_VOLUME_BY_NAME = """
docker run --rm -v <volume_name>:/volume -v $(pwd):/backup alpine tar cvf /backup/<file_name> -C /volume .
"""
DOCKER_INSPECT_BY_ID = "docker inspect <id>"
DOCKER_CONTAINER_RENAME = "docker rename <old_name> <new_name>"
DOCKER_IMAGE_RENAME = "docker tag <old_name> <new_name>"
DOCKER_VOLUME_CREATE = "docker volume create <new_name>"
DOCKER_VOLUME_COPY = """
docker run --rm -v <old_name>:/from -v <new_name>:/to alpine sh -c "cp -a /from/. /to/"
"""
DOCKER_PULL = "docker pull <name>"