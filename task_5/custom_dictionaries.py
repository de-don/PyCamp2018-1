class ReadOnlyDictionary:
    """Class transforms dict() keys into attributes and gives access to dict()
    values using attributes

    """
    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('Input data must Python dict()')

        self._dictionary_of_attributes = dictionary

        cls = type(self)

        # transform internal dictionary into ReadOnlyDictionary
        for key, value in self._dictionary_of_attributes.items():
            if isinstance(self._dictionary_of_attributes[key], dict):
                self._dictionary_of_attributes[key] = cls(value)

    @property
    def dictionary_of_attributes(self):
        """Displays dictionary of attributes"""
        return self._dictionary_of_attributes

    def __getitem__(self, item):
        if item in self.dictionary_of_attributes.keys():
            return self.dictionary_of_attributes[item]
        raise IndexError

    def __getattr__(self, item):
        if item in self.dictionary_of_attributes.keys():
            return self.dictionary_of_attributes[item]
        raise AttributeError('No such attribute')

    def __setattr__(self, name, value):
        if name in self.dictionary_of_attributes.keys():
            raise AttributeError('Attribute is read-only')
        super().__setattr__(name, value)






