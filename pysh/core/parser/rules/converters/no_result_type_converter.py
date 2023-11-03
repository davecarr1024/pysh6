from dataclasses import dataclass
from typing import Generic
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import no_result_rule, scope
from pysh.core.parser.rules.converters import type_converter


@dataclass(frozen=True)
class NoResultTypeConverter(
    Generic[results.Result, results.ConverterResult],
    type_converter.TypeConverter[
        results.ConverterResult,
        no_result_rule.NoResultRule[results.Result],
    ],
):
    func: results.NoResultConverterFunc[results.ConverterResult]

    def __call__(
        self, state: states.State, scope: scope.Scope[results.ConverterResult]
    ) -> states.StateAndSingleResult[results.ConverterResult]:
        try:
            return self._call(state, scope.Scope[results.Result]()).convert_type(
                self.func
            )
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])
