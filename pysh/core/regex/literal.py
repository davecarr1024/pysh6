from dataclasses import dataclass
from .. import chars, errors
from . import regex, state_and_result, result, error


@dataclass(frozen=True)
class Literal(regex.Regex):
    value: str

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f"invalid literal {self}")

    def __str__(self) -> str:
        return self.value

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        if state.head().value != self.value:
            raise error.Error(
                regex=self,
                state=state,
                msg=f"expected literal {self.value} got {state.head()}",
            )
        return state.tail(), result.Result([state.head()])
