from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, optional_result_rule, scope, unary_rule


@dataclass(frozen=True)
class UnaryOptionalResultRule(
    optional_result_rule.OptionalResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndOptionalResult[results.Result]:
        return self.child(state, scope).optional()
