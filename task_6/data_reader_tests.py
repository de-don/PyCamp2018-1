from unittest import TestCase
from .data_reader import Data
from datetime import datetime, date


class DataReaderTest(TestCase):

    def test_data_get_csv(self):
        d = Data().get_csv('table.csv')
        self.assertTrue(isinstance(d, Data))

    def test_data_len(self):
        d = Data().get_csv('table.csv')
        self.assertTrue(len(d) == 3)

    def test_data_iterable(self):
        d = Data().get_csv('table.csv')
        for entry in iter(d):
            self.assertTrue(isinstance(entry, dict))

    def test_type_cast(self):
        d = Data().get_csv('table.csv')
        headers = d._headers
        entry = d[0]
        self.assertTrue(isinstance(entry[headers[0]], str))
        self.assertTrue(isinstance(entry[headers[1]], int))
        self.assertTrue(isinstance(entry[headers[2]], str))
        self.assertTrue(isinstance(entry[headers[3]], date))



