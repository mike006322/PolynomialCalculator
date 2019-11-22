def euclidean_norm(vector):
    return (sum([component ** 2 for component in vector])) ** .5


def weighted_frobenius_norm(matrix):
    return (sum([sum([abs(a) ** 2 for a in row]) for row in matrix])) ** .5


if __name__ == '__main__':
    pass
