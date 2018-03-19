from unittest import TestCase
from .myset import MySet
from collections import Iterable


class MySetTests(TestCase):
    def setUp(self):
        self.init_data = [0, 1, 2, 3, 3, 4, 5]
        self.check_data = [0, 1, 2, 3, 4, 5]
        self.gt_data = [0, 1, 2, 3, 4, 5, 6, 7]
        self.or_data = [1, 2, 3, 6, 7]
        self.xor_data = [6, 7]
        self.sub_data = [4, 5, 6, 7]
        self.sub_res = [0, 1, 2, 3]

    def test_init_myset(self):
        m = MySet()
        m1 = MySet(4)
        m2 = MySet([1, 2])
        self.assertTrue(isinstance(m, MySet))
        self.assertTrue(isinstance(m1, MySet))
        self.assertTrue(isinstance(m2, MySet))



    def test_items_property(self):
        m = MySet(self.init_data)
        m2 = MySet()
        self.assertTrue(isinstance(m.items, list))
        self.assertEqual(m2.items, list())

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
            m |= {6, 7, 8}

    def test_xor_operation(self):
        # __xor__
        self.assertEqual(
            MySet(self.init_data) ^ MySet(self.check_data),
            MySet()
        )
        self.assertEqual(
            MySet(self.init_data) ^ MySet(self.gt_data),
            MySet(self.xor_data)
        )
        with self.assertRaises(TypeError):
            MySet(self.init_data) ^ {1, 2, 3, 7, 8}

        # __rxor__
        self.assertEqual(
            MySet(self.init_data) ^ MySet(self.gt_data),
            MySet(self.gt_data) ^ MySet(self.init_data)
        )
        with self.assertRaises(TypeError):
            {1, 2, 3, 7, 8} ^ MySet(self.init_data)

        # __ixor__
        m = MySet(self.init_data)
        m2 = MySet(self.gt_data)
        id_before = id(m)
        m ^= m2
        id_after = id(m)
        self.assertNotEqual(m, m2 ^ m)
        self.assertEqual(id_before, id_after)
        with self.assertRaises(TypeError):
            m ^= {6, 7, 8}

    def test_sub_operations(self):
        # __sub__
        self.assertEqual(
            MySet(self.init_data) - MySet(self.sub_data),
            MySet(self.sub_res)
        )
        self.assertEqual(
            str(MySet(self.init_data) - MySet(self.check_data)),
            'My set()'
        )
        with self.assertRaises(TypeError):
            MySet(self.sub_res) - {56, 3, 2}

        # __rsub__
        self.assertEqual(
            MySet(self.sub_data) - MySet(self.init_data),
            MySet(set(self.sub_data) - set(self.init_data))
        )
        self.assertNotEqual(
            MySet(self.init_data) - MySet(self.sub_data),
            MySet(self.sub_data) - MySet(self.init_data)
        )
        with self.assertRaises(TypeError):
             {56, 3, 2} - MySet(self.sub_res)

        # __isub__
        m = MySet(self.init_data)
        m2 = MySet(self.sub_data)
        id_before = id(m)
        m -= m2
        id_after = id(m)
        self.assertEqual(id_before, id_after)
        with self.assertRaises(TypeError):
            m -= {6, 7, 8}

    def test_add_method(self):
        m = MySet(self.init_data)
        id1 = id(m)
        m.add([1, 2, 3])
        self.assertEqual(m, MySet(self.init_data))
        m.add(self.sub_data)
        self.assertNotEqual(m, MySet(self.init_data))
        self.assertEqual(id(m), id1)
        m.add(76)
        self.assertEqual(id(m), id1)

    def test_clear_method(self):
        m1 = MySet(self.init_data)
        m1.clear()
        m2 = MySet()
        self.assertEqual(m1, m2)

    def test_copy(self):
        m1 = MySet(self.init_data)
        m2 = m1.copy()
        self.assertEqual(m1, m2)
        self.assertNotEqual(id(m1), id(m2))
        self.assertEqual(id(m1.items), id(m2.items))















