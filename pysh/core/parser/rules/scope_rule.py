from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import scope, state_extractor_rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_StateAndResults = TypeVar("_StateAndResults", bound=states.StateAndResults)


@dataclass(frozen=True)
class ScopeRule(
    Generic[_State, _Result, _StateAndResults],
    state_extractor_rule.StateExtractorRule[
        _State,
        _Result,
        _StateAndResults,
        scope.Scope[_State, _Result],
    ],
):
    ...
