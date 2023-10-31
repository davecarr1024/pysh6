from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import child_rule, multiple_result_rule

from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class OneOrMore(
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
    multiple_result_rule.MultipleResultRule[results.Result],
):
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndMultipleResult[results.Result]":
        try:
            state_and_result = self.child(state)
            state = state_and_result.state
            results_ = state_and_result.results.multiple()
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])
        while True:
            try:
                state_and_result = self.child(state)
                state = state_and_result.state
                results_ |= state_and_result.multiple().results
            except errors.Error:
                return states.StateAndMultipleResult[results.Result](state, results_)


from pysh.core.parser import states
