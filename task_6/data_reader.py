import csv
from dateutil import parser
from datetime import datetime


class Data:
    """ Class to store and manipulate data from table-like sources

    """

    _conversion_types = [int, float, parser.parse]

    def __init__(self):
        self._headers = list()
        self._entries = list()

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, item):
        return self._entries[item]

    def __iter__(self):
        return iter(self._entries)

    def _add_headers(self, list_of_headers):
        self._headers += list_of_headers

    def _represents_some_type(self, some_type, value):
        try:
            some_type(value)
            return True
        except ValueError:
            return False

    def _add_entry(self, entry_values):
        # convert types of values
        casted_entry_vals = list()
        for val in entry_values:
            # try each of probable types to cast
            for cast_type in self._conversion_types:
                if self._represents_some_type(cast_type, val):
                    after_cast = cast_type(val)
                    if isinstance(after_cast, datetime):
                        after_cast = after_cast.date()
                    casted_entry_vals.append(after_cast)
                    break
            # or do not cast and save as sting
            else:
                casted_entry_vals.append(val)

        entry = dict(zip(self._headers, casted_entry_vals))
        self._entries.append(entry)

    @classmethod
    def get_csv(self, filename, delimiter=',', quotechar='|'):
        """Get data from .csv file"""

        data = Data()
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            # print(reader.next())
            # get header from first row of csv
            data._add_headers(next(reader))

            # get entries from csv
            for row in reader:
                data._add_entry(row)
        return data

    def _entry_repr(self, entry):
        """Return string representation of an entry"""
        entry_lines = list()
        for key, value in entry.items():
            entry_lines.append(f'   {key}: {value}')
        return '\n'.join(entry_lines)

    def __repr__(self):
        entries_repr = list()
        for i in range(len(self)):
            entry_repr = self._entry_repr(self._entries[i])
            entries_repr.append(f'{i}:\n{entry_repr}')
        return '\n'.join(entries_repr)
















