import csv
import abc
import json
from dateutil import parser
from datetime import datetime
from itertools import compress
from operator import itemgetter, methodcaller, lt, le, eq, ne, ge, gt


# dictionary of comparison operators
COMPARISON_OPERATORS = {
    'lt': lt,
    'le': le,
    'eq': eq,
    'ne': ne,
    'ge': ge,
    'gt': gt
}


CALL_METHOD_MARK = '__'


class FileExtensionError(Exception):
    """Raises when try to read data from unsupported file type"""


class AbstractDataProvider(abc.ABC):
    """Class to read data from some source

    """



class DataProvider:
    """Class to read data from different

    """

    def _csv_reader(self, filename, delimiter):
        """Get data from .csv file

        """

        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            # print(reader.next())
            # get header from first row of csv
            csv_headers = next(reader)

            # get entries from csv
            csv_entries = list()
            for row in reader:
                csv_entries.append(row)

        return csv_headers, csv_entries

    @classmethod
    def read_data(self, file_name, file_type, **kwargs):
        """Read data from file of supported type

        """

        _supported_sources = {
            'csv': self._csv_reader
        }

        if file_type not in _supported_sources:
            raise FileExtensionError(
                f'No support of reading data from .{file_type} files'
            )

        return _supported_sources[file_type](file_name)

    @classmethod
    def write_data(self, file_name, file_type, **kwargs):
        """Read data to file of supported type

        """

        _supported_receivers = {

        }

        if file_type not in _supported_receivers:
            raise FileExtensionError(
                f'No support of reading data from .{file_type} files'
            )

        return _supported_receivers[file_type](file_name)



def header_exist(method_to_decorate):
    """Check that header exists in data

    """
    def wrapper(self, *header):
        if all(head in self._headers for head in header):
            return method_to_decorate(self, *header)
        raise KeyError(f'No such header: {header}')
    return wrapper


