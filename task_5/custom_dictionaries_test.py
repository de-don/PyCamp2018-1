from unittest import TestCase
from .custom_dictionaries import ReadOnlyDictionary as RODict


class CustomDictionariesTests(TestCase):
    def setUp(self):
        self.data1 = {'one': 1, 'two': 2}
        self.dict1 = RODict(self.data1)

        self.data2 = {'one': 1, 'two': {'three': 3, 'four': 4}}
        self.dict2_field2 = 'two'
        self.dict2 = RODict(self.data2)

        self.data3 = {'one': 1, 'two': 2}
        self.dict3 = RODict(self.data1)

    def test_mydict_init(self):
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

    def test_my_dict_get_attribute(self):
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

    def test_my_dict_set_attribute(self):
        with self.assertRaises(AttributeError):
            self.dict3.three = 3
        self.assertEqual(
            self.dict3.dictionary_of_attributes,
            self.data3
        )









