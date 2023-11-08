from dataclasses import dataclass, field
from typing import Iterable, Iterator, MutableSequence, Sequence, Sized
from pysh.core import chars, errors, regex, tokens
from pysh.core.lexer import lex_error, state, state_and_result


@dataclass(frozen=True)
class Lexer(Sized, Iterable["rule.Rule"]):
    _rules: Sequence["rule.Rule"] = field(default_factory=lambda: list[rule.Rule]())

    def __str__(self) -> str:
        return f'Lexer({", ".join(str(rule) for rule in self)})'

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator["rule.Rule"]:
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
        raise lex_error.LexError(lexer_=self, state=state, _children=errors_)

    def __call__(self, state: chars.Stream | str) -> tokens.Stream:
        if isinstance(state, str):
            state = chars.Stream.load(state)
        tokens_: MutableSequence[tokens.Token] = []
        while state:
            state, token = self._apply_any(state)
            if token.value:
                tokens_.append(token)
        return tokens.Stream(tokens_)

    @staticmethod
    def load(**regexes: str | regex.Regex) -> "Lexer":
        return Lexer(
            [rule.Rule.load(rule_name, regex) for rule_name, regex in regexes.items()]
        )

    @staticmethod
    def literal(*values: str) -> "Lexer":
        return Lexer([rule.Rule.load(value) for value in values])


from pysh.core.lexer import rule
