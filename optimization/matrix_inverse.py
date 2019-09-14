def transpose_matrix(m):
    return list(map(list, zip(*m)))


def get_matrix_minor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def get_matrix_determinant(m):
    # base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * get_matrix_determinant(get_matrix_minor(m, 0, c))
    return determinant


def get_matrix_inverse(m):
    determinant = get_matrix_determinant(m)
    # special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]

    # find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = get_matrix_minor(m, r, c)
            cofactorRow.append(((-1) ** (r + c)) * get_matrix_determinant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose_matrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return cofactors


if __name__ == '__main__':
    pass
