from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import nary_regex, state, state_and_result, result


@dataclass(frozen=True)
class And(nary_regex.NaryRegex):
    def __str__(self) -> str:
        return f"({''.join([str(child) for child in self])})"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        result_ = result.Result()
        for child in self:
            try:
                child_state_and_result = child(state)
                state = child_state_and_result.state
                result_ += child_state_and_result.result
            except errors.Error as error:
                raise self._error(state=state, children=[error])
        return state_and_result.StateAndResult(state, result_)
