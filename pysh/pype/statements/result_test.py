from unittest import TestCase

from pysh import pype


class ResultTest(TestCase):
    def test_is_return(self) -> None:
        for result, expected in list[tuple[pype.statements.Result, bool]](
            [
                (
                    pype.statements.Result(),
                    False,
                ),
                (
                    pype.statements.Result(pype.vals.builtins.none),
                    True,
                ),
                (
                    pype.statements.Result(pype.vals.builtins.Int.create(1)),
                    True,
                ),
                (
                    pype.statements.Result.for_return(),
                    True,
                ),
                (
                    pype.statements.Result.for_return(pype.vals.builtins.Int.create(1)),
                    True,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(result.is_return(), expected)
