from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import unary_regex, state_and_result, result


@dataclass(frozen=True)
class ZeroOrMore(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"{self.child}*"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        result_ = result.Result()
        while True:
            try:
                state, child_result = super().__call__(state)
                result_ += child_result
            except errors.Error:
                return state, result_
