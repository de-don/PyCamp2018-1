from array import array
import reprlib
import numbers



def normalize(elements):
    """Make each list in elements of equal length

    """
    maxlen = len(max(elements, key=len))
    for elem in elements:
        elem.extend([0] * (maxlen - len(elem)))

    return elements


def flatten(elements):
    """Flattens list of lists into 1-d list"""
    flattened = list()

    for el in elements:
        flattened.extend(el)

    return flattened


class Matrix:
    """"""
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
        self + other


    def __mul__(self, other):
        # Matrix * Numeric
        if isinstance(other, numbers.Rational):
            result = [[i * other for i in el] for el in self._elements]
            return Matrix(result)
        # Matrix * Matrix
        # elif isinstance(other, type(self)):
            # if self.columns == other.columns and self.rows == other.rows:

            # else:
                # raise TypeError

        else:
            raise TypeError

    def __rmul__(self, other):
        self * other

    def __sub__(self, other):
        return self + (-1) * other

    def __rsub__(self, other):
        return self - other


    def __matmul__(self, other):
        pass

    def __rmatmul__(self, other):
        pass

    def __imatmul__(self, other):
        pass


    def __invert__(self):
        pass


    def __pow__(self):
        pass

    def __eq__(self, other):
        return self._elements == other._elements


    def is_square_matrix(self):
        return len(self._elements) == len(self._elements[0])

    def transpose(self):
        cls = type(self)

        transposed = [flatten(self._elements)[i::self.rows]
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
    m = Matrix([[1,2], [4,5, 5], [8]])
    print(m)
    # print(m.is_square_matrix())
    # m2 = Matrix.zero(3, 10)
    # print(m2)
    # print(m2.is_square_matrix())
    # m3 = Matrix.even(10)
    # print(m3)
    # print(m3.is_square_matrix())
    # print(m[0])
    print(m.transpose())
    print(m + m.transpose())
    print(m - 1)
    m += 1
    print(m)

