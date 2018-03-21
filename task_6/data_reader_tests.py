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

    def tests_data_get_new_data_from_single_column(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        d2 = d.columns('name')
        self.assertTrue(isinstance(d2, Data))
        self.assertEqual(d2.entry_size, 1)
        with self.assertRaises(KeyError):
            d3 = d.columns('newname')

    def tests_data_get_new_data_from_multiple_columns(self):
        fname = 'table.csv'
        d = Data().get_csv(fname)
        d2 = d.columns('name', 'age')
        self.assertTrue(isinstance(d2, Data))
        self.assertEqual(d2.entry_size, 2)
        with self.assertRaises(KeyError):
            d3 = d.columns('newname', 'name')
        with self.assertRaises(KeyError):
            d3 = d.columns('newname', 'newage')

    def test_data_unique_values(self):
        fname = 'table2.csv'
        d = Data().get_csv(fname)
        self.assertNotEqual(len(d.unique('age')), len(d))
        self.assertEqual(len(d.unique('city')), len(d))
        with self.assertRaises(KeyError):
            d2 = d.unique('newname')






