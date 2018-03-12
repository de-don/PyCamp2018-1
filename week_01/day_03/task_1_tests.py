from unittest import TestCase
from .task_1 import keys_counter


class KeyCounterTest(TestCase):
    """"""
    def test_simple_case(self):
        given = [{'id': 1, 'success': True, 'name': 'Lary'},
                 {'id': 2, 'success': False, 'name': 'Rabi'},
                 {'id': 3, 'success': True, 'name': 'Alex'}]
        expect = [{'key': 'id', 'value': 1, 'count': 1},
                  {'key': 'success', 'value': True, 'count': 2},
                  {'key': 'name', 'value': 'Lary', 'count': 1},
                  {'key': 'id', 'value': 2, 'count': 1},
                  {'key': 'success', 'value': False, 'count': 1},
                  {'key': 'name', 'value': 'Rabi', 'count': 1},
                  {'key': 'id', 'value': 3, 'count': 1},
                  {'key': 'name', 'value': 'Alex', 'count': 1}]

        self.assertEqual(keys_counter(given), expect)

    def test_empty_list(self):
        self.assertEqual(keys_counter([]), [])

    def test_uniq_dicts(self):
        given = [{'id': 1, 'success': True, 'name': 'Lary'},
                 {'id': 2, 'success': False, 'name': 'Rabi'},]
        expect = [{'key': 'id', 'value': 1, 'count': 1},
                  {'key': 'success', 'value': True, 'count': 1},
                  {'key': 'name', 'value': 'Lary', 'count': 1},
                  {'key': 'id', 'value': 2, 'count': 1},
                  {'key': 'success', 'value': False, 'count': 1},
                  {'key': 'name', 'value': 'Rabi', 'count': 1},]

        self.assertEqual(keys_counter(given), expect)

    def test_similar_dicts(self):
        given = [{'id': 1, 'success': True, 'name': 'Lary'},
                 {'id': 2, 'success': True, 'name': 'Lary'},]
        expect = [{'key': 'id', 'value': 1, 'count': 1},
                  {'key': 'success', 'value': True, 'count': 2},
                  {'key': 'name', 'value': 'Lary', 'count': 2},
                  {'key': 'id', 'value': 2, 'count': 1},]

        self.assertEqual(keys_counter(given), expect)
