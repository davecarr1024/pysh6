from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import single_result_rule, scope

from pysh.core.parser.rules.converters import converter


@dataclass(frozen=True)
class SingleResultConverter(
    converter.Converter[
        results.Result, single_result_rule.SingleResultRule[results.Result]
    ],
):
    func: results.SingleResultConverterFunc[results.Result, results.Result]

    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndSingleResult[results.Result]:
        return self.child(state, self._scope(scope)).convert(self.func)
