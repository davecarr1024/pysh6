from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pysh.core.parser.states import state_extractor


_State = TypeVar("_State", bound="AbstractScopeState")
_Result = TypeVar("_Result")


class AbstractScopeState(
    ABC,
    Generic[_State, _Result],
):
    @classmethod
    @abstractmethod
    def scope_state_extractor(
        cls,
    ) -> state_extractor.StateExtractor[_State, "rules.Scope[_State, _Result]"]:
        ...

    @classmethod
    def ref(cls, name: str) -> "rules.Ref[_State,_Result]":
        return rules.Ref[_State, _Result](cls.scope_state_extractor(), name)


from pysh.core.parser import rules
