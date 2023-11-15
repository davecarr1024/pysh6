from typing import Optional
from unittest import TestCase

from pysh import core, pysp


class RefTest(TestCase):
    def test_eval(self) -> None:
        for ref, scope, expected in list[
            tuple[
                pysp.Ref,
                pysp.Scope,
                Optional[pysp.Val],
            ]
        ](
            [
                (
                    pysp.Ref("a"),
                    pysp.Scope(),
                    None,
                ),
                (
                    pysp.Ref("a"),
                    pysp.Scope({"a": pysp.Int(1)}),
                    pysp.Int(1),
                ),
                (
                    pysp.Ref("a"),
                    pysp.Scope({}, pysp.Scope({"a": pysp.Int(1)})),
                    pysp.Int(1),
                ),
            ]
        ):
            with self.subTest(ref=ref, scope=scope, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        ref.eval(scope)
                else:
                    self.assertEqual(ref.eval(scope), expected)
