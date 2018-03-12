from unittest import TestCase
from .task_2 import dict_merger


class DictMergerTest(TestCase):
    """"""
    def test_simple_case(self):
        d1 = dict(one=1, two=2)
        d2 = dict(four=1, three=3)
        d3 = dict(one=1, two=2, three=3, four=1)
        self.assertEqual(dict_merger(d1, d2), d3)

    def test_different_vals(self):
        d1 = dict(one=1, two=2)
        d2 = dict(one=5, three=3)
        d3 = dict(one=5, two=2, three=3)
        d4 = dict(one=1, two=2, three=3)
        self.assertEqual(dict_merger(d1, d2), d3)
        self.assertNotEqual(dict_merger(d1, d2), d4)

    def test_empty_dict(self):
        d1 = dict()
        d2 = dict(one=5, three=3)
        d3 = dict(one=5, three=3)
        self.assertEqual(dict_merger(d1, d2), d3)