from dataclasses import dataclass
from abc import ABC


@dataclass(kw_only=True)
class CommonModel(ABC):

    id: str
