import csv
import abc
import json
import yaml
from dateutil import parser
from datetime import datetime
from itertools import compress, chain
from operator import itemgetter, methodcaller, lt, le, eq, ne, ge, gt


# dictionary of comparison operators
SUPPORTED_FUNCTIONS = {
    'lt': lt,
    'le': le,
    'eq': eq,
    'ne': ne,
    'ge': ge,
    'gt': gt
}


CUSTOM_FILTERS = {
    str: {

    },
    int: {

    }
}


CALL_METHOD_MARK = '__'


class FileExtensionError(Exception):
    """Raises when try to read data from unsupported file type"""


class AbstractDataProvider(abc.ABC):
    """Abstract class define interface to save or load data
    from some source

    """
    # functions used for conversion from string into some type
    _conversion_funcs = [int, float, parser.parse]

    def _represents_type(self, some_type, value):
        """Check if value can be casted into some type"""
        try:
            some_type(value)
            return True
        except ValueError:
            return False

    def _get_entries(self, headers, entry_values):
        """Convert string of entry values into entry, represented as dict.

        Can convert string into supported types

        """
        casted_file_entries = list()

        for entry_value in entry_values:
            # convert types of values
            casted_entry_vals = list()
            for val in entry_value:
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
            casted_file_entries.append(entry)

        return casted_file_entries

    @classmethod
    @abc.abstractclassmethod
    def load_data(cls, filename, **kwargs):
        pass

    @classmethod
    @abc.abstractclassmethod
    def save_data(cls, filename, headers, entries, **kwargs):
        pass


class CSVDataProvider(AbstractDataProvider):
    """Class to save or load data from .csv tables

    """

    @classmethod
    def load_data(cls, filename, **kwargs):
        """Method to get data from csv file

        Args:
            filename (str): source filename with extension
            **kwargs : optional argument for opening csv file
                *23/03/18 - defined only for csv delimiter symbol

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """
        # cvs file delimiter
        if kwargs.get('delimiter'):
            delimiter = kwargs.get('delimiter')
        else:
            delimiter = ','

        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)

            # get header from first row of csv
            csv_headers = next(reader)

            # get entries from csv
            csv_entries = list()
            for row in reader:
                csv_entries.append(row)

        return csv_headers, cls()._get_entries(csv_headers, csv_entries)

    @classmethod
    def save_data(cls, filename, headers, entries, **kwargs):
        """Method to save data as csv file

        Args:
            filename (str): filename with extension
            headers (list): list of strings with heades names
            entries (list): list of entries. Each entry is dict()
                with headers used as keys.

            **kwargs : optional argument for work with csv file
                *23/03/18 - defined only for csv delimiter symbol

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """
        # cvs file delimiter
        if kwargs.get('delimiter'):
            delimiter = kwargs.get('delimiter')
        else:
            delimiter = ','

        with open(filename, 'w') as csv_file:
            entry_writer = csv.writer(csv_file, delimiter=delimiter)

            # write headers
            entry_writer.writerow(headers)

            for entry in entries:
                # build string of entry values
                entry_string_values = [
                    str(entry[header]) for header in headers
                ]
                entry_writer.writerow(entry_string_values)


class JSONDataProvider(AbstractDataProvider):
    """Class to save or load data from .json files of such format:
        {
            "name" : ["name_1", "name_2, ..."]
            "city" : ["city_1", "city_2, ..."]
            "age" : ["age_1", "age_2, ..."]
        }

    """

    @classmethod
    def load_data(cls, filename, **kwargs):
        """Method to get data from csv file

        Args:
            filename (str): source filename with extension
            **kwargs : optional arguments for opening json file
                *23/03/18 - not defined

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """
        with open(filename, 'r') as json_out:
            data = json.load(json_out)
            # get headers
            json_headers = list(data.keys())
            # list of lists for aggregating entry values
            json_entries_strings = list(zip(*list(data.values())))

            return json_headers, cls()._get_entries(json_headers,
                                                    json_entries_strings)

    @classmethod
    def save_data(cls, filename, headers, entries, **kwargs):
        """Method to save data as csv file

        Args:
            filename (str): filename with extension
            headers (list): list of strings with heades names
            entries (list): list of entries. Each entry is dict()
                with headers used as keys.

            **kwargs : optional argument for work with csv file
                *23/03/18 - defined only for csv delimiter symbol

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """
        with open(filename, 'w') as json_out:
            entry_strings = {header: list() for header in headers}

            for entry in entries:
                for entry_key, entry_value in entry.items():
                    entry_strings[entry_key].append(str(entry_value))

            json.dump(entry_strings, json_out)


