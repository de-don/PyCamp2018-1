import csv
from dateutil import parser
from datetime import datetime
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


def header_exist(method_to_decorate):
    def wrapper(self, *header):
        if all(head in self._headers for head in header):
            return method_to_decorate(self, *header)
        raise KeyError(f'No such header: {header}')
    return wrapper


class Data:
    """ Class to store and manipulate data from table-like sources

    """

    _conversion_funcs = [int, float, parser.parse]

    def __init__(self):
        self._headers = list()
        self._entries = list()

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

    def _add_headers(self, list_of_headers):
        self._headers += list_of_headers

    def _represents_type(self, some_type, value):
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

        entry = dict(zip(self._headers, casted_entry_vals))
        self._entries.append(entry)

    @classmethod
    def get_csv(self, filename, delimiter=','):
        """Get data from .csv file

        """

        data = Data()
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            # print(reader.next())
            # get header from first row of csv
            data._add_headers(next(reader))

            # get entries from csv
            for row in reader:
                data._add_entry(row)
        return data

    def _entry_repr(self, entry):
        """Return string representation of an entry

        """
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

    def count(self):
        """Return number of entries

        """
        return len(self)

    @header_exist
    def summa(self, field_name):
        """Return sum of values from field_name of each entry

        """
        return sum(entry[field_name] for entry in self._entries)

    def average(self, field_name):
        """Return average value from field_name of each entry

        """
        return self.summa(field_name) / self.count()

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

    def simple_filter(self, **filter_params):
        """Return Data object """
        filtered_data = Data()

        for filter_param, filter_value in filter_params.items():
            for entry in self._entries:
                if entry[filter_param] == filter_value:
                    print(entry)



    def filter(self, **filter_params):
        """Return Data object with filtered entries

        """
        filtered_headers = self._headers
        filtered_entries = list()
        # dictionary of filtering methods
        # key is name of method, value is argument
        filter_methods = dict()

        for filter_param in filter_params:
            # if no calls of method, filter parameter is 'greater than'
            if CALL_METHOD_MARK not in filter_param:
                object_name = filter_param
                # save method and value to path the method
                filter_methods[object_name] = [
                    # filtering method
                    gt,
                    # parameter of filtering method
                    filter_params[filter_param]
                ]
            # if calls method, split object name and method name
            else:
                object_name, method_name = filter_param.split(CALL_METHOD_MARK, 1)
                # if comparison method
                if method_name in COMPARISON_OPERATORS:
                    filter_methods[object_name] = [
                        # filtering method
                        COMPARISON_OPERATORS[method_name],
                        # parameter of filtering method
                        filter_params[filter_param]
                    ]
                else:
                    filter_methods[object_name] = [
                        # use callable method with passed param
                        methodcaller(method_name, filter_param)
                    ]



        # for key in filter_methods:
        #     filtered = list(
        #         map(
        #             # filter parameter
        #             filter_methods[key],
        #             self._entries
        #         )
        #     )

