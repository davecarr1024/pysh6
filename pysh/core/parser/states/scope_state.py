from dataclasses import dataclass, field
from typing import Generic, TypeVar
from pysh.core.parser.states import abstract_scope_state, state_extractor


_State = TypeVar("_State", bound="ScopeState")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class ScopeState(
    Generic[_State, _Result],
    abstract_scope_state.AbstractScopeState[_State, _Result],
):
    scope: "rules.Scope[_State, _Result]" = field(default_factory=lambda: rules.Scope())

    @classmethod
    def scope_state_extractor(
        cls,
    ) -> "state_extractor.StateExtractor[_State,rules.Scope[_State,_Result]]":
        ExtractorState = TypeVar("ExtractorState", bound=ScopeState)
        ExtractorResult = TypeVar("ExtractorResult")

        class Extractor(
            state_extractor.StateExtractor[
                ExtractorState, rules.Scope[ExtractorState, ExtractorResult]
            ]
        ):
            def __call__(
                self, state: ExtractorState
            ) -> rules.Scope[ExtractorState, ExtractorResult]:
                return state.scope

            def state_with_value(
                self,
                state: ExtractorState,
                value: rules.Scope[ExtractorState, ExtractorResult],
            ) -> ExtractorState:
                raise NotImplementedError()

        return Extractor[_State, _Result]()


from pysh.core.parser import rules
