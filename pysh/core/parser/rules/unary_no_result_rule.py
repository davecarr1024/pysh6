from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, no_result_rule, scope, unary_rule


@dataclass(frozen=True)
class UnaryNoResultRule(
    no_result_rule.NoResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndNoResult[results.Result]:
        return self.child(state, scope).no()
