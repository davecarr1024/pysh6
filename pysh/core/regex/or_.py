from dataclasses import dataclass
from typing import MutableSequence
from pysh.core import chars, errors
from pysh.core.regex import nary_regex, state_and_result, nary_error


@dataclass(frozen=True)
class Or(nary_regex.NaryRegex):
    def __str__(self) -> str:
        return f"({'|'.join([str(child) for child in self])})"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        child_errors: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state)
            except errors.Error as error_:
                child_errors.append(error_)
        raise nary_error.NaryError(regex=self, state=state, children=child_errors)
