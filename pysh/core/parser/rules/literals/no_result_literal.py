from dataclasses import dataclass
from pysh.core import tokens
from pysh.core.parser import errors, results, states
from pysh.core.parser.rules import no_result_rule, scope

from pysh.core.parser.rules.literals import literal


@dataclass(frozen=True)
class NoResultLiteral(
    literal.Literal[results.Result], no_result_rule.NoResultRule[results.Result]
):
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndNoResult[results.Result]":
        try:
            if state.tokens.head().rule_name != self.lexer_rule.name:
                raise errors.ParseError(
                    rule=self,
                    state=state,
                    msg=f"expected lexer_rule {self.lexer_rule} but got {state.tokens.head()}",
                )
            print("test")
            return states.StateAndNoResult[results.Result](
                states.State(state.tokens.tail()),
                results.NoResult[results.Result](),
            )
        except tokens.Error as error:
            raise errors.ParseError(
                rule=self, state=state, msg=f"failed to get token: {error}"
            )


from pysh.core.parser import states