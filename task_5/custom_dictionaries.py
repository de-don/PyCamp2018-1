from copy import deepcopy


class ReadOnly:
    """Class transforms dict() keys into attributes and gives
    read-only access to dict() values using attributes

    """

    _class_name = 'Read-Only Dictionary'

    _dictionary_of_attributes = {'_dictionary_of_attributes': 1}

    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('Input data must be Python dict()')

        self._dictionary_of_attributes = deepcopy(dictionary)

        cls = type(self)

        # transform internal dictionary into ReadOnlyDictionary
        for key, value in self._dictionary_of_attributes.items():
            if isinstance(self._dictionary_of_attributes[key], dict):
                self._dictionary_of_attributes[key] = cls(value)

    def __len__(self):
        return len(self._dictionary_of_attributes)

    def __repr__(self):
        if not len(self):
            return '{No attributes}'

        attribute_strings = list()

        # find longest name of attribute
        attribute_name = '  |{}|: '
        attribute_names = [str(name)
                           for name in self._dictionary_of_attributes]
        max_attribute_name = len(max(attribute_names, key=len))

        for key, value in self._dictionary_of_attributes.items():
            # each line with name of key must have same length
            key_line = attribute_name.format(key).ljust(max_attribute_name)
            if isinstance(value, ReadOnly):
                # split dictionary into single lines
                dict_lines = repr(value).split('\n')

                # first line of dict_lines starts with attribute_name
                dict_lines[0] = ''.join([key_line, dict_lines[0]])

                # shift right each line on length of key_line
                dict_lines[1:] = [' ' * len(key_line) + line
                                  for line in dict_lines[1:]]
                attribute_string = '\n'.join(dict_lines)
            else:
                attribute_string = ''.join([key_line, '{}'.format(value)])
            attribute_strings.append(attribute_string)

        return '{\n' + ',\n'.join(attribute_strings) + '\n}'

    def __str__(self):
        return '\n'.join([self._class_name, repr(self)])

    def __getattr__(self, name):
        if name in self._dictionary_of_attributes:
            return self._dictionary_of_attributes[name]
        raise AttributeError('No such attribute')

    def __setattr__(self, name, value):
        # print('RO setattr')
        if name == '_dictionary_of_attributes':
            return super().__setattr__(name, value)
        if name in self._dictionary_of_attributes:
            raise AttributeError('Attribute is read-only')
        raise AttributeError('Attribute add forbidden')

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __delitem__(self, name):
        return self.__getattr__(name)


class ReadModify(ReadOnly):
    """Class transforms dict() keys into attributes and gives
    read and modify access to dict() values using attributes

    """

    _class_name = 'Read-and-Modify Dictionary'

    def __setattr__(self, name, value):
        # print('RM setattr')
        if name == '_dictionary_of_attributes':
            super().__setattr__(name, value)
        elif name in self._dictionary_of_attributes:
            self._dictionary_of_attributes[name] = value
        else:
            raise AttributeError('Attribute add forbidden')


class ReadAddModify(ReadModify):
    """Class transforms dict() keys into attributes and gives
    read, add and modify access to dict() values using attributes

    """

    _class_name = 'Read-Add-Modify Dictionary'

    def __setattr__(self, name, value):
        # print('RAM setattr')
        if name not in self._dictionary_of_attributes:
            self._dictionary_of_attributes[name] = value
        super().__setattr__(name, value)


class ReadAddModifyDelete(ReadAddModify):
    """Class transforms dict() keys into attributes and gives
    read, add and modify access to dict() values using attributes

    """

    _class_name = 'Read-Add-Modify-Delete Dictionary'

    def __delattr__(self, item):
        # print('Delete attribute')
        if item not in self._dictionary_of_attributes:
            raise AttributeError('Deleting denied')
        del self._dictionary_of_attributes[item]


class ProtectedError(Exception):
    """Exception raises when try to set or get protected attribute of class

    """


class Protected(ReadAddModifyDelete):
    """Class transforms dict() keys into attributes and gives
    read, add and modify access to dict() values using attributes

    """

    _class_name = 'Protected Read-Add-Modify-Delete Dictionary'

    _protected_attributes = ['_protected_attributes']

    def __init__(self, dictionary, *protected_attrs):
        ReadAddModifyDelete.__init__(self, dictionary)

        self.__dict__['_protected_attributes'] = list()

        for protected in protected_attrs:
            # split with '.' one time to get highest level property from line
            if '.' in protected[:-1]:
                high_protected, low_protected = protected.split('.', 1)
            else:
                high_protected, low_protected = protected.split('.', 1)[0], None

            if high_protected not in self._dictionary_of_attributes:
                raise AttributeError(
                    f'No {high_protected} attribute in {self.__name__}'
                )

            # if low_protected attribute exist, protect high attribute
            # only if there is any nested Protected with protected attributes
            if low_protected:
                # if value of highest protected attribute is Protected dict
                # redefine it with low protected properties
                if isinstance(self._dictionary_of_attributes[high_protected], Protected):
                    nested_protected = Protected(dictionary[high_protected], low_protected)
                    self._dictionary_of_attributes[high_protected] = nested_protected

                    # get nested attribute from low_protected
                    if '.' in low_protected:
                        nested_attribute = low_protected.split('.', 1)[0]
                    else:
                        nested_attribute = low_protected

                    # check if nested Protected has protected attributes
                    if nested_attribute in nested_protected._protected_attributes:
                        self._protected_attributes.append(high_protected)

            else:
                if high_protected in self._dictionary_of_attributes:
                    self._protected_attributes.append(high_protected)

    def __setattr__(self, key, value):
        if key in self._protected_attributes:
            # print(self.__class__)
            raise ProtectedError(f'{key} attribute is forbidden to modify')
        super().__setattr__(key, value)

    def __delattr__(self, item):
        # print('Delete attribute')
        if item in self._protected_attributes:
            raise ProtectedError(f'{item} attribute is forbidden to delete')
        del self._dictionary_of_attributes[item]

