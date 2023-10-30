from dataclasses import dataclass
from typing import Callable
from pysh.core import errors, tokens
from pysh.core import parser
from pysh.core.parser import results
from pysh.core.parser.rules import scope, single_result_rule

from pysh.core.parser.rules.literals import literal


@dataclass(frozen=True)
class SingleResultLiteral(
    literal.Literal[results.Result], single_result_rule.SingleResultRule[results.Result]
):
    func: Callable[[tokens.Token], results.Result]

    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndSingleResult[results.Result]":
        try:
            if state.tokens.head().rule_name == self.lexer_rule.name:
                return states.StateAndSingleResult[results.Result](
                    state.tail(),
                    results.SingleResult[results.Result](self.func(state.head())),
                )
        except errors.Error as error:
            raise parser.errors.ParseError(rule=self, state=state, _children=[error])
        raise parser.errors.ParseError(rule=self, state=state, msg="unexpected token")


from pysh.core.parser import states
