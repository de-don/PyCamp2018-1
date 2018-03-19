class ReadOnlyDictionary:
    """Class allows to transform Python dict() into attributes

    """
    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('Input data must Python dict()')

        self._dictionary = dictionary

        cls = type(self)

        # transform internal dictionary into ReadOnlyDictionary
        for key, value in self._dictionary.items():
            if isinstance(self._dictionary[key], dict):
                self._dictionary[key] = cls(value)

        # get list of proper attribute names
        self._attribute_names = tuple(self._dictionary.keys())

    # def __getattr__(self, item):





