from dataclasses import dataclass
from unittest import TestCase
from pysh.core import lexer, tokens

from pysh.core.parser import results, rules, states
from pysh.core.parser.rules import scope


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
        state = states.State(
            tokens.Stream(
                [
                    tokens.Token("l", "a"),
                    tokens.Token("r", "1"),
                ]
            )
        )
        actual = rule(state, scope.Scope())
        expected = states.StateAndNamedResult[str | int](
            states.State(),
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
            rule.convert(Decl)(state, scope.Scope()),
            states.StateAndSingleResult[Decl](
                states.State(), results.SingleResult[Decl](Decl("a", 1))
            ),
        )
