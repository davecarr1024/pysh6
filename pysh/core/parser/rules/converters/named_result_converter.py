from dataclasses import dataclass
from typing import Callable, Generic, Protocol, TypeVar
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import parse_error

from pysh.core.parser.rules import named_result_rule, single_result_rule
from pysh.core.parser.rules.converters import converter_result
from pysh.core.parser.rules.unary_rules import unary_rule

_Result = TypeVar("_Result", contravariant=True)
_ConverterResult = TypeVar("_ConverterResult", covariant=True)


class NamedResultConverterFunc(Protocol, Generic[_Result, _ConverterResult]):
    def __call__(self, **kwargs: _Result) -> _ConverterResult:
        ...


@dataclass(frozen=True)
class NamedResultConverter(
    Generic[results.Result, converter_result.ConverterResult],
    single_result_rule.SingleResultRule[converter_result.ConverterResult],
    unary_rule.UnaryRule[
        converter_result.ConverterResult,
        named_result_rule.NamedResultRule[results.Result],
    ],
):
    func: NamedResultConverterFunc[results.Result, converter_result.ConverterResult]

    def __call__(
        self, state: "states.State[converter_result.ConverterResult]"
    ) -> "states.StateAndSingleResult[converter_result.ConverterResult]":
        child_state = states.State[results.Result](state.tokens)
        try:
            state_and_result = self.child(child_state)
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])
        state = states.State[converter_result.ConverterResult](
            state_and_result.state.tokens
        )
        result = results.SingleResult[converter_result.ConverterResult](
            self.func(**state_and_result.results)
        )
        return states.StateAndSingleResult[converter_result.ConverterResult](
            state, result
        )


from pysh.core.parser import states
