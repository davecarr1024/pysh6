from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import unary_regex, state_and_result, nary_error


@dataclass(frozen=True)
class OneOrMore(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"{self.child}+"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        try:
            state, result = self.child(state)
        except errors.Error as error_:
            raise nary_error.NaryError(regex=self, state=state, _children=[error_])
        while True:
            try:
                state, child_result = self.child(state)
                result += child_result
            except errors.Error:
                return state, result
