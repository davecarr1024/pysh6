from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import regex, state, state_and_result, result


@dataclass(frozen=True)
class Literal(regex.Regex):
    value: str

    def __post_init__(self):
        if len(self.value) != 1:
            raise self._error(msg="invalid literal")

    def __str__(self) -> str:
        return self.value

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        head = self._try(state.head)
        if head.value != self.value:
            raise self._error(
                state=state,
                msg=f"expected literal {self.value} got {head}",
            )
        return self._try(state.tail).and_result(result.Result([head]))
