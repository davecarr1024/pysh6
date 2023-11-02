from dataclasses import dataclass
from typing import Generic
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import named_result_rule, scope
from pysh.core.parser.rules.converters import type_converter


@dataclass(frozen=True)
class NamedResultTypeConverter(
    Generic[results.Result, results.ConverterResult],
    type_converter.TypeConverter[
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
            return self.child(state, self.scope).convert_type(self.func)
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])
