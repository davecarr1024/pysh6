from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_StateAndResults = TypeVar("_StateAndResults", bound=states.StateAndResults)
_StateValue = TypeVar("_StateValue")


@dataclass(frozen=True)
class StateExtractorRule(
    Generic[_State, _Result, _StateAndResults, _StateValue],
    rule.Rule[_State, _Result],
):
    state_extractor: states.StateExtractor[_State, _StateValue]

    @abstractmethod
    def _call_with_state_value(
        self, state: _State, state_value: _StateValue
    ) -> _StateAndResults:
        ...

    def __call__(self, state: _State) -> _StateAndResults:
        return self._call_with_state_value(state, self.state_extractor(state))

    def _state_with_value(self, state: _State, state_value: _StateValue) -> _State:
        return self.state_extractor.state_with_value(state, state_value)
