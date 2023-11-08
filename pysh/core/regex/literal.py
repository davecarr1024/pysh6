from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import regex, state, state_and_result, result


@dataclass(frozen=True)
class Literal(regex.Regex):
    value: str

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f"invalid literal {self}")

    def __str__(self) -> str:
        return self.value

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            head = state.head()
            if head.value != self.value:
                raise self._error(
                    state,
                    msg=f"expected literal {self.value} got {head}",
                )
            return state.tail().and_result(result.Result([head]))
        except chars.Error as error:
            raise self._error(state, children=[error])
