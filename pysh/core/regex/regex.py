from abc import ABC, abstractmethod
from .. import chars
from . import state_and_result


class Regex(ABC):
    @abstractmethod
    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        ...
