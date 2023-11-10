from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Self, Sequence, Type, TypeVar
from pysh.core.parser.rules import ref, scope, single_results_rule
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
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def scope(cls) -> scope.Scope[_State, _T]:
        return scope.Scope[_State, _T]({t.name(): t.parser_rule() for t in cls.types()})

    @classmethod
    def ref(
        cls,
    ) -> ref.Ref[_State, _T]:
        return ref.Ref[_State, _T](
            state_value_getter.StateValueGetter[_State, scope.Scope[_State, _T]].load(
                lambda _: cls.scope()
            ),
            cls.name(),
        )
