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


if __name__ == '__main__':
    pass
