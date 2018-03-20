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
            self.dict1.dictionary_of_attributes,
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
            self.dict1.dictionary_of_attributes,
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
            self.dict3.dictionary_of_attributes,
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

    def test_protected_dict(self):
        p = PRADMDict({'one': 1, 'two': 2}, 'one')
        print(p.protected_attributes)
        p2 = PRADMDict({'one': 1, 'two': {'three': 3, 'four': 4}}, 'two.three')
        print(p2.protected_attributes)
        print(p2.two.protected_attributes)
        print(p2.two)


