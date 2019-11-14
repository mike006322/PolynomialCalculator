# Conjugate Gradient Optimization
# Iterative method of solving systems of system of linear equations, Ax = b
# Rate of convergence is tied to the distribution of the eigenvalues of A
# If A is dense, running time is O(n^2). If A is sparse, running time is O(n).


def matrix_euclidean_norm(m):
    """
    euclidean norm of a single-column matrix, i.e. a vector
    """
    res = 0
    for i in range(len(m)):
        res += m[i][0]**2
    return res**.5


def conjugate_gradient(A, b, x):
    norm = matrix_euclidean_norm
    r = A * x - b
    p = -r
    r_k_r_k = float(r.transpose() * r)
    k = 0  # number of iterations
    residuals = []
    while norm(r) > 1e-6:
        Ap = A * p
        alpha = r_k_r_k / float(p.transpose() * Ap)
        x = x + alpha * p
        r = r + alpha * Ap
        r_k1_r_k1 = float(r.transpose() * r)
        beta = r_k1_r_k1 / r_k_r_k
        r_k_r_k = r_k1_r_k1
        p = -r + beta * p
        k += 1
        residuals.append(norm(r))
    return x, residuals, k


if __name__ == '__main__':
    pass
