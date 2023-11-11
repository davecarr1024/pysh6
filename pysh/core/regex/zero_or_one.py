from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import regex, state, state_and_result, result, unary_regex


@dataclass(frozen=True)
class ZeroOrOne(unary_regex.UnaryRegex[regex.Regex]):
    def __str__(self) -> str:
        return f"{self.child}?"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            return self._call_child(state)
        except errors.Error:
            return state.and_result(result.Result())
