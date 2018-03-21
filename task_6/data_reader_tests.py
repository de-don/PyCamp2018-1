from unittest import TestCase
from .data_reader import Data
from datetime import datetime, date


class DataReaderTest(TestCase):

    def test_data_get_csv(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        self.assertTrue(isinstance(d, Data))

    def test_data_len(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        entries = 3
        self.assertTrue(len(d) == entries)

    def test_data_iterable(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        for entry in iter(d):
            self.assertTrue(isinstance(entry, dict))

    def test_type_cast(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        headers = d._headers
        entry = d[0]
        self.assertTrue(isinstance(entry[headers[0]], str))
        self.assertTrue(isinstance(entry[headers[1]], int))
        self.assertTrue(isinstance(entry[headers[2]], str))
        self.assertTrue(isinstance(entry[headers[3]], date))

    def test_data_headers(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.headers, d._headers)

    def test_data_count_method(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.count(), len(d))

    def test_data_summa(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.summa('age'), sum(e['age'] for e in d._entries))

    def test_data_summa_raises_key_error_for_wrong_fieldname(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        with self.assertRaises(KeyError):
            d.summa('university')

    def test_data_average(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        print(d.average('age'))
        self.assertEqual(
            d.average('age'),
            sum(e['age'] for e in d._entries) / d.count()
        )





