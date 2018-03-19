from unittest import TestCase
from .custom_dictionaries import ReadOnlyDictionary as RODict


class ReadOnlyDictionaryTests(TestCase):
    def setUp(self):
        self.data1 = {'one': 1, 'two': 2}
        self.data2 = {'one': 1, 'two': {'three': 3, 'four': 4}}

    def test_init_ro_dict(self):
        with self.assertRaises(TypeError):
            RODict(['one', 1, 'two', 2])
        # transforms dict() values into self type()
        r_o_dict2 = RODict(self.data2)
        self.assertTrue(isinstance(
            r_o_dict2._dictionary['two'],
            RODict)
        )

        # check tuple of attribute names
        r_o_dict1 = RODict(self.data1)
        self.assertEqual(r_o_dict1._attribute_names, tuple(self.data1.keys()))







