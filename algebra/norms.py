from typing import Sequence, Union

Number = Union[int, float, complex]
Vector = Sequence[Number]
Matrix = Sequence[Sequence[Number]]


def euclidean_norm(vector: Vector) -> float:
    return (sum([component**2 for component in vector])) ** 0.5


def weighted_frobenius_norm(matrix: Matrix) -> float:
    return (sum([sum([abs(a) ** 2 for a in row]) for row in matrix])) ** 0.5


def sum_of_squared_coefficietns(matrix: Matrix) -> Number:
    return sum([sum([a**2 for a in row]) for row in matrix])


if __name__ == "__main__":
    pass
