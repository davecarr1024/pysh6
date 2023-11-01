from abc import ABC, abstractmethod
from typing import Generic, Optional, overload
from pysh.core import lexer as lexer_lib
from pysh.core.parser import results, states


class Rule(ABC, Generic[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndResult[results.Result]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "multiple_result_rule.MultipleResultRule[results.Result]"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "named_result_rule.NamedResultRule[results.Result]"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(self, rhs: str) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "lexer_lib.Rule"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @abstractmethod
    def __and__(
        self, rhs: "and_args.AndArgs"
    ) -> "and_.And[results.Result, Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __rand__(self, lhs: str) -> "and_.And[results.Result,Rule[results.Result]]":
        ...

    @overload
    @abstractmethod
    def __rand__(
        self, lhs: "lexer_lib.Rule"
    ) -> "and_.And[results.Result,Rule[results.Result]]":
        ...

    @abstractmethod
    def __rand__(
        self, lhs: "rand_args.RandArgs"
    ) -> "and_.And[results.Result,Rule[results.Result]]":
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

    def multiple(self) -> "multiple_result_rule.MultipleResultRule[results.Result]":
        return unary_multiple_result_rule.UnaryMultipleResultRule(self)

    def named(
        self, name: Optional[str] = None
    ) -> "named_result_rule.NamedResultRule[results.Result]":
        return unary_named_result_rule.UnaryNamedResultRule(self, name)

    def zero_or_more(
        self,
    ) -> "zero_or_more.ZeroOrMore[results.Result,Rule[results.Result]]":
        return zero_or_more.ZeroOrMore[results.Result, Rule[results.Result]](self)

    def one_or_more(
        self,
    ) -> "one_or_more.OneOrMore[results.Result,Rule[results.Result]]":
        return one_or_more.OneOrMore[results.Result, Rule[results.Result]](self)

    def zero_or_one(
        self,
    ) -> "zero_or_one.ZeroOrOne[results.Result,Rule[results.Result]]":
        return zero_or_one.ZeroOrOne[results.Result, Rule[results.Result]](self)


from pysh.core.parser.rules import (
    no_result_rule,
    scope,
    single_result_rule,
    optional_result_rule,
    multiple_result_rule,
    named_result_rule,
)
from pysh.core.parser.rules.unary_rules import (
    one_or_more,
    unary_no_result_rule,
    unary_single_result_rule,
    unary_optional_result_rule,
    unary_multiple_result_rule,
    unary_named_result_rule,
    zero_or_more,
    zero_or_one,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
    rand_args,
)
