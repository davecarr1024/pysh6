from dataclasses import dataclass
from pysh.core import errors, chars
from pysh.core.regex import regex, error, state_and_result, result


@dataclass(frozen=True)
class Range(regex.Regex):
    start: str
    end: str

    def __post_init__(self):
        if len(self.start) != 1 or len(self.end) != 1:
            raise errors.Error(msg=f"invalid range {self}")

    def __str__(self):
        return f"[{self.start}-{self.end}]"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        if self.start > state.head().value or self.end < state.head().value:
            raise error.Error(regex=self, state=state)
        return state.tail(), result.Result([state.head()])
