from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import regex, result, state, state_and_result


@dataclass(frozen=True)
class Any(regex.Regex):
    def __str__(self) -> str:
        return "."

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            return state.tail().and_result(result.Result([state.head()]))
        except errors.Error as error:
            raise self._error(state=state, children=[error])
