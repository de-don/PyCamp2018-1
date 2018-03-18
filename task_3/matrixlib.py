from array import array
from numbers import Integral, Real
from functools import reduce
from collections import Iterable



def normalize(elements):
    """Make each list in elements of equal length

    """
    maxlen = len(max(elements, key=len))
    for elem in elements:
        elem.extend([0] * (maxlen - len(elem)))

    return elements


def flatten(elements):
    """Flattens list of lists into 1-d list.

    Each list has the same size with others.

    """
    flattened = list()

    for el in elements:
        flattened.extend(el)

    return flattened


class Matrix:
    """

    """
    def __init__(self, elements):
        # Matrix can be created only for iterable of numbers
        # and iterable of iterable of numbers
        # E.g. list of floats or list of array of ints
        if isinstance(elements, Iterable):
            iterator = iter(elements)
            # check if elements are numbers
            if all(isinstance(rest, Real)
                   for rest in iterator):
                self._elements = [array('f', elements)]
            # che if all elements are iterable
            elif all(isinstance(rest, Iterable)
                     for rest in iterator):
                self._elements = [array('f', row)
                                  for row in normalize(elements)]
            else:
                raise TypeError('All elements of data must be numbers or iterables')
        else:
            raise TypeError('Data must be iterable')

        self._rows = len(self._elements)
        self._columns = len(self._elements[0])

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def size(self):
        return self.rows, self.columns

    def __len__(self):
        return self.rows * self.columns

    # ----------------------------------------------------------
    # Work with elements of matrix
    # ----------------------------------------------------------

    def _split_indices(self, indices):
        """Private method to process indices of matrix

        Args:
            indices(Tuple[slice]): pair of slices or ints.

        Returns:
            1) slice: first slice or None
            2) slice: second slice or None
        """
        if isinstance(indices, tuple):
            if len(indices) == 1:
                return indices[0], None
            elif len(indices) == 2:
                return indices
            else:
                raise TypeError("Matrix indices consists of two elements")
        elif isinstance(indices, slice) or isinstance(indices, Integral):
            return indices, None
        else:
            raise TypeError("Matrix indices must be in, slice or tuple of them")

    def __getitem__(self, index):
        # Get indices of rows in columns.
        r, c = self._split_indices(index)

        temp_data = list()

        # selecting rows of matrix
        if r:
            if isinstance(r, Integral) or isinstance(r, slice):
                temp_data = list(self)

        # selecting columns of matrix
        if c:
            if isinstance(r, Integral) or isinstance(r, slice):
                temp_data = [row[c] for row in temp_data]

        # create matrix from selected data
        res_matrix = Matrix(temp_data)

        # if res_matrix is 1 x 1, return numeric value
        if res_matrix.size == (1, 1):
            return res_matrix._elements[0][0]

        if res_matrix.rows or res_matrix.columns == 0:
            return None

        return res_matrix

    def __setitem__(self, key, value):
        # Get indices of rows in columns.
        r, c = self._split_indices(key)

        # set single element of matrix
        if isinstance(value, Integral) and isinstance(r, Integral) and isinstance(c, Integral):
            self._elements[r][c] = value
        # set single row of matrix
        elif isinstance(value, Integral) and isinstance(r, Integral) and c is None:
            row = array('f', value)
            # check compatibility of rows length
            if len(row) == self.columns:
                self._elements[r] = len(row)
            else:
                raise IndexError('Wrong length of inserted row. '
                                 'Must be less or equal to matrix row length')
        else:
            raise TypeError('Only single value or single row can be inserted')

    # def __str__(self):
        # pass

    def __repr__(self):
        matrix_format = "{}\n" * self._rows
        row_format = " {:>5} " * self._columns
        matrix_rows = list()
        for row in self._elements:
            r = row_format.format(*row.tolist())
            matrix_rows.append(r)

        return matrix_format.format(*matrix_rows)

    def __iter__(self):
        return iter(self._elements)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return len(self) == len(other) and self._elements == other._elements
        else:
            return False

    def __add__(self, other):
        # Matrix + Numeric
        if isinstance(other, Real):
            result = [[i + other for i in el] for el in self._elements]
            return Matrix(result)
        # Matrix + Matrix
        elif isinstance(other, type(self)):
            # matrices must be of same size
            if self.columns == other.columns and self.rows == other.rows:
                pairs = list(zip(flatten(self._elements), flatten(other._elements)))
                result = [[a + b for a, b in pairs[i:i+self.rows]]
                          for i in range(0, len(self), self.rows)]
                return Matrix(result)
            else:
                raise IndexError
        else:
            raise TypeError

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        self._elements = (self + other)._elements
        return self

    def __mul__(self, other):
        # Matrix * Numeric
        if isinstance(other, Real):
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

    # def __rsub__(self, other):
    #     return self - other

    def __isub__(self, other):
        self._elements = (self - other)._elements
        return self

    def __pow__(self, power, modulo=None):
        # Matrix ** Numeric
        # works only for square matrices
        if isinstance(power, Integral) and (self.rows == self.columns):
            # Returns even matrix if power is 0
            if power == 0:
                return Matrix.even(self.rows)
            elif power == 1:
                return self
            elif power > 1:
                base_val = self
                for i in range(power - 1):
                    base_val @= self
                return base_val
            else:
                raise TypeError
        else:
            raise TypeError

    def __ipow__(self, other):
        self._elements = (self ** other)._elements
        return self

    # def __invert__(self):
        # pass

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
    print(list(Matrix([[1, 2], [2, 3]])))

