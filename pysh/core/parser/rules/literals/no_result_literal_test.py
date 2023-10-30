import string
from unittest import TestCase

from pysh.core import lexer, regex, tokens
from pysh.core import parser
from pysh.core.parser import states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import no_result_literal

_INT_LEXER_RULE = lexer.Rule.load(
    "int",
    regex.OneOrMore(regex.Or([regex.Regex.load(digit) for digit in string.digits])),
)


class NoResultLiteralTest(TestCase):
    def test_call(self):
        for token in list[tokens.Token](
            [
                tokens.Token("int", "1"),
                tokens.Token("int", "12"),
                tokens.Token("int", "123"),
            ]
        ):
            with self.subTest(token=token):
                no_result_literal.NoResultLiteral[int](_INT_LEXER_RULE)(
                    states.State(tokens.Stream([token])), scope.Scope[int]()
                )

    def test_call_fail(self):
        for token in list[tokens.Token](
            [
                tokens.Token("str", "a"),
            ]
        ):
            with self.subTest(token=token):
                with self.assertRaises(parser.errors.ParseError):
                    no_result_literal.NoResultLiteral[int](_INT_LEXER_RULE)(
                        states.State(tokens.Stream([token])), scope.Scope[int]()
                    )
