from unittest import TestCase
from .myset import MySet


class MySetTests(TestCase):
    def setUp(self):
        self.init_data = [0, 1, 2, 3, 3, 4, 5]
        self.check_data = [0, 1, 2, 3, 4, 5]

    def test_len(self):
        self.assertNotEqual(len(MySet(self.init_data)), len(self.init_data))
        self.assertEqual(len(MySet(self.init_data)), len(self.check_data))
        # self.assertEqual(MySet(self.init_data), self.check_data)
        # self.assertNotEqual(MySet(self.init_data), self.init_data)

    def test_contains(self):
        self.assertTrue(1 in MySet(self.init_data))
        self.assertTrue([1, 2, 3] in MySet(self.init_data))
        self.assertFalse(7 in MySet(self.init_data))
        self.assertFalse([1, 2, 3, 7] in MySet(self.init_data))




