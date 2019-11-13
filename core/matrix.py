# import numpy as np
from math import gcd
from numbers import *


class Matrix:
    __slots__ = ('_values',)

    def __init__(self, values):
        self._values = values

    def __add__(self, other):
        if type(other) == Matrix:
            assert self.shape == other.shape
            return Matrix(matrix_plus_matrix(self._values, other._values))
        if type(other) == list:
            return Matrix(matrix_plus_matrix(self._values, other))

    def __sub__(self, other):
        return self + -1 * other

    def __mul__(self, other):
        if type(other) == Matrix:
            return Matrix(matrix_times_matrix(self._values, other._values))
        if type(other) == list:
            return Matrix(matrix_times_matrix(self._values, other))
        if type(other) in {int, float, Integer, Rational}:
            return Matrix(scalar_multiplication(other, self._values))

    def __eq__(self, other):
        if type(other) == Matrix:
            if self._values == other._values:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return matrix_to_string(self._values)

    def __repr__(self):
        return matrix_to_string(self._values)

    @property
    def shape(self):
        return len(self._values), len(self._values[0])

    def transpose(self):
        return transpose_matrix(self._values)

    def determinant(self):
        return get_matrix_determinant(self._values)

    def inverse(self):
        return get_matrix_inverse(self._values)

    def null_space(self):
        return get_nullspace(self._values)


def transpose_matrix(m):
    return list(map(list, zip(*m)))


def get_matrix_minor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def get_matrix_determinant(m):
    # base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for j in range(len(m)):
        determinant += ((-1) ** j) * m[0][j] * get_matrix_determinant(get_matrix_minor(m, 0, j))
    return determinant


def get_matrix_inverse(m):
    determinant = get_matrix_determinant(m)
    # special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]

    # find matrix of cofactors
    cofactors = []
    for i in range(len(m)):
        cofactor_row = []
        for j in range(len(m)):
            minor = get_matrix_minor(m, i, j)
            cofactor_row.append(((-1) ** (i + j)) * get_matrix_determinant(minor))
        cofactors.append(cofactor_row)
    cofactors = transpose_matrix(cofactors)
    for i in range(len(cofactors)):
        for j in range(len(cofactors)):
            cofactors[i][j] = cofactors[i][j] / determinant
    return cofactors


def vector_plus_vector(v_1, v_2):
    if type(v_1) == tuple:
        return tuple(map(sum, zip(v_1, v_2)))
    if type(v_1) == list:
        return list(map(sum, zip(v_1, v_2)))


def vector_times_vector(v_1, v_2):
    res = 0
    for i, component in enumerate(v_1):
        res += component * v_2[i]
    return res


def constant_times_vector(constant, vector):
    res = []
    for component in vector:
        res.append(constant * component)
    return res


def scalar_multiplication(constant, matrix):
    res = []
    for i, row in enumerate(matrix):
        res.append([])
        for component in row:
            res[i].append(constant * component)
    return res


def matrix_times_vector(matrix, vector):
    res = []
    for row in matrix:
        dot_product = 0
        for i, item in enumerate(row):
            dot_product += item * vector[i]
        res.append(dot_product)
    return res


def matrix_times_matrix(x, y):
    res = []
    for i in range(len(x)):
        res.append([])
        for j in range(len(y[0])):
            res[i].append(0)
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                res[i][j] += x[i][k] * y[k][j]
    return res


def matrix_plus_matrix(x, y):
    res = []
    for i in range(len(x)):
        res.append([])
        for j in range(len(x[0])):
            res[i].append(x[i][j] + y[i][j])
    return res


def vector_times_matrix(vector, matrix):
    res = []
    for column_number in range(len(matrix[0])):
        dot_product = 0
        for row_number in range(len(matrix)):
            dot_product += matrix[row_number][column_number] * vector[row_number]
        res.append(dot_product)
    return res


def get_nullspace(matrix):
    """
    returns the right nullspace of matrix, a.k.a. kernel
    The left nullspace is simply the nullspace of the transpose of the input
    """
    # get ref
    m = get_integer_ref(matrix)
    # number of paramaters is number of variables that are not on the diagonal, i.e. columns - rows (if full rank)
    # if everything to the left is zeros then that variable is not a paramater
    # make the equations
    diagonal_indices = set()
    running_lcm = 1
    rank = 0
    for j in range(len(m[0])):
        for i in reversed(range(rank, len(m))):
            if m[i][j] != 0:
                diagonal_indices.add(j)
                rank += 1
                running_lcm = lcm(running_lcm, m[i][j])
                break
    m = [x for x in m if any(x)]  # remove zero lines
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] != 0:
                first_non_zero = m[i][j]
                break
        for j in range(len(m[i])):
            m[i][j] *= running_lcm // first_non_zero
    # build the paramater vector
    # go through columns, if they are in the diagonal indices, they are not a parameter
    nullspace_vectors = []
    for r in range(len(m[0]) - rank):
        nullspace_vectors.append([])
    rank = 0
    for j in range(len(m[0])):
        if j not in diagonal_indices:
            for i in range(len(m)):
                nullspace_vectors[j - rank].append(-m[i][j])
        else:
            rank += 1
    vector_number = 0
    for j in range(len(m[0])):
        if j not in diagonal_indices:
            for i, vector in enumerate(nullspace_vectors):
                if i == vector_number:
                    vector.insert(j, running_lcm)
                else:
                    vector.insert(j, 0)
            vector_number += 1
    return transpose_matrix(nullspace_vectors)


