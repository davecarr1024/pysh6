from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import child_rule, multiple_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class ZeroOrMore(
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
    multiple_result_rule.MultipleResultRule[results.Result],
):
    def __str__(self) -> str:
        return f"{self.child}*"

    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndMultipleResult[results.Result]":
        results_ = results.MultipleResult[results.Result]()
        while True:
            try:
                state_and_result = super().__call__(state, scope)
                state = state_and_result.state
                results_ |= state_and_result.multiple().results
            except errors.Error:
                return states.StateAndMultipleResult[results.Result](state, results_)
