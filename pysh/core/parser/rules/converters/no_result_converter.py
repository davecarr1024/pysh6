from dataclasses import dataclass
from pysh.core.parser import results, states
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
        return self.child(state, self._scope(scope)).convert(self.func)