# def get_nullspace_numpy(matrix):
#     """
#     returns the right nullspace of matrix, a.k.a. kernel
#     The left nullspace is simply the nullspace of the transpose of the input
#     This function has numpy dependency.
#     """
#     # get ref
#     m = get_integer_ref_numpy(matrix)
#     # number of paramaters is number of variables that are not on the diagonal, i.e. columns - rows (if full rank)
#     # if everything to the left is zeros then that variable is not a paramater
#     # make the equations
#     diagonal_indices = set()
#     running_lcm = 1
#     rank = 0
#     for j in range(len(m[0])):
#         for i in reversed(range(rank, len(m))):
#             if m[i][j] != 0:
#                 diagonal_indices.add(j)
#                 rank += 1
#                 running_lcm = lcm(running_lcm, m[i][j])
#                 break
#     m = m[[i for i, x in enumerate(m) if x.any()]]  # remove zero lines
#     for row in m:
#         for j in range(len(row)):
#             if row[j] != 0:
#                 first_non_zero = row[j]
#                 break
#         row *= running_lcm // first_non_zero
#     # build the paramater vector
#     # go through columns, if they are in the diagonal indices, they are not a parameter
#     nullspace_vectors = []
#     for r in range(len(m[0]) - rank):
#         nullspace_vectors.append([])
#     rank = 0
#     for j in range(len(m[0])):
#         if j not in diagonal_indices:
#             for i in range(len(m)):
#                 nullspace_vectors[j - rank].append(-m[i][j])
#         else:
#             rank += 1
#     vector_number = 0
#     for j in range(len(m[0])):
#         if j not in diagonal_indices:
#             for i, vector in enumerate(nullspace_vectors):
#                 if i == vector_number:
#                     vector.insert(j, running_lcm)
#                 else:
#                     vector.insert(j, 0)
#             vector_number += 1
#     return np.array(nullspace_vectors).transpose()


# def get_left_nullspace_numpy(m):
#     return get_nullspace_numpy(m.transpose()).transpose()


def get_left_nullspace(m):
    return transpose_matrix(get_nullspace(transpose_matrix(m)))


def lcm(a, b):
    return abs(a * b // gcd(int(a), int(b)))


def list_gcd(numbers):
    # initialize g to first non-zero number
    for num in numbers:
        if num != 0:
            g = num
            break
    else:
        return 0
    for a in numbers:
        if a != 0:
            g = gcd(int(g), int(a))
    return g


def get_integer_ref(matrix):
    m = []
    for row in matrix:
        m.append(row.copy())
    number_of_rows = len(m)
    number_of_columns = len(m[0])
    # make the variables on the diagonal all the same number
    for i in range(number_of_rows):
        if i < number_of_columns:
            if m[i][i] == 0:
                # search for row with non-zero entry in that column and add it to that row
                for j in range(i, number_of_rows):
                    if m[j][i] != 0:
                        for e in range(len(m[i])):
                            m[i][e] += m[j][e]
                if m[i][i] == 0:
                    continue
            for j in range(number_of_rows):
                if j == i:
                    continue
                if m[j][i] != 0:
                    lcm_m_i_i_m_j_i = lcm(m[i][i], m[j][i])
                    m_j_i = m[j][i]
                    m_i_i = m[i][i]
                    for e in range(len(m[i])):
                        m[j][e] *= lcm_m_i_i_m_j_i // m_j_i
                    for e in range(len(m[i])):
                        m[j][e] -= m[i][e] * lcm_m_i_i_m_j_i // m_i_i
    # divide by gcd and omit double rows
    for r, row in enumerate(m):
        if any(row):
            row_gcd = list_gcd(row)
            for e in range(len(row)):
                m[r][e] //= row_gcd
    m = sorted(m, key=lambda x: [abs(y) for y in x])
    return list(reversed(m))


# def get_integer_ref_numpy(matrix):
#     m = matrix.copy()
#     number_of_rows = len(m)
#     number_of_columns = len(m[0])
#     # make the variables on the diagonal all the same number
#     for i in range(number_of_rows):
#         if i < number_of_columns:
#             if m[i][i] == 0:
#                 # search for row with non-zero entry in that column and add it to that row
#                 for j in range(i, number_of_rows):
#                     if m[j][i] != 0:
#                         m[i] += m[j]
#                 if m[i][i] == 0:
#                     continue
#             for j in range(number_of_rows):
#                 if j == i:
#                     continue
#                 if m[j][i] != 0:
#                     m[j] *= lcm(m[i][i], m[j][i]) // m[j][i]
#                     m[j] -= m[i] * lcm(m[i][i], m[j][i]) // m[i][i]
#     # divide by gcd and omit double rows
#     for row in m:
#         if any(row):
#             row //= list_gcd(row)
#     m = m[np.lexsort(np.rot90(abs(m)))][::-1]  # lex sort
#     return m


def column_sub_matrix(m, stop, start=0):
    return [x[start: stop] for x in m]


def matrix_to_string(matrix):
    """
    prints a python list in matrix formatting
    """
    s = [[str(int(e)) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table) + '\n'


# def test_get_integer_ref_numpy():
#     m = np.array([[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]])
#     assert get_integer_ref_numpy(m).tolist() == [[1, -2, 0, -1, 3], [0, 0, 1, 2, -2], [0, 0, 0, 0, 0]]
#     m = m.transpose()
#     int_ref = get_integer_ref_numpy(m)
#     assert int_ref.tolist() == [[-5, 0, -1], [0, 5, 13], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


if __name__ == '__main__':
    pass
