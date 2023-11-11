from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors
from pysh.core.regex import regex, state, state_and_result


_Child = TypeVar("_Child", bound=regex.Regex)


@dataclass(frozen=True)
class UnaryRegex(Generic[_Child], regex.Regex):
    child: _Child

    def _call_child(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            return self.child(state)
        except errors.Error as error:
            raise self._error(state, children=[error])
