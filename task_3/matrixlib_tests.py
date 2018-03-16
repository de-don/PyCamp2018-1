from unittest import TestCase
from .matrixlib import Matrix
from array import array


class MatrixTester(TestCase):
    def setUp(self):
        self.normal_data = [[1,2,3],[2,3,4],[3,4,5]]
        self.normal_matrix = Matrix([[1,2,3],[2,3,4],[3,4,5]])
        self.not_normal = [[1], [1, 2], [1, 2, 3]]
        self.not_normal_matrix = Matrix([[1], [1, 2], [1, 2, 3]])
        self.matrices = [
            Matrix([[1, 1], [1, 1]]),  # 0
            Matrix([[2, 2], [2, 2]]),  # 1
            Matrix([[1, 1], [1]]),  # 2
            Matrix([[2, 2], [2, 1]]),  # 3
            Matrix([[2, 2], [2]]),  # 4
            Matrix([[0, 0], [0, 0]]),  # 5
            Matrix([[0, 0, 0], [0, 0, 0]]),  # 6
            Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),  # 7
            Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),  # 8
            Matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]]),  # 9
            Matrix([[1, 2], [4, 5], [7, 8]]),  # 10
            Matrix([[1, 4, 7], [2, 5, 8]]),  # 11
            Matrix([[2, 3], [1, 4]]),  # 12
            Matrix([[1, 2], [4, 5]]),  # 13
            Matrix([[14, 19], [17, 22]]),  # 14

        ]

    def test_elements_of_matrix(self):
        for i in range(len(self.normal_data)):
            self.assertEqual(
                self.normal_matrix[i],
                array('f', self.normal_data[i])
            )
        # check normalizing
        for i in range(len(self.not_normal) - 1):
            self.assertNotEqual(
                self.not_normal_matrix[i],
                array('f', self.not_normal[i])
            )
        # check type of each element is float
        for row in self.normal_matrix:
            for col in row:
                self.assertEqual(type(col), float)

    def test_matrices_equality(self):
        self.assertEqual(self.matrices[0], Matrix([[1, 1], [1, 1]]))
        self.assertEqual(Matrix([[1, 1], [1, 1]]), self.matrices[0])
        self.assertNotEqual(self.matrices[0], self.matrices[1])
        self.assertNotEqual(self.matrices[0], [[1, 1], [1, 1]])

    def test_matrix_plus_number(self):
        self.assertEqual(self.matrices[0] + 1, self.matrices[1])
        self.assertEqual(self.matrices[2] + 1, self.matrices[3])
        self.assertEqual(1 + self.matrices[0], self.matrices[1])
        self.assertEqual(1 + self.matrices[0], self.matrices[0] + 1)
        with self.assertRaises(TypeError):
            self.matrices[0] + [[1, 1], [1, 1]]

    def test_matrix_plus_matrix(self):
        self.assertEqual(self.matrices[0] + self.matrices[0], self.matrices[1])
        self.assertEqual(self.matrices[0] + self.matrices[2], self.matrices[3])
        self.assertEqual(self.matrices[2] + self.matrices[0], self.matrices[3])
        self.assertEqual(
            self.matrices[2] + self.matrices[0],
            self.matrices[0] + self.matrices[2]
        )

    def test_matrix_mul_number(self):
        self.assertEqual(self.matrices[0] * 2, self.matrices[1])
        self.assertEqual(2 * self.matrices[0], self.matrices[0] * 2)
        with self.assertRaises(TypeError):
            self.matrices[0] * [[1, 1], [1, 1]]

    def test_creating_zero_matrix(self):
        self.assertEqual(Matrix.zero(2, 2), self.matrices[5])
        self.assertEqual(Matrix.zero(2, 3), self.matrices[6])
        self.assertNotEqual(Matrix.zero(3, 3), self.matrices[6])

    def test_creating_even_matrix(self):
        self.assertEqual(self.matrices[7], Matrix.even(3))
        self.assertTrue(Matrix.even(3).is_square_matrix())

    def test_matrix_transpose(self):
        self.assertEqual(self.matrices[0], self.matrices[0].transpose())
        self.assertEqual(self.matrices[9], self.matrices[8].transpose())
        self.assertEqual(self.matrices[10], self.matrices[11].transpose())
        self.assertEqual(self.matrices[10], self.matrices[10].transpose().transpose())

    def test_matrix_power(self):
        self.assertEqual(self.matrices[0] ** 4, self.matrices[0])
        self.assertEqual((self.matrices[0] * 2) ** 2, self.matrices[1] * 2)

    def test_matrix_mul_matrix(self):
        self.assertEqual(self.matrices[12] @ self.matrices[13], self.matrices[14])
        self.assertNotEqual(
            self.matrices[12] @ self.matrices[13],
            self.matrices[13] @ self.matrices[12]
        )
        with self.assertRaises(TypeError):
            self.matrices[12] @ 1

    def test_i_operations_not_change_id(self):
        check = Matrix([[1, 1], [1, 1]])
        id0 = id(check)
        check += 1
        id_check = id(check)
        self.assertEqual(id0, id_check)
        check -= 4
        id_check = id(check)
        self.assertEqual(id0, id_check)
        check += Matrix([[1, 1], [1, 1]])
        id_check = id(check)
        self.assertEqual(id0, id_check)
        check *= 3
        id_check = id(check)
        self.assertEqual(id0, id_check)
        check **= 3
        id_check = id(check)
        self.assertEqual(id0, id_check)
        check @= Matrix([[3, 3], [3, 3]])
        id_check = id(check)
        self.assertEqual(id0, id_check)







