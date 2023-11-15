from typing import Optional
from unittest import TestCase

from pysh import core, pysp


class ScopeTest(TestCase):
    def test_get(self):
        for scope, name, expected in list[
            tuple[
                pysp.Scope,
                str,
                Optional[pysp.Val],
            ]
        ](
            [
                (
                    pysp.Scope(),
                    "a",
                    None,
                ),
                (
                    pysp.Scope(
                        {
                            "a": pysp.Int(1),
                        }
                    ),
                    "a",
                    pysp.Int(1),
                ),
                (
                    pysp.Scope(
                        {
                            "a": pysp.Int(1),
                        }
                    ),
                    "b",
                    None,
                ),
                (
                    pysp.Scope(
                        {
                            "a": pysp.Int(1),
                        },
                        pysp.Scope(
                            {
                                "a": pysp.Int(2),
                            }
                        ),
                    ),
                    "a",
                    pysp.Int(1),
                ),
                (
                    pysp.Scope(
                        {
                            "a": pysp.Int(1),
                        },
                        pysp.Scope(
                            {
                                "b": pysp.Int(2),
                            }
                        ),
                    ),
                    "b",
                    pysp.Int(2),
                ),
            ]
        ):
            with self.subTest(scope=scope, name=name, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        scope[name]
                else:
                    self.assertEqual(scope[name], expected)

    def test_set(self):
        for scope, name, val, expected in list[
            tuple[
                pysp.Scope,
                str,
                pysp.Val,
                pysp.Scope,
            ]
        ](
            [
                (
                    pysp.Scope(),
                    "a",
                    pysp.Int(1),
                    pysp.Scope({"a": pysp.Int(1)}),
                ),
                (
                    pysp.Scope({"a": pysp.Int(1)}),
                    "a",
                    pysp.Int(2),
                    pysp.Scope({"a": pysp.Int(2)}),
                ),
                (
                    pysp.Scope({}, pysp.Scope({"a": pysp.Int(1)})),
                    "a",
                    pysp.Int(2),
                    pysp.Scope({"a": pysp.Int(2)}, pysp.Scope({"a": pysp.Int(1)})),
                ),
            ]
        ):
            with self.subTest(scope=scope, name=name, val=val, expected=expected):
                scope[name] = val
                self.assertEqual(scope, expected)
