from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized, Type
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, rules, states


class ParserTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class Expr(ABC):
            @classmethod
            def loader(cls) -> rules.SingleResultRule["Expr"]:
                return Int.reference() | Str.reference()

            @classmethod
            def scope(cls) -> rules.Scope["Expr"]:
                return rules.Scope[Expr](
                    {expr.name(): expr.loader() for expr in cls.types()}
                )

            @classmethod
            def name(cls) -> str:
                return cls.__name__

            @classmethod
            def types(cls) -> Sequence[Type["Expr"]]:
                return [Expr, Int, Str]

            @classmethod
            def parser(cls) -> rules.Parser["Expr"]:
                return rules.Parser[Expr](
                    cls.scope(),
                    cls.name(),
                )

            @classmethod
            def reference(cls) -> rules.Reference["Expr"]:
                return rules.Reference[Expr](cls.name())

        @dataclass(frozen=True)
        class Int(Expr):
            value: int

            @classmethod
            def loader(cls) -> rules.SingleResultRule[Expr]:
                def convert(token: tokens.Token) -> Int:
                    try:
                        return Int(int(token.value))
                    except Exception as error:
                        raise errors.Error(msg=f"failed to load int {token}: {error}")

                return rules.literals.SingleResultLiteral[Expr](
                    lexer.Rule.load("int"),
                    convert,
                )

        @dataclass(frozen=True)
        class Str(Expr):
            value: str

            @classmethod
            def loader(cls) -> rules.SingleResultRule[Expr]:
                return rules.literals.SingleResultLiteral[Expr](
                    lexer.Rule.load("str"),
                    lambda token: Str(token.value),
                )

        for state, expected in list[
            tuple[
                states.State | str,
                Optional[states.StateAndSingleResult[Expr]],
            ]
        ](
            [
                (
                    states.State(),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("int", "1"),
                            ]
                        )
                    ),
                    states.StateAndSingleResult[Expr](
                        states.State(),
                        results.SingleResult[Expr](Int(1)),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("str", "a"),
                            ]
                        )
                    ),
                    states.StateAndSingleResult[Expr](
                        states.State(),
                        results.SingleResult[Expr](Str("a")),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        Expr.parser()(state)
                else:
                    self.assertEqual(Expr.parser()(state), expected)
