from unittest import TestCase
from .custom_dictionaries import ProtectedError
from .custom_dictionaries import ReadOnly as RODict
from .custom_dictionaries import ReadModify as RMDict
from .custom_dictionaries import ReadAddModify as RAMDict
from .custom_dictionaries import ReadAddModifyDelete as RADMDict
from .custom_dictionaries import Protected as PRADMDict


class CustomDictionariesTests(TestCase):
    def setUp(self):
        self.data1 = {'one': 1, 'two': 2}
        self.dict1 = RODict(self.data1)

        self.data2 = {'one': 1, 'two': {'two': 2, 'four': 4}}
        self.dict2_field2 = 'two'
        self.dict2 = RODict(self.data2)

        self.data3 = {'one': 1, 'two': 2}
        self.dict3 = RMDict(self.data3)

        self.data4 = {'one': 1, 'two': {'two': 2, 'four': 4}}
        self.dict4 = RMDict(self.data4)

        self.data5 = {'one': 1, 'two': 2}
        self.dict5 = RAMDict(self.data5)

        self.data6 = {'one': 1, 'two': {'two': 2, 'four': 4}}
        self.dict6 = RAMDict(self.data6)

        self.data7 = {'one': 1, 'two': 2, 'three': 3}
        self.dict7 = RADMDict(self.data7)

        self.data8 = {'one': 1, 'two': {'two': 2, 'four': 4, 'five': 5}}
        self.dict8 = RADMDict(self.data8)

    def test_custom_dicts_init(self):
        # ############################################
        # ReadOnlyDictionary
        # ############################################
        with self.assertRaises(TypeError):
            RODict(['one', 1, 'two', 2])

        with self.assertRaises(TypeError):
            RODict(['one', 'two', 'three'])

        # check tuple of attribute names
        self.assertEqual(
            self.dict1._dictionary_of_attributes.keys(),
            self.data1.keys()
        )

        # ############################################
        # ReadModifyDictionary
        # ############################################
        # check transformation dict() values into type custom dict
        self.assertEqual(type(self.dict4.two), type(self.dict4))

        # ############################################
        # ReadAddModifyDictionary
        # ############################################
        # check transformation dict() values into type custom dict
        self.assertEqual(type(self.dict6.two), type(self.dict6))

    def test_custom_dicts_get_attribute(self):
        # ############################################
        # ReadOnlyDictionary
        # ############################################
        self.assertEqual(
            self.dict1.one,
            self.data1['one']
        )
        self.assertEqual(
            self.dict1.two,
            self.data1['two']
        )
        with self.assertRaises(AttributeError):
            a = self.dict1.three
        self.assertEqual(
            self.dict2.two,
            RODict(self.data2['two'])
        )
        self.assertEqual(
            self.dict2.two.two,
            self.data2['two']['two']
        )

    def test_custom_dicts_set_attribute(self):
        # ############################################
        # ReadOnlyDictionary
        # ############################################
        with self.assertRaises(AttributeError):
            self.dict1.three = 3
        self.assertEqual(
            self.dict1._dictionary_of_attributes.keys(),
            self.data1.keys()
        )
        with self.assertRaises(AttributeError):
            self.dict1.one = 12
        # WARNING!!! Still can add properties, but only through private member
        self.dict1._dictionary_of_attributes.update(one=3)
        self.assertEqual(self.dict1.one, 3)

        # ############################################
        # ReadModifyDictionary
        # ############################################
        with self.assertRaises(AttributeError):
            self.dict3.three = 3
        self.assertEqual(
            self.dict3._dictionary_of_attributes.keys(),
            self.data3.keys()
        )
        self.dict3.one = 12
        self.assertEqual(self.dict3.one, 12)
        self.dict4.two.two = 12
        self.assertEqual(self.dict4.two.two, 12)

        # ############################################
        # ReadAddModifyDictionary
        # ############################################
        self.dict5.three = 3
        self.assertEqual(self.dict5.three, 3)
        self.dict5.one = 12
        self.assertEqual(self.dict3.one, 12)
        self.dict6.two.two = 12
        self.assertEqual(self.dict6.two.two, 12)
        self.dict6.two.death = 'death'
        self.assertEqual(self.dict6.two.death, 'death')

    def test_custom_dicts_len(self):
        # ############################################
        # ReadOnlyDictionary
        # ############################################
        self.assertEqual(len(self.data1), len(self.dict1))
        self.assertEqual(len(self.data2), len(self.dict2))

    def test_custom_dicts_print(self):
        # ############################################
        # ReadOnlyDictionary
        # ############################################
        self.assertEqual(repr(RODict(dict())), '{No attributes}')
        self.assertEqual(
            str(RODict(dict())),
            'Read-Only Dictionary\n{No attributes}\n'
        )
        self.assertEqual(
            '{\n  |one|: 1,\n  |two|: {\n           |two|: 2,'
            '\n           |four|: 4\n         }\n}',
            repr(self.dict2)
        )

        # ############################################
        # ReadModifyDictionary
        # ############################################
        self.assertEqual(repr(RMDict(dict())), '{No attributes}')
        self.assertEqual(
            str(RMDict(dict())),
            'Read-and-Modify Dictionary\n{No attributes}\n'
        )

        # ############################################
        # ReadAddModifyDictionary
        # ############################################
        self.assertEqual(repr(RAMDict(dict())), '{No attributes}')
        self.assertEqual(
            str(RAMDict(dict())),
            'Read-Add-Modify Dictionary\n{No attributes}\n'
        )

        # ############################################
        # ReadAddModifyDeleteDictionary
        # ############################################
        self.assertEqual(repr(RADMDict(dict())), '{No attributes}')
        self.assertEqual(
            str(RADMDict(dict())),
            'Read-Add-Modify-Delete Dictionary\n{No attributes}\n'
        )

        # ############################################
        # Protected
        # ############################################
        self.assertEqual(repr(PRADMDict(dict())), '{No attributes}')
        self.assertEqual(
            str(PRADMDict(dict())),
            'Protected Read-Add-Modify-Delete Dictionary\n{No attributes}\n'
        )

    def test_custom_dicts_getitem(self):
        # ############################################
        # ReadOnlyDictionary
        # ############################################
        self.assertEqual(self.dict1['two'], self.data1['two'])
        self.assertNotEqual(self.dict2['two'], self.data2['two'])
        self.assertNotEqual(self.dict2['two'], self.data2['two'])
        self.assertEqual(self.dict2['two'], RODict(self.data2['two']))
        with self.assertRaises(IndexError):
            print(self.dict2['four'])

    def test_radmd_dict_delitem(self):
        with self.assertRaises(AttributeError):
            del self.dict7.error
        with self.assertRaises(AttributeError):
            del self.dict8.two.error
        del self.dict7.three
        self.assertEqual(self.dict5, self.dict7)
        del self.dict8.two.five
        self.assertEqual(self.dict6, self.dict8)

    def test_protected_dict_has_protected_attribute(self):
        p = PRADMDict({'one': 1, 'two': 2}, 'one')
        self.assertTrue('one' in p._protected_attributes)

    def test_protected_dict_has_protected_attribute_case_dot(self):
        p = PRADMDict({'one': 1, 'two': 2}, 'one.')
        self.assertTrue('one' in p._protected_attributes)

    def test_protected_dict_raises_protected_error(self):
        p = PRADMDict({'one': 1, 'two': 2}, 'one')
        with self.assertRaises(ProtectedError):
            p.one = 11

    def test_protected_dict_has_nested_protected_attribute(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        self.assertTrue('two' in p._protected_attributes)

    def test_protected_dict_has_nested_protected_attribute_case_dot(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three.')
        self.assertTrue('two' in p._protected_attributes)

    def test_protected_dict_has_nested_with_protected_attribute(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        self.assertTrue('three' in p.two._protected_attributes)
        self.assertFalse('three' in p._protected_attributes)
        self.assertFalse('two' in p.two._protected_attributes)

    def test_protected_dict_with_nested_raises_protected_error_on_top_level(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        with self.assertRaises(ProtectedError):
            p.two = 23

    def test_protected_dict_with_nested_raises_protected_error_on_low_level(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        with self.assertRaises(ProtectedError):
            p.two.three = 23

    def test_protected_dict_with_nested_raises_attribute_error_on_top_level(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        with self.assertRaises(ProtectedError):
            p.two = 23

    def test_protected_dict_with_nested_raises_attribute_error_on_low_level(self):
        with self.assertRaises(AttributeError):
            _ = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}},
                          'shark')

    def test_protected_dict_with_nested_raises_attribute_error_on_nested_level(self):
        with self.assertRaises(AttributeError):
            _ = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}},
                          'two.shark')

    def test_equality_of_protected(self):
        p1 = PRADMDict({'one': 1, 'two': 2}, 'one')
        p2 = PRADMDict({'one': 1, 'two': 2}, 'one')
        self.assertTrue(p1 == p2)
        p3 = PRADMDict({'one': 1, 'two': 2}, 'two')
        self.assertFalse(p1 == p3)

    def test_prtected_dict_delete_top_level(self):
        p1 = PRADMDict({'one': 1, 'two': 2}, 'one')
        del p1.two
        p2 = PRADMDict({'one': 1}, 'one')
        self.assertTrue(p1 == p2)

    def test_prtected_dict_delete_top_level_raises_protected_error(self):
        p1 = PRADMDict({'one': 1, 'two': 2}, 'one')
        with self.assertRaises(ProtectedError):
            del p1.one

    def test_prtected_dict_delete_nested_level(self):
        p1 = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'one')
        del p1.two.three
        p2 = PRADMDict({'one': 1, 'two': {'four': 4}}, 'one')
        self.assertTrue(p1 == p2)

    def test_prtected_dict_delete_nested_level_raises_protected_error(self):
        p = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        with self.assertRaises(ProtectedError):
            del p.two.three
        with self.assertRaises(ProtectedError):
            del p.two





