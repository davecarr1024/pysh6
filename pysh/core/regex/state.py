from dataclasses import dataclass
from pysh.core import chars as chars_lib
from pysh.core.regex import result, state_and_result


@dataclass(frozen=True)
class State:
    chars: chars_lib.Stream

    def head(self) -> "chars_lib.Char":
        return self.chars.head()

    def tail(self) -> "State":
        return State(self.chars.tail())

    def and_result(self, result: result.Result) -> state_and_result.StateAndResult:
        return state_and_result.StateAndResult(self, result)
