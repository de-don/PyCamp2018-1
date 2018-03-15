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
        return len(self._elements)

    def __add__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __iadd__(self, other):
        pass


    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __imul__(self, other):
        pass


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
        pass


    def is_square_matrix(self):
        return len(self._elements) == len(self._elements[0])

    def transpose(self):
        cls = type(self)

        for_transpose = array('f')
        for r in self._elements:
            for_transpose.extend(r)

        transposed = [for_transpose[i::self.rows] for i in range(self.columns)]
        # print(transposed)

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
    print(m.is_square_matrix())
    m2 = Matrix.zero(3, 10)
    print(m2)
    print(m2.is_square_matrix())
    m3 = Matrix.even(10)
    print(m3)
    print(m3.is_square_matrix())
    print(m[0])
    print(m.transpose())

