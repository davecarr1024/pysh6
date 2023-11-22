from unittest import TestCase
from pysh import pysh


class ResultTest(TestCase):
    def test_is_return(self) -> None:
        for result, expected in list[
            tuple[
                pysh.statements.Result,
                bool,
            ]
        ](
            [
                (
                    pysh.statements.Result(),
                    False,
                ),
                (
                    pysh.statements.Result.for_return(),
                    True,
                ),
                (
                    pysh.statements.Result.for_return(
                        pysh.vals.int_(1),
                    ),
                    True,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(result.is_return, expected)
