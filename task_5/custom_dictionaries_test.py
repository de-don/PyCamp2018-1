from unittest import TestCase
from .custom_dictionaries import ReadOnlyDictionary as RODict
from .custom_dictionaries import ReadModifyDictionary as RMDict


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
        self.dict4 = RMDict(self.data2)

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
            self.dict1.dictionary_of_attributes.keys(),
            self.data1.keys()
        )

        # ############################################
        # ReadModifyDictionary
        # ############################################
        # check transformation dict() values into type custom dict
        self.assertEqual(type(self.dict4.two), type(self.dict4))

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
            self.data1
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
            self.data3
        )
        self.dict3.one = 12
        self.assertEqual(self.dict3.one, 12)
        self.dict4.two.two = 12
        self.assertEqual(self.dict4.two.two, 12)

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





