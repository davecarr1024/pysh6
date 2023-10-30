from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, single_result_rule, scope, unary_rule


@dataclass(frozen=True)
class UnarySingleResultRule(
    single_result_rule.SingleResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndSingleResult[results.Result]:
        return self.child(state, scope).single()
