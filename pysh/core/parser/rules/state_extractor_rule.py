from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_StateValue = TypeVar("_StateValue")


@dataclass(frozen=True)
class StateExtractorRule(
    Generic[_State, _Result, _StateValue],
    states.StateExtractor[_State, _StateValue],
    rule.Rule[_State, _Result],
):
    @abstractmethod
    def _call(
        self, state: _State, state_value: _StateValue
    ) -> states.StateAndResults[_State, _Result]:
        ...

    def __call__(self, state: _State) -> states.StateAndResults[_State, _Result]:
        return self._call(state, self.state_value(state))
