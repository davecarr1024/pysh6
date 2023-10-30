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

    @abstractmethod
    def no(self) -> "no_result_rule.NoResultRule[results.Result]":
        ...

    @abstractmethod
    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        ...


from pysh.core.parser.rules import no_result_rule, single_result_rule
