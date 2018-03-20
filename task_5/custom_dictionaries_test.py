from unittest import TestCase
from .custom_dictionaries import ReadOnlyDictionary as RODict


class CustomDictionariesTests(TestCase):
    def setUp(self):
        self.data1 = {'one': 1, 'two': 2}
        self.dict1 = RODict(self.data1)

        self.data2 = {'one': 1, 'two': {'two': 2, 'four': 4}}
        self.dict2_field2 = 'two'
        self.dict2 = RODict(self.data2)

        self.data3 = {'one': 1, 'two': 2}
        self.dict3 = RODict(self.data3)

        self.data4 = {'one': 1, 'two': 2}
        self.dict4 = RODict(self.data3)

        self.data5 = {'one': 1, 'two': {'three': 3, 'four': 4}}

    def test_ro_dict_init(self):
        with self.assertRaises(TypeError):
            RODict(['one', 1, 'two', 2])

        with self.assertRaises(TypeError):
            RODict(['one', 'two', 'three'])

        # check tuple of attribute names
        self.assertEqual(
            self.dict1.dictionary_of_attributes.keys(),
            self.data1.keys()
        )

        # check transformation dict() values into type custom dict
        self.assertEqual(
            type(self.dict2.dictionary_of_attributes[self.dict2_field2]),
            type(self.dict2)
        )

    def test_ro_dict_get_attribute(self):
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

    def test_ro_dict_set_attribute(self):
        with self.assertRaises(AttributeError):
            self.dict3.three = 3
        self.assertEqual(
            self.dict3.dictionary_of_attributes,
            self.data3
        )
        with self.assertRaises(AttributeError):
            self.dict3.one = 12
        # still can add properties, but only
        self.dict3._dictionary_of_attributes.update(one=3)
        # print(self.dict3.one)
        # print(self.dict2)

    def test_ro_dict_len(self):
        self.assertEqual(len(self.data1), len(self.dict1))
        self.assertEqual(len(self.data2), len(self.dict2))

    def test_ro_dict_print(self):
        self.assertEqual(repr(RODict(dict())), '{No attributes}')
        self.assertEqual(
            str(RODict(dict())),
            'Read-Only Dictionary\n{No attributes}\n'
        )
        print(repr(self.dict2))
        self.assertEqual(
            '{\n  |one|: 1,\n  |two|: {\n           |two|: 2,'
            '\n           |four|: 4\n         }\n}',
            repr(self.dict2)
        )

    def test_ro_dict_getitem(self):
        self.assertEqual(self.dict1['two'], self.data1['two'])
        self.assertNotEqual(self.dict2['two'], self.data2['two'])
        self.assertEqual(self.dict2['two'], RODict(self.data2['two']))
        with self.assertRaises(IndexError):
            print(self.dict2['four'])





