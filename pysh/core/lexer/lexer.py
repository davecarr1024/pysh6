from dataclasses import dataclass, field
from typing import Iterable, Iterator, MutableSequence, Optional, Sequence, Sized
from pysh.core import errors, regex, tokens
from pysh.core.lexer import result, rule, state, state_and_result


@dataclass(frozen=True)
class Lexer(
    Sized,
    Iterable[rule.Rule],
    errors.Errorable["Lexer"],
):
    _rules: Sequence[rule.Rule] = field(default_factory=lambda: list[rule.Rule]())

    def __str__(self) -> str:
        return f'Lexer({", ".join(str(rule) for rule in self)})'

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[rule.Rule]:
        return iter(self._rules)

    def __or__(self, rhs: "Lexer") -> "Lexer":
        return Lexer(
            list[rule.Rule](
                (
                    {rule.name: rule for rule in self._rules}
                    | {rule.name: rule for rule in rhs._rules}
                ).values()
            )
        )

    def _apply_any(self, state: state.State) -> state_and_result.StateAndResult:
        errors_: MutableSequence[errors.Error] = []
        for rule in self._rules:
            try:
                return rule(state)
            except errors.Error as error:
                errors_.append(error)
        raise self._error(state=state, children=errors_)

    def __call__(self, state_: str | state.State) -> result.Result:
        if isinstance(state_, str):
            state_ = state.State.load(state_)
        tokens_: MutableSequence[tokens.Token] = []
        while state_.chars:
            state_and_result_ = self._apply_any(state_)
            state_ = state_and_result_.state
            for token in state_and_result_.result.tokens:
                if token.value and not token.rule_name.startswith("~"):
                    tokens_.append(token)
        return result.Result(tokens.Stream(tokens_))

    @staticmethod
    def load(**regexes: str | regex.Regex) -> "Lexer":
        return Lexer(
            [rule.Rule.load(rule_name, regex) for rule_name, regex in regexes.items()]
        )

    @staticmethod
    def literal(*values: str) -> "Lexer":
        return Lexer([rule.Rule.load(value) for value in values])
