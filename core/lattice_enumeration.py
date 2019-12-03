"""
Finds all non-zero vectors in a lattice that are shorter than a given distance from the origin.
If argument for distance is empty then finds the shortest vector precisely (i.e. non-approximation like LLL).
"""

import numpy as np
from core.norms import euclidean_norm as norm
import math
from core.gram_schmidt_numpy import gram_schmidt
import scipy
from core.lll import lll_reduction


def floor_ceil(number):
    if number >= 0:
        return math.floor(number)
    else:
        return math.ceil(number)


class Node:

    def __init__(self, vector, level, lam):
        self.vector = vector
        self.level = level
        self.lam = lam  # lambda

    def __repr__(self):
        return str(self.vector)


# def find_vectors_less_than(basis, R=None):
#     """
#     Given a basis for a lattice, finds all vectors shorter than specified distance.
#     This algorithm executes much faster if the basis is reduced
#     https://eprint.iacr.org/2012/533.pdf pages 19-22
#     """
#     b, u = gram_schmidt(basis)  # b = orthogonalized basis, u = gram schmidt coefficients
#     print('orthogonal b: \n', b)
#     print('coefficients u \n', u)
#     if not R:
#         distance_of_shortest_vector = norm(basis[0])
#         R = distance_of_shortest_vector
#     short_vectors = list()
#     # proceed down the tree using non-recursive depth first search
#     search_stack = list()
#     bound = math.floor(R / norm(basis[-1]))
#     for i in range(-1 * bound, bound + 1):
#         search_stack.append(Node(i * b[-1], len(b) - 1, 1))
#     while search_stack:
#         print('search stack: ', search_stack)
#         c = search_stack.pop()  # current node
#         print('current node: ', c)
#         level = c.level - 1
#         print('current level = ', level)
#         bound = math.floor(R / norm(basis[level]))
#         print('bound: ', bound)
#         for i in range(-1 * bound, bound + 1):
#             lam = -1 * floor_ceil(u[level][level - 1]) + i
#             vector = c.vector + (c.lam * u[level][level - 1] + lam) * b[level - 1]
#             print('new vector to stack?: ', vector, ' level: ', level)
#             if norm(vector) <= R:
#                 print('yes, short vector')
#                 short_vectors.append(vector)
#                 if level > 0:
#                     search_stack.append(Node(vector, level, lam))
#
#     return short_vectors


def find_vectors_less_than(b, c):
    """
    b input matrix, lattice basis where the COLUMNS are basis vectors
    c = upper bound on length of lattices

    Murray R. Bremner
    "Lattice Basis Reduction: An Introduction to the LLL Algorithm and Its Applications"
    page 163 (MAPLE code)
    """

    c = c ** 2
    N, M = b.shape
    G = b.transpose() @ b
    u = G.copy()

    for j in range(M - 1):
        for i in range(j + 1, M):
            # U = RowOperation( U, [i,j], -U[i,j]/U[j,j] )
            # row_i = row_i + (-U[i,j]/U[j,j])* row_j
            factor = -u[i][j] / u[j][j]
            for k in range(len(u[i])):
                u[i][k] += factor * u[j][k]

    dd = np.zeros((M, M))
    for i in range(N):
        dd[i][i] = u[i][i]
    u = np.linalg.inv(dd) @ u
    result_old = [[]]
    for k in reversed(range(M)):
        result_new = []
        # print('len(result_old), ', len(result_old))
        i = 0
        for r in result_old:

            xvalue = []
            counter = 0
            while counter <= k:
                xvalue.append(0)
                counter += 1
            xvalue += r

            s = sum(dd[i][i] * sum(u[i][j] * xvalue[j] for j in range(i, M)) ** 2 for i in range(k + 1, M))
            t = sum(u[k][j] * xvalue[j] for j in range(k + 1, M))

            lower_bound = math.ceil(-1 * np.sqrt((c - s) / dd[k][k]) - t)
            upper_bound = math.floor(np.sqrt((c - s) / dd[k][k]) - t)
            for x in range(lower_bound, upper_bound + 1):
                xr = [x] + r
                mm = 0
                for m in range(len(xr)):
                    if xr[m] != 0:
                        mm = m
                if mm == 0:
                    ok = True
                else:
                    ok = (xr[mm] > 0)
                if ok:
                    result_new = result_new + [xr]
            i += 1
        result_old = result_new
    res = []
    for x in result_new:
        x = np.array(x)
        res.append(b.dot(x))
    return res

def fincke_pohst_with_lll_preprocessing(B, C):
    """
    inputs: basis B, upper bound C
    output:  All vectors of squared length ≤ C in the lattice L spanned by the columns of B.

    Murray R. Bremner
    "Lattice Basis Reduction: An Introduction to the LLL Algorithm and Its Applications"
    page 174
    """
    m = len(B[0])
    n = len(B)
    Q = B.transpose() @ B
    for j in range(m-1):
        for i in range(j+1, m):
            # add -Q_ij/Q_jj(Q[j]) to Q[i]
            Q[i] += (-1*Q[i][j]/Q[j][j])*Q[j]
    D = np.zeros((m, m))
    for i in range(m):
        D[i][i] = Q[i][i]
    U = np.linalg.inv(D) @ Q
    # R = D**.5 @ U
    D_1_2 = scipy.linalg.sqrtm(D)
    R = D_1_2 @ U
    R_inverse = np.linalg.inv(R)
    S_inverse = lll_reduction(R_inverse.tolist())
    # Sort the rows of S−1 by decreasing norm to obtain P^−1S^−1
    P_1S_1 = sorted(S_inverse, key=norm, reverse=True)
    # S = RX
    # P = (P^-1)^-1
    # SP = S @ P
    # H = SP.transpose() @ SP
    # Q = H




def test():
    t = [[0, 1, 0],
         [1, 0, 1],
         [-1, 0, 2]]
    t = np.array(t).transpose()
    short_vectors = find_vectors_less_than(t, 1)
    for i in range(len(short_vectors)):
        print(short_vectors[i])


if __name__ == '__main__':
    test()
