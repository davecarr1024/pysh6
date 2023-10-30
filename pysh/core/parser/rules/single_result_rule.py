from abc import abstractmethod
from dataclasses import dataclass
from pysh.core import lexer
from pysh.core.parser import results, states
from pysh.core.parser.rules import adapter_result, rule, scope, unary_rule


@dataclass(frozen=True)
class SingleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndSingleResult[results.Result]:
        ...

    def no(self) -> "no_result_rule.NoResultRule[results.Result]":
        @dataclass(frozen=True)
        class _Adapter(
            no_result_rule.NoResultRule[adapter_result.AdapterResult],
            unary_rule.UnaryRule[
                adapter_result.AdapterResult,
                SingleResultRule[adapter_result.AdapterResult],
            ],
        ):
            def __call__(
                self,
                state: states.State,
                scope: scope.Scope[adapter_result.AdapterResult],
            ) -> states.StateAndNoResult[adapter_result.AdapterResult]:
                return states.StateAndNoResult(
                    self.child(state, scope).state, results.NoResult()
                )

        return _Adapter[results.Result](self)

    def single(self) -> "SingleResultRule[results.Result]":
        return self


from pysh.core.parser.rules import no_result_rule
