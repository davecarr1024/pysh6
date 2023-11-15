from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Self, Sequence, Type, TypeVar
from pysh.core import lexer
from pysh.core.parser import states
from pysh.core.parser.rules import ors, ref, scope as scope_lib, single_results_rule
from pysh.core.parser.states import state_value_getter

_State = TypeVar("_State", bound=states.State)
_T = TypeVar("_T", bound="Parsable")


@dataclass(frozen=True)
class Parsable(ABC, Generic[_State, _T]):
    @classmethod
    @abstractmethod
    def parser_rule(cls) -> single_results_rule.SingleResultsRule[_State, Self]:
        return ors.SingleResultsOr[_State, Self, Self](
            [type.ref() for type in cls.types() if type != cls]
        )

    @classmethod
    @abstractmethod
    def types(cls) -> Sequence[Type[_T]]:
        ...

    @classmethod
    @abstractmethod
    def scope_getter(
        cls,
    ) -> state_value_getter.StateValueGetter[_State, scope_lib.Scope[_State, Self]]:
        ...

    @classmethod
    def type_name(cls) -> str:
        return cls.__name__

    @classmethod
    def scope(cls) -> scope_lib.Scope[_State, _T]:
        return scope_lib.Scope[_State, _T](
            {type.type_name(): type.parser_rule() for type in cls.types()}
        )

    @classmethod
    def ref(
        cls,
    ) -> ref.Ref[_State, Self]:
        return ref.Ref[_State, Self](
            cls.scope_getter(),
            cls.type_name(),
        )

    @classmethod
    def lexer(cls) -> lexer.Lexer:
        lexer_ = lexer.Lexer()
        for type in cls.types():
            lexer_ |= type.parser_rule().lexer()
        return lexer_