class Data:
    """ Class to store and manipulate data from table-like sources

    """

    # functions used for conversion from string into some type
    _conversion_funcs = [int, float, parser.parse]

    def __init__(self, headers=None, entries=None):
        self._headers = headers
        self._entries = entries

    def _entry_repr(self, entry):
        """Return string representation of an entry

        """
        entry_lines = list()
        for key, value in entry.items():
            entry_lines.append(f'   {key}: {value}')
        return '\n'.join(entry_lines)

    def _represents_type(self, some_type, value):
        """Check if value can be casted into some type"""
        try:
            some_type(value)
            return True
        except ValueError:
            return False

    def _get_entry(self, headers, entry_values):
        """Convert string of entry values into entry, represented as dict.

        Can convert string into supported types

        """
        # convert types of values
        casted_entry_vals = list()
        for val in entry_values:
            # try each of probable types to cast
            for cast_type in self._conversion_funcs:
                if self._represents_type(cast_type, val):
                    after_cast = cast_type(val)
                    if isinstance(after_cast, datetime):
                        after_cast = after_cast.date()
                    casted_entry_vals.append(after_cast)
                    break
            # or do not cast and save as sting
            else:
                casted_entry_vals.append(val)

        entry = dict(zip(headers, casted_entry_vals))
        # self._entries.append(entry)
        return entry

    @property
    def headers(self):
        return self._headers

    @property
    def entry_size(self):
        if self._headers:
            return len(self._headers)
        return 0

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, item):
        return self._entries[item]

    def __iter__(self):
        return iter(self._entries)

    def __repr__(self):
        entries_repr = list()
        if not len(self):
            return 'Data()'
        for i in range(len(self)):
            entry_repr = self._entry_repr(self._entries[i])
            entries_repr.append(f'{i}:\n{entry_repr}')
        return '\n'.join(entries_repr)

    #

    @classmethod
    def get_csv(self, filename, delimiter=','):
        """Get data from .csv file

        """
        csv_entries = list()

        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            # print(reader.next())
            # get header from first row of csv
            csv_headers = next(reader)

            # get entries from csv
            for row in reader:
                csv_entries.append(self()._get_entry(csv_headers, row))

        return Data(csv_headers, csv_entries)

    @classmethod
    def get_json(self, filename):
        """Get data from json file

        """
        with open(filename, 'r') as json_out:
            data = json.load(json_out)
            # get headers
            json_headers = list(data.keys())
            # list of lists for aggregating entry values
            json_entries_strings = list(zip(*list(data.values())))
            json_entries = list()
            for entry_string in json_entries_strings:
                json_entries.append(self()._get_entry(
                    json_headers, entry_string
                ))

            return Data(json_headers, json_entries)

    def print_csv(self, filename, delimiter=','):
        """Write Data into csv file

        """
        with open(filename, 'w') as csv_file:
            entry_writer = csv.writer(csv_file, delimiter=delimiter)

            # write headers
            entry_writer.writerow(self._headers)

            for entry in self._entries:
                # build string of entry values
                entry_string_values = [
                    str(entry[header]) for header in self._headers
                ]
                entry_writer.writerow(entry_string_values)

    def print_json(self, filename):
        """Write Data into json file

        """
        with open(filename, 'w') as json_out:
            entry_strings = {header: list() for header in self._headers}

            for entry in self._entries:
                for entry_key, entry_value in entry.items():
                    entry_strings[entry_key].append(str(entry_value))

            json.dump(entry_strings, json_out)

    def print_html_table(self, filename):
        return

    def copy(self):
        return Data(self._headers, self._entries)

    def count(self):
        """Return number of entries

        """
        return len(self)

    @header_exist
    def summa(self, field_name):
        """Return sum of values from field_name of each entry

        """
        return sum(entry[field_name] for entry in self._entries)

    @header_exist
    def columns(self, *headers):
        """Return new Data() with only selected columns

        """
        from_columns = Data()

        entries_from_columns = [
            {
                key: value
                for key, value in entry.items()
                if key in headers
            }
            for entry in self._entries
        ]
        from_columns._headers = list(headers)
        from_columns._entries = entries_from_columns

        return from_columns

    @header_exist
    def unique(self, header):
        """Return only values from header

        """
        return list({value[header] for value in self._entries})

    def average(self, field_name):
        """Return average value from field_name of each entry

        """
        return self.summa(field_name) / self.count()

    def order_by(self, header, reversed=False):
        """Return Data object with sorted entries

        """
        if header not in self._headers:
            raise KeyError(f'No such header: {header}')

        sorted_data = Data()

        sorted_entries = sorted(
            self._entries,
            key=itemgetter(header),
            reverse=reversed
        )

        sorted_data._headers = self._headers
        sorted_data._entries = sorted_entries

        return sorted_data

    def filtered(self, **filter_params):
        """Return Data object with filtered entries

        """
        filtered_data = self.copy()

        filter_results = [True for _ in self._entries]

        for filter_param, filter_value in filter_params.items():
            # if no calls of method, filter parameter is 'greater than'
            if CALL_METHOD_MARK not in filter_param:

                res = [entry[filter_param] == filter_value for entry in
                       self._entries]
            else:
                # split into field name of entry and name of function
                object_name, method_name = filter_param.split(CALL_METHOD_MARK, 1)
                # if comparison method
                if method_name in COMPARISON_OPERATORS:
                    operation = COMPARISON_OPERATORS[method_name]
                    res = [operation(entry[object_name], filter_value)
                           for entry in self._entries]

                else:
                    # use callable method with passed param
                    operation = methodcaller(method_name, filter_value)
                    res = [operation(entry[object_name])
                           for entry in self._entries]

            filter_results = list(
                map(lambda x, y: x & y, filter_results, res))

        filtered_data._entries = list(compress(self._entries, filter_results))

        return filtered_data

