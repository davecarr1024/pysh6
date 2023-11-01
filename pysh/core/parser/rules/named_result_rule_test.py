from dataclasses import dataclass
from unittest import TestCase
from pysh.core import lexer, tokens

from pysh.core.parser import results, rules, states


class NamedResultRuleTest(TestCase):
    def test_merge(self) -> None:
        lhs: rules.NamedResultRule[str] = rules.literals.TokenValue(
            lexer.Rule.load("l")
        ).named("name")
        rhs: rules.NamedResultRule[int] = rules.literals.SingleResultLiteral[int](
            lexer.Rule.load("r"),
            lambda token: int(token.value),
        ).named("value")
        rule = lhs @ rhs
        state = states.State[int | str](
            tokens.Stream(
                [
                    tokens.Token("l", "a"),
                    tokens.Token("r", "1"),
                ]
            )
        )
        actual = rule(state)
        expected = states.StateAndNamedResult[str | int](
            states.State[int | str](),
            results.NamedResult[str | int](
                {
                    "name": "a",
                    "value": 1,
                }
            ),
        )
        self.assertEqual(actual, expected)

        @dataclass(frozen=True)
        class Decl:
            name: str
            value: int

        self.assertEqual(
            rule.convert(Decl)(states.State[Decl](state.tokens)),
            states.StateAndSingleResult[Decl](
                states.State[Decl](), results.SingleResult[Decl](Decl("a", 1))
            ),
        )
