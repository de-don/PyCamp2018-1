from collections import Counter


def keys_counter(list_of_dicts):
    """"""
    keys_and_vals = list()
    for d in list_of_dicts:
        # if no such key-value
        keys_and_vals += [(('key', k), ('value', v)) for k, v in d.items()]

    sum_keys_vals = list()
    count = Counter(keys_and_vals)
    for c in count.items():
        d = dict(c[0])
        d['count'] = c[1]
        sum_keys_vals.append(d)

    return sum_keys_vals