class HTMLDataProvider(AbstractDataProvider):
    """Class to load data to .html tables

    """
    _table_template = '<table>\n{}\n</table>'
    _row_template = '\t<tr>\n{}\n</tr>'
    # _header_template = '<th>{}</th>'
    # _cell_template = '<td>{}</td>'

    def _build_row(self, cells, header=False):
        """Build a row of html table using list of cell values

        Args:
            cells (list): list of values to build row of table
            header (bool): defines if use header tag <th>
                or data element tag <td>

        Returns:
            html_table_row (str): representation of html table's row
        """
        if header:
            html_cells = [
                f'\t\t<th>{str(cell)}</th>' for cell in cells
            ]
        else:
            html_cells = [
                f'\t\t<td>{str(cell)}</td>' for cell in cells
            ]

        html_table_row = self._row_template.format('\n'.join(html_cells))
        return html_table_row

    @classmethod
    def load_data(cls, filename, **kwargs):
        """Method to get data from html file
        *23/03/18 - NOT SUPPORTED
        """
        raise FileExtensionError('Reading from .html file is not supported')

    @classmethod
    def save_data(cls, filename, headers, entries, **kwargs):
        """Method to save data as csv file

        Args:
            filename (str): filename with extension
            headers (list): list of strings with heades names
            entries (list): list of entries. Each entry is dict()
                with headers used as keys.

            **kwargs : optional argument for work with csv file
                *23/03/18 - not defined

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """

        with open(filename, 'w') as html_file:
            html_rows = list()

            # make a row of  headers
            html_rows.append(cls()._build_row(headers, header=True))

            for entry in entries:
                # select values from entry dict
                entry_string_values = [
                    str(entry[header]) for header in headers
                ]
                html_rows.append(cls()._build_row(entry_string_values))
            html_file.write(
                cls._table_template.format(
                    '\n'.join(html_rows)
                )
            )


class YAMLDataProvider(AbstractDataProvider):
    """Class to save or load data from .yaml tables

    """

    @classmethod
    def load_data(cls, filename, **kwargs):
        """Method to get data from csv file

        Args:
            filename (str): source filename with extension
            **kwargs : optional argument for opening csv file
                *23/03/18 - defined only for csv delimiter symbol

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """

        with open(filename, 'r') as yml_file:
            yml_entries = yaml.load(yml_file)

            # get headers from all entries
            all_keys = set(chain.from_iterable(yml_entries))

            # check each entry has same headers as others
            if not all(all_keys == entry.keys() for entry in yml_entries):
                raise KeyError('Entries with different fields were passed')

        return all_keys, yml_entries

    @classmethod
    def save_data(cls, filename, headers, entries, **kwargs):
        """Method to save data as csv file

        Args:
            filename (str): filename with extension
            headers (list): list of strings with heades names
            entries (list): list of entries. Each entry is dict()
                with headers used as keys.

            **kwargs : optional argument for work with csv file
                *23/03/18 - defined only for csv delimiter symbol

        Returns:
            csv_headers (list): headers of csv table
            csv_entries (list): rows of csv table. Each row is list of values
                according to csv headers
        """
        with open(filename, 'w') as outfile:
            yaml.dump(entries, outfile, default_flow_style=False)


def header_exist(method_to_decorate):
    """Check that header exists in data

    """
    def wrapper(self, *header):
        if all(head in self._headers for head in header):
            return method_to_decorate(self, *header)
        raise KeyError(f'No such header: {header}')
    return wrapper


def add_filter(filter_to_decorate):
    """Adds custom filter to SUPPORTED_FUNCTIONS dict

    """
    # add filter_to_decorate to supported functions
    SUPPORTED_FUNCTIONS[filter_to_decorate.__name__] = filter_to_decorate

    def wrapper(value, condition):
        return filter_to_decorate(value, condition)

    return wrapper


