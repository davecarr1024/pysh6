from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import unary_regex, state, state_and_result, result


@dataclass(frozen=True)
class ZeroOrMore(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"{self.child}*"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        result_ = result.Result()
        while True:
            try:
                child_state_and_result = super().__call__(state)
                state = child_state_and_result.state
                result_ += child_state_and_result.result
            except errors.Error:
                return state.and_result(result_)
