from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Self, Sequence, Type, TypeVar
from pysh.core import lexer
from pysh.core.parser.rules import ref, scope as scope_lib, single_results_rule
from pysh.core.parser.states import state_value_getter

_State = TypeVar("_State")
_T = TypeVar("_T", bound="Parsable")


@dataclass(frozen=True)
class Parsable(ABC, Generic[_State, _T]):
    @classmethod
    @abstractmethod
    def parser_rule(cls) -> single_results_rule.SingleResultsRule[_State, Self]:
        ...

    @classmethod
    @abstractmethod
    def types(cls) -> Sequence[Type[_T]]:
        ...

    @classmethod
    @abstractmethod
    def scope_getter(
        cls,
    ) -> state_value_getter.StateValueGetter[_State, scope_lib.Scope[_State, _T]]:
        ...

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def scope(cls) -> scope_lib.Scope[_State, _T]:
        return scope_lib.Scope[_State, _T](
            {t.name(): t.parser_rule() for t in cls.types()}
        )

    @classmethod
    def ref(
        cls,
    ) -> ref.Ref[_State, _T]:
        return ref.Ref[_State, _T](
            cls.scope_getter(),
            cls.name(),
        )

    @classmethod
    def lexer(cls) -> lexer.Lexer:
        lexer_ = lexer.Lexer()
        for type in cls.types():
            lexer_ |= type.parser_rule().lexer()
        return lexer_
