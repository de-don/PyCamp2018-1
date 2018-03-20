from copy import deepcopy


class ReadOnlyDictionary:
    """Class transforms dict() keys into attributes and gives
    read-only access to dict() values using attributes

    """

    _dictionary_of_attributes = {'_dictionary_of_attributes': 1}

    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('Input data must be Python dict()')

        self._dictionary_of_attributes = deepcopy(dictionary)

        cls = type(self)

        # transform internal dictionary into ReadOnlyDictionary
        for key, value in self._dictionary_of_attributes.items():
            t = type(self._dictionary_of_attributes[key])
            if isinstance(self._dictionary_of_attributes[key], dict):
                self._dictionary_of_attributes[key] = cls(value)

    @property
    def dictionary_of_attributes(self):
        """Displays dictionary of attributes"""
        return self._dictionary_of_attributes

    def __len__(self):
        return len(self.dictionary_of_attributes)

    def __eq__(self, other):
        if not isinstance(other, ReadOnlyDictionary):
            return False
        else:
            return self._dictionary_of_attributes == other._dictionary_of_attributes

    def __repr__(self):
        if not len(self):
            return '{No attributes}'

        attribute_strings = list()

        # find longest name of attribute
        attribute_name = '  |{}|: '
        attribute_names = [str(name)
                           for name in self._dictionary_of_attributes.keys()]
        max_attribute_name = len(max(attribute_names, key=len))

        for key, value in self._dictionary_of_attributes.items():
            # each line with name of key must have same length
            key_line = attribute_name.format(key).ljust(max_attribute_name)
            if isinstance(value, ReadOnlyDictionary):
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
        string = 'Read-Only Dictionary\n'
        return ''.join([string, repr(self), '\n'])

    def __getitem__(self, item):
        if item in self.dictionary_of_attributes.keys():
            return self.dictionary_of_attributes[item]
        raise IndexError

    def __getattr__(self, item):
        if item in self.dictionary_of_attributes.keys():
            return self.dictionary_of_attributes[item]
        raise AttributeError('No such attribute')

    def __setattr__(self, name, value):
        # print('RO setattr')
        if name == '_dictionary_of_attributes':
            super().__setattr__(name, value)
        elif name in self.dictionary_of_attributes.keys():
            raise AttributeError('Attribute is read-only')
        else:
            raise AttributeError('Attribute add forbidden')


class ReadModifyDictionary(ReadOnlyDictionary):
    """Class transforms dict() keys into attributes and gives
    read and modify access to dict() values using attributes

    """

    def __setattr__(self, name, value):
        # print('RM setattr')
        if name == '_dictionary_of_attributes':
            super().__setattr__(name, value)
        elif name in self.dictionary_of_attributes.keys():
            self._dictionary_of_attributes[name] = value
        else:
            raise AttributeError('Attribute add forbidden')

    def __str__(self):
        string = 'Read-and-Modify Dictionary\n'
        return ''.join([string, repr(self), '\n'])


class ReadAddModifyDictionary(ReadModifyDictionary):
    """Class transforms dict() keys into attributes and gives
    read, add and modify access to dict() values using attributes

    """

    def __setattr__(self, name, value):
        # print('RAM setattr')
        if name not in self.dictionary_of_attributes.keys():
            self._dictionary_of_attributes[name] = value
        super().__setattr__(name, value)

    def __str__(self):
        string = 'Read-Add-Modify Dictionary\n'
        return ''.join([string, repr(self), '\n'])


class ReadAddModifyDeleteDictionary(ReadAddModifyDictionary):
    """Class transforms dict() keys into attributes and gives
    read, add and modify access to dict() values using attributes

    """

    def __delattr__(self, item):
        # print('Delete attribute')
        if item not in self._dictionary_of_attributes.keys():
            raise AttributeError
        del self._dictionary_of_attributes[item]

    def __str__(self):
        string = 'Read-Add-Modify-Delete Dictionary\n'
        return ''.join([string, repr(self), '\n'])
