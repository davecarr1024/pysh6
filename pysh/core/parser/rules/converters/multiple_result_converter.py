from dataclasses import dataclass
from typing import Callable, Generic
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import parse_error

from pysh.core.parser.rules import multiple_result_rule, single_result_rule
from pysh.core.parser.rules.converters import converter_result
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class MultipleResultConverter(
    Generic[results.Result, converter_result.ConverterResult],
    single_result_rule.SingleResultRule[converter_result.ConverterResult],
    unary_rule.UnaryRule[
        converter_result.ConverterResult,
        multiple_result_rule.MultipleResultRule[results.Result],
    ],
):
    func: Callable[
        [results.MultipleResult[results.Result]],
        results.SingleResult[converter_result.ConverterResult],
    ]

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
        result = self.func(state_and_result.results)
        return states.StateAndSingleResult[converter_result.ConverterResult](
            state, result
        )


from pysh.core.parser import states
