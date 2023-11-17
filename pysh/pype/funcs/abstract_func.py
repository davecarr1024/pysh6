from abc import abstractmethod
from dataclasses import dataclass
from pysh.pype.vals import val


@dataclass(frozen=True)
class AbstractFunc(val.Val):
    @abstractmethod
    def name(self) -> str:
        ...
