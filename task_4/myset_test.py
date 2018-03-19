from unittest import TestCase
from .myset import MySet
from collections import Iterable


class MySetTests(TestCase):
    def setUp(self):
        self.init_data = [0, 1, 2, 3, 3, 4, 5]
        self.check_data = [0, 1, 2, 3, 4, 5]
        self.gt_data = [0, 1, 2, 3, 4, 5, 6, 7]
        self.or_data = [1, 2, 3, 6, 7]

    def test_len(self):
        self.assertNotEqual(len(MySet(self.init_data)), len(self.init_data))
        self.assertEqual(len(MySet(self.init_data)), len(self.check_data))

    def test_contains(self):
        self.assertTrue(1 in MySet(self.init_data))
        self.assertTrue([1, 2, 3] in MySet(self.init_data))
        self.assertFalse(7 in MySet(self.init_data))
        self.assertFalse([1, 2, 3, 7] in MySet(self.init_data))

    def test_repr_of_myset(self):
        a = str(set(self.init_data))
        b = str(MySet(self.init_data))
        self.assertEqual(a, b)
        self.assertTrue(str(MySet([])), str('My set()'))

    def test_myset_iterable(self):
        m = MySet(self.init_data)
        self.assertTrue(isinstance(MySet(self.init_data), Iterable))
        for i in m:
            self.assertTrue(i in m)

    def test_equality(self):
        self.assertEqual(MySet(self.init_data), MySet(self.check_data))
        with self.assertRaises(TypeError):
            MySet(self.init_data) == self.init_data

    def test_not_equality(self):
        self.assertFalse(MySet(self.init_data) == MySet(self.gt_data))

    def test_greater_than(self):
        self.assertTrue(MySet(self.gt_data) > MySet(self.init_data))
        self.assertFalse(MySet(self.check_data) > MySet(self.init_data))
        self.assertFalse(MySet(self.init_data) > MySet(self.gt_data))
        with self.assertRaises(TypeError):
            MySet(self.init_data) > set(self.init_data)

    def test_greater_or_equal(self):
        self.assertTrue(MySet(self.gt_data) >= MySet(self.init_data))
        self.assertTrue(MySet(self.check_data) >= MySet(self.init_data))
        self.assertFalse(MySet(self.init_data) >= MySet(self.gt_data))

    def test_less_than(self):
        self.assertTrue(MySet(self.init_data) < MySet(self.gt_data))
        self.assertFalse(MySet(self.init_data) < MySet(self.check_data))
        self.assertFalse(MySet(self.gt_data) < MySet(self.init_data))

    def test_less_or_equal(self):
        self.assertTrue(MySet(self.init_data) <= MySet(self.gt_data))
        self.assertTrue(MySet(self.init_data) <= MySet(self.check_data))
        self.assertFalse(MySet(self.gt_data) <= MySet(self.init_data))

    def test_and_operation(self):
        # __and__ test
        self.assertEqual(
            MySet(self.init_data) & MySet(self.check_data),
            MySet(self.init_data)
        )
        self.assertEqual(
            MySet(self.init_data) & MySet(self.gt_data),
            MySet(self.init_data)
        )
        self.assertNotEqual(
            MySet(self.init_data) & MySet(self.gt_data),
            MySet(self.gt_data)
        )
        with self.assertRaises(TypeError):
            MySet(self.init_data) & {6, 7, 8}

        # __rand__
        self.assertEqual(
            MySet(self.init_data) & MySet(self.check_data),
            MySet(self.check_data) & MySet(self.init_data)
        )
        with self.assertRaises(TypeError):
            {6, 7, 8} & MySet(self.init_data)


        # __iand__
        m = MySet(self.init_data)
        m2 = MySet(self.gt_data)
        id_before = id(m2)
        m2 &= m
        id_after = id(m2)
        self.assertEqual(m, m2)
        self.assertEqual(id_before, id_after)
        with self.assertRaises(TypeError):
            m2 &= {6, 7, 8}


    def test_or_operation(self):
        # __or__
        self.assertEqual(
            MySet(self.init_data) | MySet(self.check_data),
            MySet(self.check_data)
        )
        self.assertEqual(
            MySet(self.init_data) | MySet(self.or_data),
            MySet(self.gt_data)
        )
        self.assertEqual(
            MySet(self.init_data) | MySet(self.gt_data),
            MySet(self.gt_data)
        )
        with self.assertRaises(TypeError):
            MySet(self.init_data) | {6, 7, 8}

        # __ror__
        self.assertEqual(
            MySet(self.init_data) | MySet(self.or_data),
            MySet(self.or_data) | MySet(self.init_data)
        )
        with self.assertRaises(TypeError):
             {6, 7, 8} | MySet(self.init_data)

        # __ior__
        m = MySet(self.init_data)
        m2 = MySet(self.gt_data)
        id_before = id(m)
        m |= m2
        id_after = id(m)
        self.assertEqual(m, m2)
        self.assertEqual(id_before, id_after)
        with self.assertRaises(TypeError):
            m &= {6, 7, 8}












