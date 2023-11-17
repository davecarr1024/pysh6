from unittest import TestCase
from pysh import pype


class RootTest(TestCase):
    def test_create(self) -> None:
        for value, expected in list[
            tuple[
                str | pype.vals.Val,
                pype.exprs.refs.roots.Root,
            ]
        ](
            [
                (
                    "a",
                    pype.exprs.refs.roots.Name("a"),
                ),
                (
                    pype.vals.builtins.Int.create(1),
                    pype.exprs.refs.roots.Literal(
                        pype.vals.builtins.Int.create(1),
                    ),
                ),
            ]
        ):
            with self.subTest((value, expected)):
                self.assertEqual(
                    pype.exprs.refs.roots.Root.create(value),
                    expected,
                )
