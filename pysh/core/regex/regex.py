from abc import ABC, abstractmethod
from .. import chars
from . import state_and_result


class Regex(ABC):
    @abstractmethod
    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        ...

    def apply(self, state: str) -> str:
        _, result = self(chars.Stream.load(state))
        return result.value()

    @staticmethod
    def literal(value: str) -> "Regex":
        from . import and_, literal

        literals = [literal.Literal(c) for c in value]
        if len(literals) == 1:
            return literals[0]
        return and_.And(literals)

    @staticmethod
    def load(value: str) -> "Regex":
        return Regex.literal(value)
