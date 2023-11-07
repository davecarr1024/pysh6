from typing import TypeVar
from pysh.core.parser.states import state_extractor


_State = TypeVar("_State")


class StateSelfExtractor(state_extractor.StateExtractor[_State, _State]):
    def __call__(self, state: _State) -> _State:
        return state
