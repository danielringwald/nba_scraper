from abc import ABC, abstractmethod
from typing import Any


class CommonDAO(ABC):

    @classmethod
    @abstractmethod
    def get_by_id(cls, item_id: str) -> Any:
        raise NotImplementedError
