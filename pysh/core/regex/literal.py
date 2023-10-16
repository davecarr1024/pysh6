from dataclasses import dataclass

from .. import chars, errors
from . import regex, state_and_result, result, error, unary_error


@dataclass(frozen=True)
class Literal(regex.Regex):
    value: str

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f"invalid literal {self}")

    def __str__(self) -> str:
        return self.value

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        try:
            head = state.head()
            if head.value != self.value:
                raise error.Error(
                    regex=self,
                    state=state,
                    msg=f"expected literal {self.value} got {head}",
                )
            return state.tail(), result.Result([head])
        except chars.Error as error_:
            raise unary_error.UnaryError(regex=self, state=state, child=error_)
