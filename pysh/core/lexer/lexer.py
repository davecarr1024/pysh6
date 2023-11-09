from dataclasses import dataclass, field
from typing import Iterable, Iterator, MutableSequence, Optional, Sequence, Sized
from pysh.core import chars, errors, regex, tokens
from pysh.core.lexer import lexer_error, result, rule, state, state_and_result


@dataclass(frozen=True)
class Lexer(Sized, Iterable[rule.Rule]):
    _rules: Sequence[rule.Rule] = field(default_factory=lambda: list[rule.Rule]())

    def __str__(self) -> str:
        return f'Lexer({", ".join(str(rule) for rule in self)})'

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[rule.Rule]:
        return iter(self._rules)

    def __or__(self, rhs: "Lexer") -> "Lexer":
        return Lexer(list(self._rules) + list(rhs._rules))

    def _apply_any(self, state: state.State) -> state_and_result.StateAndResult:
        errors_: MutableSequence[errors.Error] = []
        for rule in self._rules:
            try:
                return rule(state)
            except errors.Error as error:
                errors_.append(error)
        raise self._error(state, children=errors_)

    def __call__(self, state: state.State) -> result.Result:
        tokens_: MutableSequence[tokens.Token] = []
        while state.chars:
            state_and_result_ = self._apply_any(state)
            state = state_and_result_.state
            for token in state_and_result_.result.tokens:
                if token.value:
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

    def _error(
        self,
        state: state.State,
        *,
        msg: Optional[str] = None,
        children: Sequence[errors.Error] = [],
    ) -> lexer_error.LexerError:
        return lexer_error.LexerError(
            lexer=self, state=state, msg=msg, _children=children
        )
