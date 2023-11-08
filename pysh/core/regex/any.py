from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import regex, result, state_and_result, unary_error


@dataclass(frozen=True)
class Any(regex.Regex):
    def __str__(self) -> str:
        return "."

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            return state.tail(), result.Result([state.head()])
        except errors.Error as error:
            raise unary_error.UnaryError(regex=self, state=state, child=error)
