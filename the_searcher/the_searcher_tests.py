from unittest import TestCase
from click.testing import CliRunner

from .the_searcher import searcher


# global runner
runner = CliRunner()


class TheSearcherTests(TestCase):
    """"""
    def setUp(self):
        self.pattern1 = "\w+@[\w.-_]+"
        self.file = "the_searcher/emails.txt"

    def test_zero_exit_code(self):
        result1 = runner.invoke(
            searcher,
            ['-u', self.pattern1],
            input="cgarcia@outlook.com\nblahblahblah\tjrif.kin@icloud.com",
        )
        result2 = runner.invoke(
            searcher,
            ['-u', self.pattern1, self.file],
        )
        self.assertEqual(result1.exit_code, 0)
        self.assertEqual(result2.exit_code, 0)
