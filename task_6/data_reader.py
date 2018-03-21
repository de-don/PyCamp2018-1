import csv
from datetime import datetime
from dateutil import parser


class Data:
    """ Class to store and manipulate data from table-like sources

    """

    _conversion_types = [float, int, bool, datetime]

    def __init__(self):
        self._headers = list()
        self._entries = list()

    def __len__(self):
        return len(self._entries)

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

        entry = dict(zip(self._headers, entry_values))
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
                print(row)
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


