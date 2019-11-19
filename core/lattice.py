from core.matrix import Matrix
from core.lll import lll_reduction
from core.norms import euclidean_norm


class Lattice:

    def __init__(self, matrix):
        self.matrix = Matrix(matrix)

    @property
    def center_density(self):
        b = Matrix(lll_reduction(self.matrix, .75))  # LLL basis reduction
        r = euclidean_norm(b[0]) / 2  # radius
        d = len(self.matrix[0])  # dimension
        det = ((b * b.transpose()).determinant()) ** .5
        return r ** d / det


if __name__ == '__main__':
    pass
