from dataclasses import dataclass
from typing import MutableSequence
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import (
    named_result_rule,
    rule,
    scope,
)
from pysh.core.parser.rules.ors import or_
from pysh.core.parser import states


@dataclass(frozen=True)
class NamedResultOr(
    named_result_rule.NamedResultRule[results.Result],
    or_.Or[
        results.Result,
        rule.Rule[results.Result],
    ],
):
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndNamedResult[results.Result]:
        child_errors: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state, scope).named()
            except errors.Error as error:
                child_errors.append(error)
        raise parse_error.ParseError(rule=self, state=state, _children=child_errors)
