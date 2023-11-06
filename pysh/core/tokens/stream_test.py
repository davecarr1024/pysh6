from unittest import TestCase
from pysh.core import errors
from pysh.core.tokens import stream


class StreamTest(TestCase):
    def test_head_error(self):
        with self.assertRaises(errors.Error):
            stream.Stream().head()

    def test_tail_error(self):
        with self.assertRaises(errors.Error):
            stream.Stream().tail()
