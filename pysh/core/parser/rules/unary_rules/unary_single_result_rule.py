from dataclasses import dataclass
from pysh.core.parser import results

from pysh.core.parser.rules import child_rule, single_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnarySingleResultRule(
    single_result_rule.SingleResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: "states.State"
    ) -> "states.StateAndSingleResult[results.Result]":
        return self.child(state).single()


from pysh.core.parser import states
