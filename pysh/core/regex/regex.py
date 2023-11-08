from abc import ABC, abstractmethod
from pysh.core.regex import and_, state, state_and_result


class Regex(ABC):
    @abstractmethod
    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        ...

    @staticmethod
    def literal(value: str) -> "Regex":
        from pysh.core.regex import and_, literal

        literals = [literal.Literal(c) for c in value]
        if len(literals) == 1:
            return literals[0]
        return and_.And(literals)

    @staticmethod
    def load(value: str) -> "Regex":
        if len(value) > 1:
            return and_.And([Regex.literal(c) for c in value])
        else:
            return Regex.literal(value)
