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
        determinant += ((-1)**j) * m[0][j] * get_matrix_determinant(get_matrix_minor(m, 0, j))
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
            cofactor_row.append(((-1)**(i + j)) * get_matrix_determinant(minor))
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
        res.append(constant*component)
    return res


def matrix_times_vector(matrix, vector):
    res = []
    for row in matrix:
        dot_product = 0
        for i, item in enumerate(row):
            dot_product += item * vector[i]
        res.append(dot_product)
    return res


if __name__ == '__main__':
    pass
