from typing import Optional
from unittest import TestCase
from pysh import core, pysp


class ValTest(TestCase):
    def test_load(self) -> None:
        for state, expected in list[
            tuple[
                pysp.Parser,
                Optional[
                    core.parser.states.StateAndSingleResults[pysp.Parser, pysp.Val]
                ],
            ]
        ](
            [
                (
                    pysp.Parser(),
                    None,
                ),
                (
                    pysp.Parser.load(core.tokens.Token("int", "1")),
                    core.parser.states.StateAndSingleResults[pysp.Parser, pysp.Val](
                        pysp.Parser(),
                        core.parser.results.SingleResults[pysp.Val](pysp.Int(1)),
                    ),
                ),
                (
                    pysp.Parser.load(core.tokens.Token("str", '"a"')),
                    core.parser.states.StateAndSingleResults[pysp.Parser, pysp.Val](
                        pysp.Parser(),
                        core.parser.results.SingleResults[pysp.Val](pysp.Str("a")),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pysp.Val.ref()(state)
                else:
                    self.assertEqual(pysp.Val.ref()(state), expected)
