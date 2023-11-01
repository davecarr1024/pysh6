from dataclasses import dataclass
from typing import Iterable, Iterator, Optional, Sequence, Sized
from unittest import TestCase
from pysh.core import errors

from pysh.core.parser import rules, states


class ParserTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class Expr:
            ...

        @dataclass(frozen=True)
        class Int(Expr):
            value: int

        @dataclass(frozen=True)
        class Str(Expr):
            value: str

        @dataclass(frozen=True)
        class List(Expr, Sized, Iterable):
            _values: Sequence[Expr]

            def __iter__(self) -> Iterator[Expr]:
                return iter(self._values)

            def __len__(self) -> int:
                return len(self._values)

        for state, expected in list[
            tuple[
                states.State | str,
                Optional[states.StateAndSingleResult[Expr]],
            ]
        ]([]):
            parser = rules.Parser[Expr](
                rules.Scope[Expr]({}),
                "expr",
            )
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        parser(state)
                else:
                    self.assertEqual(parser(state), expected)
