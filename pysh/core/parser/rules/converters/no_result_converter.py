from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import no_result_rule, scope

from pysh.core.parser.rules.converters import converter


@dataclass(frozen=True)
class NoResultConverter(
    converter.Converter[results.Result, no_result_rule.NoResultRule[results.Result]]
):
    func: results.NoResultConverterFunc[results.Result]

    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndSingleResult[results.Result]:
        try:
            state_and_result = self.child(state, scope | self.scope)
            return states.StateAndSingleResult[results.Result](
                state_and_result.state,
                results.SingleResult[results.Result](self.func()),
            )
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])
