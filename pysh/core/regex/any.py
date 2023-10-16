from dataclasses import dataclass
from .. import chars
from . import regex, result, state_and_result


@dataclass(frozen=True)
class Any(regex.Regex):
    def __str__(self) -> str:
        return "."

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        return state.tail(), result.Result([state.head()])
