from collections import Counter


def keys_counter(list_of_dicts):
    """ Function counts unique combinations of key: value pairs in list of dictionaries.
    Args:
        list_of_dicts (list): list of Python dict() objects
            Example:
            [{key1: val1, key2: val2, key3:val3},
            {key1: val4, key2: val2, key3:val5}
            ]

    Returns:
        sum_keys_vals (list): list of Python dict() objects
            Every dictionary contains unique pair key: value and results of count in list_of_dicts.
            Example:
            [{'key': key1, value: val1, count: 1},
            {'key': key1, value: val4, count: 1},
            {'key': key2, value: val2, count: 2},
            {'key': key3, value: val3, count: 1},
            {'key': key3, value: val5, count: 1},
            ]
    """
    keys_and_vals = list()
    for d in list_of_dicts:
        # list of unique pairs key, value
        keys_and_vals += [(('key', k), ('value', v)) for k, v in d.items()]

    sum_keys_vals = list()
    # count unique (('key', k), ('value', v)) tuples
    count = Counter(keys_and_vals)
    for c in count.items():
        # c is a tuple, containing further information:
        # ((('key', k), ('value', v)), count)
        d = dict(c[0])
        d['count'] = c[1]
        sum_keys_vals.append(d)

    return sum_keys_vals


