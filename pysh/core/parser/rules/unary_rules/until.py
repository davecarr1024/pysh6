from dataclasses import dataclass
from typing import Any, TypeVar
from pysh.core import errors, lexer as lexer_lib
from pysh.core.parser import results, states
from pysh.core.parser.rules import multiple_results_rule, rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class Until(
    multiple_results_rule.MultipleResultsRule[_State, _Result],
):
    iter_rule: rule.Rule[_State, _Result]
    term_rule: rule.Rule[_State, Any]

    def __str__(self) -> str:
        return f"{self.iter_rule}.until({self.term_rule})"

    def lexer(self) -> lexer_lib.Lexer:
        return self.iter_rule.lexer() | self.term_rule.lexer()

    def __call__(
        self, state: _State
    ) -> states.StateAndMultipleResults[_State, _Result]:
        results_ = results.MultipleResults[_Result]()
        while True:
            try:
                return states.StateAndMultipleResults[_State, _Result](
                    self.term_rule(state).state, results_
                )
            except errors.Error as error:
                term_error = error
            try:
                child_results_and_state = self.iter_rule(state)
                results_ |= child_results_and_state.results.multiple()
                state = child_results_and_state.state
            except errors.Error as error:
                raise self._parse_error(state, children=[term_error])
