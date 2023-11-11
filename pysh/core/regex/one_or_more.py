from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import regex, unary_regex, state, state_and_result


@dataclass(frozen=True)
class OneOrMore(unary_regex.UnaryRegex[regex.Regex]):
    def __str__(self) -> str:
        return f"{self.child}+"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            child_state_and_result = self._call_child(state)
            state = child_state_and_result.state
            result = child_state_and_result.result
        except errors.Error as error:
            raise self._error(state, children=[error])
        while True:
            try:
                child_state_and_result = self._call_child(state)
                state = child_state_and_result.state
                result += child_state_and_result.result
            except errors.Error:
                return state.and_result(result)
