from abc import ABC, abstractmethod


class BaseDockerApi(ABC):

    @abstractmethod
    def get_repositories(self, text: str, page: int = 0) -> str:
        raise NotImplementedError()