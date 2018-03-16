from array import array
import reprlib
import numbers
from functools import reduce



def normalize(elements):
    """Make each list in elements of equal length

    """
    maxlen = len(max(elements, key=len))
    for elem in elements:
        elem.extend([0] * (maxlen - len(elem)))

    return elements


def flatten(elements):
    """Flattens list of lists into 1-d list

    """
    flattened = list()

    for el in elements:
        flattened.extend(el)

    return flattened


class Matrix:
    """

    """
    def __init__(self, elements):
        self._elements = [array('f', row)
                          for row in normalize(elements)]
        self._rows = len(self._elements)
        self._columns = len(self._elements[0])

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    def __repr__(self):
        matrix_format = "{}\n" * self._rows
        row_format = " {:>5} " * self._columns
        matrix_rows = list()
        for row in self._elements:
            r = row_format.format(*row.tolist())
            matrix_rows.append(r)

        return matrix_format.format(*matrix_rows)

    def __len__(self):
        return self.rows * self.columns

    def __iter__(self):
        return iter(self._elements)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._elements[index])
        elif isinstance(index, numbers.Integral):
            return self._elements[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return len(self) == len(other) and self._elements == other._elements
        else:
            return False

    def __add__(self, other):
        # Matrix + Numeric
        if isinstance(other, numbers.Rational):
            result = [[i + other for i in el] for el in self._elements]
            return Matrix(result)
        # Matrix + Matrix
        elif isinstance(other, type(self)):
            if self.columns == other.columns and self.rows == other.rows:
                pairs = list(zip(flatten(self._elements), flatten(other._elements)))
                result = [[a + b for a, b in pairs[i:i+self.rows]]
                          for i in range(0, len(self), self.rows)]
                return Matrix(result)
            else:
                raise TypeError
        else:
            raise TypeError

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        self._elements = (self + other)._elements
        return self

    def __mul__(self, other):
        # Matrix * Numeric
        if isinstance(other, numbers.Rational):
            result = [[i * other for i in el] for el in self._elements]
            return Matrix(result)
        else:
            raise TypeError

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self._elements = (self * other)._elements
        return self

    def __matmul__(self, other):
        # Matrix * Matrix
        if isinstance(other, type(self)) and (self.columns == other.rows):
            other_temp = other.transpose()
            return Matrix([[reduce(
                lambda x, y: x + y,
                [a * b for a, b in zip(
                    self._elements[r1],
                    other_temp._elements[r2])])
                for r2 in range(other_temp.rows)]
                for r1 in range(self.rows)])
        else:
            raise TypeError

    def __imatmul__(self, other):
        self._elements = (self @ other)._elements
        return self

    def __sub__(self, other):
        return self + (-1) * other

    def __rsub__(self, other):
        return self - other

    def __isub__(self, other):
        self._elements = (self - other)._elements
        return self

    def __pow__(self, power, modulo=None):
        # Matrix ** Numeric
        if isinstance(power, numbers.Rational):
            result = [[i ** power for i in el] for el in self._elements]
            return Matrix(result)
        else:
            raise TypeError

    def __ipow__(self, other):
        self._elements = (self ** other)._elements
        return self

    def __invert__(self):
        pass

    def is_square_matrix(self):
        return self.rows == self.columns

    def transpose(self):
        cls = type(self)
        transposed = [flatten(self._elements)[i::self.columns]
                      for i in range(self.columns)]

        return cls(transposed)

    @classmethod
    def zero(cls, rows, columns):
        s = [[0 for i in range(columns)] for j in range(rows)]
        return cls(s)

    @classmethod
    def even(cls, rows):
        s = [[1 if i == j else 0 for i in range(rows)] for j in range(rows)]
        return cls(s)

if __name__ == '__main__':
    m = Matrix([[1,2], [4,5]])
    m2 = Matrix([[2,3], [1,4]])
    # print(m)
    # print(m.is_square_matrix())
    # m2 = Matrix.zero(3, 10)
    # print(m2)
    # print(m2.is_square_matrix())
    # m3 = Matrix.even(10)
    # print(m3)
    # print(m3.is_square_matrix())
    # print(m[0])
    # print(m.transpose())
    # print(m + m.transpose())
    # print(1 + m)
    # m += 1
    print(m)
    # print(id(m))
    # m += 1
    # print(m)
    # print(id(m))
    print(m2)
    print(m2 * m)

