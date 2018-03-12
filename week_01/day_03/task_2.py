import warnings


def dict_merger(dict1, dict2):
    """Function merges two Python dictionaries
    Based on https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
    If two dictionaries have same keys with the same values, merged one contains key: value pair without changes.
    If two dictionaries have same keys with different values, merged one contains key: value pair from the second one.

    Returns:
        dict(): merged dictionary

    """
    for k in dict1.keys():
        if k in dict2.keys():  # and dict1[k] == dict2[k]:
            print('WARNING! Both dictionaries has key', k)
            print('{}: {} from dict1 will be replaced by {}: {} from dict2'.format(k, dict1[k], k, dict2[k]))
    return {**dict1, **dict2}






