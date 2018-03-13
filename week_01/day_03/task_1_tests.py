from unittest import TestCase
from .task_1 import keys_counter


class KeyCounterTest(TestCase):
    def setUp(self):
        self.given = [
            [{'id': 1, 'success': True, 'name': 'Lary'},
             {'id': 2, 'success': False, 'name': 'Rabi'},
             {'id': 3, 'success': True, 'name': 'Alex'}],

            [{'id': 1, 'success': True, 'name': 'Lary'},
             {'id': 2, 'success': False, 'name': 'Rabi'}, ],

            [{'id': 1, 'success': True, 'name': 'Lary'},
             {'id': 2, 'success': True, 'name': 'Lary'}, ],
        ]
        self.expected = [
            [{'key': 'id', 'value': 1, 'count': 1},
             {'key': 'success', 'value': True, 'count': 2},
             {'key': 'name', 'value': 'Lary', 'count': 1},
             {'key': 'id', 'value': 2, 'count': 1},
             {'key': 'success', 'value': False, 'count': 1},
             {'key': 'name', 'value': 'Rabi', 'count': 1},
             {'key': 'id', 'value': 3, 'count': 1},
             {'key': 'name', 'value': 'Alex', 'count': 1}],

            [{'key': 'id', 'value': 1, 'count': 1},
             {'key': 'success', 'value': True, 'count': 1},
             {'key': 'name', 'value': 'Lary', 'count': 1},
             {'key': 'id', 'value': 2, 'count': 1},
             {'key': 'success', 'value': False, 'count': 1},
             {'key': 'name', 'value': 'Rabi', 'count': 1}, ],

            [{'key': 'id', 'value': 1, 'count': 1},
             {'key': 'success', 'value': True, 'count': 2},
             {'key': 'name', 'value': 'Lary', 'count': 2},
             {'key': 'id', 'value': 2, 'count': 1}, ],
        ]

    def test_simple_case(self):
        self.assertEqual(keys_counter(self.given[0]), self.expected[0])

    def test_empty_list(self):
        self.assertEqual(keys_counter([]), [])

    def test_uniq_dicts(self):
        self.assertEqual(keys_counter(self.given[1]), self.expected[1])

    def test_same_dicts(self):
        self.assertEqual(keys_counter(self.given[2]), self.expected[2])
