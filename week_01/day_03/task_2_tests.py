from unittest import TestCase
from .task_2 import dict_merger


class DictMergerTest(TestCase):
    """"""
    def setUp(self):
        self.d1 = dict(one=1, two=2)
        self.d2 = dict(four=1, three=3)
        self.d3 = dict(one=1, two=2, three=3, four=1)
        self.d4 = dict(one=5, three=3)
        self.d5 = dict(one=5, two=2, three=3)
        self.d6 = dict(one=1, two=2, three=3)
        self.d7 = dict()

    def test_different_dicts(self):
        self.assertEqual(dict_merger(self.d1, self.d2), self.d3)

    def test_partial_merge(self):
        self.assertEqual(dict_merger(self.d1, self.d4), self.d5)
        self.assertNotEqual(dict_merger(self.d1, self.d4), self.d6)

    def test_merge_with_empty_dict(self):
        self.assertEqual(dict_merger(self.d7, self.d4), self.d4)