def add_custom_filter(**kwargs):
    """Adds custom filter to SUPPORTED_FUNCTIONS dict

    """

    def filter_decorator(filter_to_decorate):
        if not kwargs.get('types'):
            raise TypeError('Types of custom filtering must be defined')

        # add filter_to_decorate to supported functions
        for data_type in kwargs['types']:
            CUSTOM_FILTERS[data_type].update(
                {
                    filter_to_decorate.__name__:
                    filter_to_decorate
                }
            )

        def wrapper(value, condition):
            return filter_to_decorate(value, condition)

        return wrapper

    return filter_decorator


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

    # ##########################################################################
    # Old methods to work with data sources
    # ##########################################################################

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

    # ##########################################################################
    # New methods for loading and saving
    # ##########################################################################

    @classmethod
    def load_from_file(self, data_provider, filename, **kwargs):
        """Method to create Data() object using data from some file.

        Args:
            data_provider: loads data from some source.
                Must be inheritor of AbstractDataProvider class.
            filename (str): filename with extension for reading data
            **kwargs : optional arguments for opening file


        Returns:
            file_data (Data()): Data object with entries from the source.

        """
        if not isinstance(data_provider, AbstractDataProvider):
            raise TypeError('Data provider must be inheritor of '
                            'AbstractDataProvider class')

        file_headers, file_entries = data_provider.load_data(filename, **kwargs)

        file_data = Data(file_headers, file_entries)
        return file_data

    def save_to_file(self, data_provider, filename, **kwargs):
        """Method to create some file using data fromData() object .

        Args:
            data_provider: loads data from some source.
                Must be inheritor of AbstractDataProvider class.
            filename (str): filename with extension for saving data
            **kwargs : optional arguments for opening file

        """
        if not isinstance(data_provider, AbstractDataProvider):
            raise TypeError('Data provider must be inheritor of '
                            'AbstractDataProvider class')

        data_provider.save_data(
            filename,
            self._headers,
            self._entries,
            **kwargs
        )

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
            # if no calls of method, filter parameter is 'is equal'
            if CALL_METHOD_MARK not in filter_param:

                res = [entry[filter_param] == filter_value for entry in
                       self._entries]
            else:
                # split into field name of entry and name of function
                object_name, method_name = filter_param.split(CALL_METHOD_MARK, 1)
                # if comparison method
                if method_name in SUPPORTED_FUNCTIONS:
                    operation = SUPPORTED_FUNCTIONS[method_name]
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

    def advanced_filters(self, **filter_params):
        """Return Data object with filtered entries

        """
        filtered_data = self.copy()

        filter_results = list()

        for entry in filtered_data._entries:
            # mark that filter allow current entry to go further
            entry_is_ok = True

            # applying filters to entry one by one
            for filter_param, filter_value in filter_params.items():
                # if no calls of method, filter parameter is 'is equal'
                if CALL_METHOD_MARK not in filter_param:
                    entry_is_ok &= entry[filter_param] == filter_value
                    # filter kicks out object
                    if not entry_is_ok:
                        break

                # split into field name of entry and name of function
                object_name, method_name = filter_param.split(
                    CALL_METHOD_MARK, 1)

                # if comparison method
                if method_name in SUPPORTED_FUNCTIONS:
                    operation = SUPPORTED_FUNCTIONS[method_name]
                    entry_is_ok &= operation(entry[object_name], filter_value)
                    # filter kicks out object
                    if not entry_is_ok:
                        break

                elif hasattr(entry[object_name], method_name):
                    # use callable method with passed param
                    operation = methodcaller(method_name, filter_value)

                    entry_is_ok &= operation(entry[object_name])
                    # filter kicks out object
                    if not entry_is_ok:
                        break

                # if used custom filter for data type
                elif type(entry[object_name]) in CUSTOM_FILTERS:
                    operation = CUSTOM_FILTERS[type(entry[object_name])][method_name]
                    entry_is_ok &= operation(entry[object_name], filter_value)

            # save result of applying filter
            filter_results.append(entry_is_ok)

        filtered_data._entries = list(compress(self._entries, filter_results))

        return filtered_data


