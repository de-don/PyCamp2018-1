from unittest import TestCase
from .matrixlib import Matrix
from array import array


class MatrixTester(TestCase):
    def setUp(self):
        self.normal_data = [[1,2,3],[2,3,4],[3,4,5]]
        self.normal_matrix = Matrix([[1,2,3],[2,3,4],[3,4,5]])
        self.not_normal = [[1], [1,2], [1,2, 3]]
        self.not_normal_matrix = Matrix([[1], [1,2], [1,2, 3]])

    def test_elements_of_matrix(self):
        for i in range(len(self.normal_data)):
            self.assertEqual(
                self.normal_matrix[i],
                array('f', self.normal_data[i])
            )
        # check normalizing
        for i in range(len(self.not_normal_matrix) - 1):
            self.assertNotEqual(
                self.not_normal_matrix[i],
                array('f', self.not_normal[i])
            )
        # check type of each element is float
        for row in self.normal_matrix:
            for col in row:
                self.assertEqual(type(col), float)








