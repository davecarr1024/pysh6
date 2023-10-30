from abc import ABC, abstractmethod
from typing import Generic, Optional, overload

from pysh.core import lexer as lexer_lib
from pysh.core.parser import results
from pysh.core.parser.rules import scope


class Rule(ABC, Generic[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndResult[results.Result]":
        ...

    # @overload
    # @abstractmethod
    # def __and__(
    #     self, rhs: "no_result_rule.NoResultRule[results.Result]"
    # ) -> "and_.And[results.Result, Rule[results.Result]]":
    #     ...

    # @overload
    # @abstractmethod
    # def __and__(
    #     self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    # ) -> "and_.And[results.Result, Rule[results.Result]]":
    #     ...

    # @overload
    # @abstractmethod
    # def __and__(
    #     self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    # ) -> "and_.And[results.Result, Rule[results.Result]]":
    #     ...

    # @overload
    # @abstractmethod
    # def __and__(
    #     self, rhs: "multiple_result_rule.MultipleResultRule[results.Result]"
    # ) -> "and_.And[results.Result, Rule[results.Result]]":
    #     ...

    # @overload
    # @abstractmethod
    # def __and__(
    #     self, rhs: "named_result_rule.NamedResultRule[results.Result]"
    # ) -> "and_.And[results.Result, Rule[results.Result]]":
    #     ...

    # @abstractmethod
    # def __and__(
    #     self, rhs: "and_args.AndArgs"
    # ) -> "and_.And[results.Result, Rule[results.Result]]":
    #     ...

    @abstractmethod
    def lexer(self) -> lexer_lib.Lexer:
        ...

    def no(self) -> "no_result_rule.NoResultRule[results.Result]":
        return unary_no_result_rule.UnaryNoResultRule(self)

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        return unary_single_result_rule.UnarySingleResultRule(self)

    def optional(self) -> "optional_result_rule.OptionalResultRule[results.Result]":
        return unary_optional_result_rule.UnaryOptionalResultRule(self)

    def multiple(self) -> "multiple_result_rule.MultipleResultRule[results.Result]":
        return unary_multiple_result_rule.UnaryMultipleResultRule(self)

    def named(
        self, name: Optional[str] = None
    ) -> "named_result_rule.NamedResultRule[results.Result]":
        return unary_named_result_rule.UnaryNamedResultRule(self, name)


from pysh.core.parser import states

from pysh.core.parser.rules import (
    no_result_rule,
    single_result_rule,
    optional_result_rule,
    multiple_result_rule,
    named_result_rule,
)
from pysh.core.parser.rules.unary_rules import (
    unary_no_result_rule,
    unary_single_result_rule,
    unary_optional_result_rule,
    unary_multiple_result_rule,
    unary_named_result_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
)
