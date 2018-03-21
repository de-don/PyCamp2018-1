from unittest import TestCase
from .data_reader import Data


class DataReaderTest(TestCase):

    def test_read_csv(self):
        d = Data().get_csv('table.csv')
        print(d)



