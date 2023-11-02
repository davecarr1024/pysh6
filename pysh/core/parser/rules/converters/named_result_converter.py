from dataclasses import dataclass
from typing import Generic
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import named_result_rule, scope
from pysh.core.parser.rules.converters import converter


@dataclass(frozen=True)
class NamedResultConverter(
    Generic[results.Result, results.ConverterResult],
    converter.Converter[
        results.Result,
        results.ConverterResult,
        named_result_rule.NamedResultRule[results.Result],
    ],
):
    func: results.NamedResultConverterFunc[results.ConverterResult]

    def __call__(
        self, state: states.State, scope: scope.Scope[results.ConverterResult]
    ) -> states.StateAndSingleResult[results.ConverterResult]:
        try:
            return self.child(state, self._scope()).convert(self.func)
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])