from typing import Sequence, List

Number = float  # Internally coerced to float in implementation
Vector = Sequence[Number]
Matrix = Sequence[Sequence[Number]]

def lll_reduction(basis: Matrix, delta: float = 0.75) -> List[List[Number]]:
    import numpy as np
    B = [np.array(list(map(float, v))) for v in basis]
    n = len(B)
    k = 1
    while k < n:
        # Gram-Schmidt
        B_star = []
        mu = np.zeros((n, n))
        for i in range(n):
            b_star = B[i].copy()
            for j in range(i):
                mu[i, j] = np.dot(B[i], B_star[j]) / np.dot(B_star[j], B_star[j])
                b_star -= mu[i, j] * B_star[j]
            B_star.append(b_star)
        # Size reduction
        for j in range(k-1, -1, -1):
            q = round(mu[k, j])
            if q != 0:
                B[k] -= q * B[j]
        # Recompute Gram-Schmidt for Lovász
        B_star = []
        mu = np.zeros((n, n))
        for i in range(n):
            b_star = B[i].copy()
            for j in range(i):
                mu[i, j] = np.dot(B[i], B_star[j]) / np.dot(B_star[j], B_star[j])
                b_star -= mu[i, j] * B_star[j]
            B_star.append(b_star)
        # Lovász condition
        if np.dot(B_star[k], B_star[k]) >= (delta - mu[k, k-1]**2) * np.dot(B_star[k-1], B_star[k-1]):
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            k = max(k-1, 1)
    return [list(map(float, v)) for v in B]