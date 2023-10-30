from dataclasses import dataclass
from pysh.core.parser import results

from pysh.core.parser.rules import child_rule, no_result_rule
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnaryNoResultRule(
    no_result_rule.NoResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndNoResult[results.Result]":
        return self.child(state).no()


from pysh.core.parser import states
