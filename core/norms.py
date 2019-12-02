def euclidean_norm(vector):
    return (sum([component ** 2 for component in vector])) ** .5


def weighted_frobenius_norm(matrix):
    return (sum([sum([abs(a) ** 2 for a in row]) for row in matrix])) ** .5


def sum_of_squared_coefficietns(matrix):
    return sum([sum([a ** 2 for a in row]) for row in matrix])


if __name__ == '__main__':
    pass
