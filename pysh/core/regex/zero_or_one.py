from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import unary_regex, state_and_result, result, unary_error


@dataclass(frozen=True)
class ZeroOrOne(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"{self.child}?"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        try:
            return super().__call__(state)
        except errors.Error:
            return state, result.Result()
