from unittest import TestCase
from pysh import core, pype


class LiteralTest(TestCase):
    def test_get(self):
        self.assertEqual(
            pype.exprs.refs.roots.Literal(pype.vals.builtins.Int.create(1)).get(
                pype.vals.Scope()
            ),
            pype.vals.builtins.Int.create(1),
        )

    def test_set(self):
        with self.assertRaises(core.errors.Error):
            pype.exprs.refs.roots.Literal(pype.vals.builtins.Int.create(1)).set(
                pype.vals.Scope(),
                pype.vals.builtins.Int.create(2),
            )
