from typing import Tuple

import numpy as np


def gram_schmidt(matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Orthogonalize a set of vectors stored as the rows of matrix
    returns orthogonal basis and gram schmidt coefficients
    """
    ortho = matrix.copy()
    n = ortho.shape[0]
    u = np.zeros(ortho.shape)  # also store gram schmidt coefficients
    for i in range(n):
        # To orthogonalize the vector in column j with respect to the previous vectors,
        # subtract from it its projection onto each of the previous vectors.
        for k in range(i):
            gs_coefficient = np.dot(ortho[:, k], ortho[i, :])
            u[i][k] = gs_coefficient
            ortho[i, :] -= gs_coefficient * ortho[k, :]
        # ortho[i, :] = ortho[i, :] / np.linalg.norm(ortho[i, :])  # This line would make it an orthonormal basis
    return ortho, u


if __name__ == "__main__":
    A = np.array([[1.0, 1.0, 0.0], [1.0, 3.0, 1.0], [2.0, -1.0, 1.0]])
    b, u = gram_schmidt(A)
    print(A)
    print(b)
    print(u)
