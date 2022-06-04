# LLL basis reduction
# Solves shortest vector problem by returning a basis such that the first vector is closest vector to the origin

from core.log_util import log
from number_objects.primitives.matrix import *


@log
def lll_reduction(basis, delta):
    n = len(basis)
    basis = list(map(Vector, basis))
    orthogonal = gram_schmidt(basis)

    def mu(i: int, j: int) -> Rational:
        return orthogonal[j].proj_coeff(basis[i])

    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            mu_kj = mu(k, j)
            if abs(mu_kj) > 0.5:
                basis[k] = basis[k] - basis[j] * round(mu_kj)
                orthogonal = gram_schmidt(basis)
        if orthogonal[k].sdot() >= (delta - mu(k, k - 1) ** 2) * orthogonal[k - 1].sdot():
            k += 1
        else:
            basis[k], basis[k - 1] = basis[k - 1], basis[k]
            orthogonal = gram_schmidt(basis)
            k = max(k - 1, 1)
    return basis


if __name__ == '__main__':
    pass
