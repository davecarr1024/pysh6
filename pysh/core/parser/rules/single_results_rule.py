from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class SingleResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        ...

    def convert(
        self, func: Callable[[_Result], _ConvertResult]
    ) -> "SingleResultsRule[_State,_ConvertResult]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")
        AdapterChildResult = TypeVar("AdapterChildResult")

        @dataclass(frozen=True)
        class Converter(
            SingleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterChildResult],
        ):
            func: Callable[[AdapterChildResult], AdapterResult]

            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).single().convert(self.func)

        return Converter[_State, _ConvertResult, _Result](self, func)


from pysh.core.parser.rules import unary_rule
