from abc import ABC, abstractmethod
from typing import Generic

from pysh.core import lexer as lexer_lib
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope


class Rule(ABC, Generic[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndResult[results.Result]:
        ...

    @abstractmethod
    def lexer(self) -> lexer_lib.Lexer:
        ...

    def no(self) -> "no_result_rule.NoResultRule[results.Result]":
        return unary_no_result_rule.UnaryNoResultRule(self)

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        return unary_single_result_rule.UnarySingleResultRule(self)

    def optional(self) -> "optional_result_rule.OptionalResultRule[results.Result]":
        return unary_optional_result_rule.UnaryOptionalResultRule(self)

    def multiple(self) -> "multiple_results_rule.MultipleResultsRule[results.Result]":
        return unary_multiple_results_rule.UnaryMultipleResultsRule(self)

    def named(self, name: str) -> "named_results_rule.NamedResultsRule[results.Result]":
        return unary_named_results_rule.UnaryNamedResultsRule(self, name)


from pysh.core.parser.rules import (
    no_result_rule,
    single_result_rule,
    optional_result_rule,
    multiple_results_rule,
    named_results_rule,
    unary_no_result_rule,
    unary_single_result_rule,
    unary_optional_result_rule,
    unary_multiple_results_rule,
    unary_named_results_rule,
)
