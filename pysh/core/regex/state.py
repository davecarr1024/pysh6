from dataclasses import dataclass, field
from typing import Optional
from pysh.core import chars as chars_lib
from pysh.core.regex import result


@dataclass(frozen=True)
class State:
    chars: chars_lib.Stream = field(default_factory=chars_lib.Stream)

    def __str__(self) -> str:
        return str(self.chars)

    def head(self) -> "chars_lib.Char":
        return self.chars.head()

    def tail(self) -> "State":
        return State(self.chars.tail())

    def and_result(
        self, result_: result.Result | str
    ) -> "state_and_result.StateAndResult":
        if isinstance(result_, str):
            result_ = result.Result.load(result_)
        return state_and_result.StateAndResult(self, result_)

    @staticmethod
    def load(value: str, position: Optional[chars_lib.Position] = None) -> "State":
        return State(chars_lib.Stream.load(value, position))


from pysh.core.regex import state_and_result
