from dataclasses import dataclass, field
from typing import Callable, Optional
from pysh.core import errors, tokens
from pysh.core import parser
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope, optional_result_rule
from pysh.core.parser.rules.literals import literal


@dataclass(frozen=True)
class OptionalResultLiteral(
    literal.Literal[results.Result],
    optional_result_rule.OptionalResultRule[results.Result],
):
    func: Callable[[tokens.Token], Optional[results.Result]] = field(
        compare=False, repr=False
    )

    def __call__(
        self,
        state: states.State,
        scope: scope.Scope[results.Result],
    ) -> states.StateAndOptionalResult[results.Result]:
        try:
            if state.tokens.head().rule_name == self.lexer_rule.name:
                return states.StateAndOptionalResult[results.Result](
                    state.tail(),
                    results.OptionalResult[results.Result](self.func(state.head())),
                )
        except errors.Error as error:
            raise parser.errors.ParseError(rule=self, state=state, _children=[error])
        raise parser.errors.ParseError(rule=self, state=state, msg="unexpected token")
