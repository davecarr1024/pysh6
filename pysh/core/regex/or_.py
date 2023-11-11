from dataclasses import dataclass
from typing import MutableSequence, TypeVar
from pysh.core import errors
from pysh.core.regex import nary_regex, regex, state, state_and_result

_Child = TypeVar("_Child", bound=regex.Regex)


@dataclass(frozen=True)
class Or(nary_regex.NaryRegex[_Child]):
    def __str__(self) -> str:
        return f"({'|'.join([str(child) for child in self])})"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        child_errors: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state)
            except errors.Error as error_:
                child_errors.append(error_)
        raise self._error(state, children=child_errors)
