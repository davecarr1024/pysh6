from dataclasses import dataclass
from .. import chars, errors
from . import unary_regex, state_and_result, result, unary_error


@dataclass(frozen=True)
class ZeroOrOne(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"{self.child}?"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        try:
            return self.child(state)
        except errors.Error:
            return state, result.Result()
