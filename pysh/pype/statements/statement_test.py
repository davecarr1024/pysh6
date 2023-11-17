from unittest import TestCase

from pysh.pype.statements import statement
from pysh.pype.vals.builtins import int_


class StatementTest(TestCase):
    def test_is_return(self):
        for result, expected in list[tuple[statement.Statement.Result, bool]](
            [
                (
                    statement.Statement.Result(),
                    False,
                ),
                (
                    statement.Statement.Result.for_return(),
                    True,
                ),
                (
                    statement.Statement.Result.for_return(int_.Int.create(1)),
                    True,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(result.is_return(), expected)
