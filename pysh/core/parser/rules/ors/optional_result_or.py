from dataclasses import dataclass
from typing import MutableSequence, Union
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import (
    no_result_rule,
    optional_result_rule,
    scope,
    single_result_rule,
)
from pysh.core.parser.rules.ors import or_
from pysh.core.parser import states


@dataclass(frozen=True)
class OptionalResultOr(
    optional_result_rule.OptionalResultRule[results.Result],
    or_.Or[
        results.Result,
        Union[
            no_result_rule.NoResultRule[results.Result],
            single_result_rule.SingleResultRule[results.Result],
            optional_result_rule.OptionalResultRule[results.Result],
        ],
    ],
):
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndOptionalResult[results.Result]:
        child_errors: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state, scope).optional()
            except errors.Error as error:
                child_errors.append(error)
        raise parse_error.ParseError(rule=self, state=state, _children=child_errors)
