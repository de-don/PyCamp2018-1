from unittest import TestCase
from .data_reader import Data
from datetime import datetime, date
from pathlib import Path


input_folder = Path("./task_6/input/")
output_folder = Path("./task_6/output/")


class DataReaderTest(TestCase):

    def test_data_get_csv(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        self.assertTrue(isinstance(d, Data))

    def test_data_len(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        entries = 3
        self.assertTrue(len(d) == entries)

    def test_data_entry_size(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.entry_size, len(d._headers))
        d2 = Data()
        self.assertEqual(d2.entry_size, 0)

    def test_data_iterable(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        for entry in iter(d):
            self.assertTrue(isinstance(entry, dict))

    def test_type_cast(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)
        headers = d._headers
        entry = d[0]
        self.assertTrue(isinstance(entry[headers[0]], str))
        self.assertTrue(isinstance(entry[headers[1]], int))
        self.assertTrue(isinstance(entry[headers[2]], str))
        self.assertTrue(isinstance(entry[headers[3]], date))

    def test_data_headers(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.headers, d._headers)

    def test_data_count_method(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.count(), len(d))

    def test_data_summa(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(d.summa('age'), sum(e['age'] for e in d._entries))

    def test_data_summa_raises_key_error_for_wrong_fieldname(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        with self.assertRaises(KeyError):
            d.summa('university')

    def test_data_average(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        self.assertEqual(
            d.average('age'),
            sum(e['age'] for e in d._entries) / d.count()
        )

    def tests_data_get_new_data_from_single_column(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        d2 = d.columns('name')
        self.assertTrue(isinstance(d2, Data))
        self.assertEqual(d2.entry_size, 1)
        with self.assertRaises(KeyError):
            d3 = d.columns('newname')

    def tests_data_get_new_data_from_multiple_columns(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        d2 = d.columns('name', 'age')
        self.assertTrue(isinstance(d2, Data))
        self.assertEqual(d2.entry_size, 2)
        with self.assertRaises(KeyError):
            d3 = d.columns('newname', 'name')
        with self.assertRaises(KeyError):
            d3 = d.columns('newname', 'newage')

    def test_data_unique_values(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)
        self.assertNotEqual(len(d.unique('age')), len(d))
        self.assertEqual(len(d.unique('city')), len(d))
        with self.assertRaises(KeyError):
            d2 = d.unique('newname')

    def test_data_order_by(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)
        d2 = d.order_by('age')
        self.assertEqual(len(d), len(d2))
        self.assertNotEqual(repr(d), repr(d2))

    def test_data_order_by_reversed(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)
        d2 = d.order_by('name')
        d3 = d.order_by('name', reversed=True)
        self.assertEqual(len(d3), len(d2))
        self.assertNotEqual(repr(d3), repr(d2))

    def test_data_order_by_raises_keyerror(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)
        with self.assertRaises(KeyError):
            d2 = d.order_by('country', reversed=True)

    def test_data_equality(self):
        fname = input_folder / 'table.csv'
        d = Data().get_csv(fname)
        d2 = Data(
            ['name', 'age', 'city'],
            [
                {'name': 'John', 'age': 32, 'city': 'NY'},
                {'name': 'Sam', 'age': 18, 'city': 'LA'},
                {'name': 'Igor', 'age': 47, 'city': 'Krasnoyarsk'}
            ]
        )
        self.assertEqual(repr(d), repr(d2))

    def test_data_copy(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)
        d2 = d.copy()
        self.assertEqual(repr(d), repr(d2))
        self.assertFalse(id(d) == id(d2))

    headers = ['name', 'age', 'city', 'birthday']
    entries = [
        {'name': 'John', 'age': 32, 'city': 'NY',
         'birthday': date(1986, 10, 10)},
        {'name': 'Sam', 'age': 18, 'city': 'LA',
         'birthday': date(2000, 1, 11)},
        {'name': 'Igor', 'age': 47, 'city': 'Krasnoyarsk',
         'birthday': date(1971, 10, 20)},
        {'name': 'John', 'age': 18, 'city': 'Los Angeles',
         'birthday': date(1999, 10, 11)}
    ]

    def test_data_filtered_single_equal_filter(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(age=18)
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            [
                {'name': 'Sam', 'age': 18, 'city': 'LA',
                 'birthday': date(2000, 1, 11)},
                {'name': 'John', 'age': 18, 'city': 'Los Angeles',
                 'birthday': date(1999, 10, 11)}
            ]
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_filtered_several_equal_filters(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(age=18, name='John')
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            [
                {'name': 'John', 'age': 18, 'city': 'Los Angeles',
                 'birthday': date(1999, 10, 11)}
            ]
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_filtered_single_comparison_filter(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(age__gt=18)
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            [
                {'name': 'John', 'age': 32, 'city': 'NY',
                 'birthday': date(1986, 10, 10)},
                {'name': 'Igor', 'age': 47, 'city': 'Krasnoyarsk',
                 'birthday': date(1971, 10, 20)},
            ]
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_filtered_empty_result(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(age__lt=18)
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            []
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_filtered_several_comparison_filters(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(age__ge=18,
                                  birthday__gt=date(1980, 1, 1))
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            [
                {'name': 'John', 'age': 32, 'city': 'NY',
                 'birthday': date(1986, 10, 10)},
                {'name': 'Sam', 'age': 18, 'city': 'LA',
                 'birthday': date(2000, 1, 11)},
                {'name': 'John', 'age': 18, 'city': 'Los Angeles',
                 'birthday': date(1999, 10, 11)}
            ]
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_filtered_comparison_filter_and_method_filter(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(age__ge=18, name__startswith='S')
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            [
                {'name': 'Sam', 'age': 18, 'city': 'LA',
                 'birthday': date(2000, 1, 11)},
            ]
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_filtered_several_method_filters(self):
        fname = input_folder / 'table2.csv'
        d = Data().get_csv(fname)

        d2 = d.filtered(city__startswith='N', name__startswith='J')
        d3 = Data(
            ['name', 'age', 'city', 'birthday'],
            [
                {'name': 'John', 'age': 32, 'city': 'NY',
                 'birthday': date(1986, 10, 10)},
            ]
        )
        self.assertEqual(repr(d2), repr(d3))

    def test_data_read_csv_print_to_csv(self):
        read = input_folder / 'table2.csv'
        d = Data().get_csv(read)
        write = output_folder / 'write.csv'
        d.print_csv(write)
        d2 = Data().get_csv(write)
        self.assertEqual(repr(d), repr(d2))

    def test_data_read_csv_print_to_json(self):
        read = input_folder / 'table2.csv'
        d = Data().get_csv(read)
        write = output_folder / 'write.json'
        d.print_json(write)
        d2 = Data().get_json(write)
        self.assertEqual(repr(d), repr(d2))

    def test_data_read_json_print_to_csv(self):
        read = input_folder / 'read.json'
        d = Data().get_json(read)
        write = output_folder / 'write.csv'
        d.print_csv(write)
        d2 = Data().get_csv(write)
        self.assertEqual(repr(d), repr(d2))

    def test_data_read_json_print_to_json(self):
        read = input_folder / 'read.json'
        d = Data().get_json(read)
        write = output_folder / 'write.json'
        d.print_json(write)
        d2 = Data().get_json(write)
        self.assertEqual(repr(d), repr(d2))
















