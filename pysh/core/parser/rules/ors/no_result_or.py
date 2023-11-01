from dataclasses import dataclass
from typing import MutableSequence
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import no_result_rule, scope
from pysh.core.parser.rules.ors import or_
from pysh.core.parser import states


@dataclass(frozen=True)
class NoResultOr(
    no_result_rule.NoResultRule[results.Result],
    or_.Or[results.Result, no_result_rule.NoResultRule[results.Result]],
):
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndNoResult[results.Result]:
        child_errors: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state, scope)
            except errors.Error as error:
                child_errors.append(error)
        raise parse_error.ParseError(rule=self, state=state, _children=child_errors)
