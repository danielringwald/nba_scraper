from abc import ABC, abstractmethod
from typing import Any

class CommonDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Any:
        pass
    