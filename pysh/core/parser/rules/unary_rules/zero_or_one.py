from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import child_rule, optional_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class ZeroOrOne(
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
    optional_result_rule.OptionalResultRule[results.Result],
):
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndOptionalResult[results.Result]":
        try:
            return self.child(state, scope).optional()
        except errors.Error:
            return states.StateAndOptionalResult[results.Result](
                state, results.OptionalResult[results.Result]()
            )
