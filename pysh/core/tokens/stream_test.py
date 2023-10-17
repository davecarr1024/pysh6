from unittest import TestCase
from pysh.core.tokens import error, stream


class StreamTest(TestCase):
    def test_head_error(self):
        with self.assertRaises(error.Error):
            stream.Stream().head()

    def test_tail_error(self):
        with self.assertRaises(error.Error):
            stream.Stream().tail()
