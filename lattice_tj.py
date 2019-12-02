"""
Torquato-Jiao (TJ) algorithm for finding sphere packings with high center density
Adapted for lattice packings in the following paper:
https://arxiv.org/pdf/1304.5003.pdf
"""
from core.lll import lll_reduction
from core.norms import euclidean_norm as norm, sum_of_squared_coefficietns
from core.lattice_enumeration import find_vectors_less_than
from simplex_method import simplex_method
from core.matrix import Matrix
from core.polynomial import Polynomial
import numpy as np


def lattice_tj(m):
    """
    input start matrix, m, that represents a basis for a lattice sphere packing
    returns lattice packing with a density that is a local maximum
    """
    # perform LLL on the matrix
    b = lll_reduction(m, 0.75)
    D = norm(m[0])
    R_i = D * 1.1
    # 1. Fin all non-zero lattices between D and R_i
    epsilon = []  # identity??
    threshold = 1e-12  # possibly make bigger for algorithm to run faster in lower dimensions
    while sum_of_squared_coefficietns(epsilon) > threshold:
        shortest_vectors = find_vectors_less_than(b, R_i)
        constraints = make_constraints(shortest_vectors, D, R_i)
        simplex_input = make_simplex_input(epsilon, constraints)
        simplex_output = simplex_method(simplex_input)
        # epsilon = process_simplex_output(simplex_output)
        # alternatively, use numpy "linprog(method='simplex')"
        # https://docs.scipy.org/doc/scipy/reference/optimize.linprog-simplex.html

        # b = epsilon*b  #### with special multiplication

    return m + epsilon * m  # here the multiplication means each value of m gets multiplied by counterpart in epsilon


def make_simplex_input(epsilon, constraints):
    """
    we need to multiply the constraints by negative one because
    "simplex_method" is standardized to "<=" vectors instead of ">=" vectors

    output matrix:
    constraints         [constraint vars ][ Identity matrix  ][constants ]
    .                   .                   .                   .
    .                   .                   .                   .
    .                   .                   .                   .

    objective function  [obj func vars  ][                  ][          ]

    objective function is the negative* trace of epsilon.
    *negative because we are going to minimize the trace and "simplex_method" maximizes

    example:
    epsilon =
    [[2, 3]
     [2, 3]]
    objective function: -2 + -3 <= 0  -> [-2, -3, 0]
    constraints:
    4x_0 + 3x_1 <= 7  -> [4, 3, 7]
    -13x_0 <= 2  ->  [-13, 0, 2]
    output matrix:
    [  4, 3, 1, 0, 0, 7]
    [-13, 0, 0, 1, 0, 2]
    [-2, -3, 0, 0, 1, 0]

    The simplex method requires that all variables be >= 0, so there is one more step to account for this
    which is described in the comments below.
    """
    # make the objective function vector
    objective_function = []
    for i in range(len(epsilon)):
        for j in range(len(epsilon[0])):
            if i == j:
                objective_function.append(epsilon[i][j])
            else:
                objective_function.append(0)
    objective_function.append(0)

    # begin to make the output matrix by putting the objective function after the constraints

    output_matrix = Matrix(constraints)
    output_matrix.append(objective_function)
    n = len(epsilon)
    # output_matrix now has length n**2 + 1, where epsilon is n by n

    # The simplex method minimizes cx subject to Ax=b and x >= 0.
    # But here we can have negative x's, so we must modify so that our variables are unrestricted
    # To do this we define x_i := x_2i - x_(2i+1). Then we reconstruct original x_i after simplex

    unresticted = Matrix.zeroes((len(output_matrix), 2*(n**2)+1))
    for i in range(len(output_matrix)):
        for j in range(n**2):
            unresticted[i][2*j] = output_matrix[i][j]
            unresticted[i][2*j+1] = -1*output_matrix[i][j]
    # now add the last column to unrestricted
    for i in range(len(output_matrix)):
        unresticted[i][2*(n**2)] = output_matrix[i][n**2]

    # insert the identity matrix before the constants
    # the size of the identity is the number of constraints plus 1 for the objective function
    id = Matrix.identity(len(constraints)+1)

    last_column = unresticted.column_sub_matrix(2*(n**2)+1, 2*(n**2))
    unresticted = unresticted.column_sub_matrix(2*(n**2)).concatenate(id, axis=1).concatenate(last_column, axis=1)
    return unresticted


def make_constraints(shortest_vectors, D, R_i):
    """
    makes constraints out of the shortest vectors
    as per algorithm specifications
    to be used in simplex method
    """
    n = len(shortest_vectors[0])
    epsilon = np.zeros((n, n)).tolist()
    epsilon = Matrix(epsilon)
    # fill epsilon with variables
    for i in range(len(epsilon)):
        for j in range(len(epsilon[0])):
            epsilon[i][j] = Polynomial('x' + str(n * i + j))

    constraints = []
    # shortest vector constraints
    for vector in shortest_vectors:
        vector = Matrix([vector])
        constraint = vector * epsilon * vector.transpose()
        constraint = make_vector_from_linear_polynomial(constraint[0][0], n)
        v_v_t = vector*vector.transpose()
        v_v_t = v_v_t[0][0]  # chance from Matrix type to just a number
        constraint.append(D**2 - v_v_t)
        constraints.append(constraint)
    # example [1, 2, 3, 2, 4, 6, 3, 6, 9, -5]
    # meaning x_0 + 2x_1 + 3x_2 + 2x_3 + 4x_4 + 5x_5 + 3x_6 + 6x_7 + 9x_8 >= -5

    lam = (1 - (D/R_i)**2)/2  # lambda
    # bound lowest eigenvalue of epsilon from below by -lamda
    # -.5*lam <= diagonal element of epsilon
    # -.5*lam/(d-1) <= off-diagonal element of epsilon
    # off-diagonal element of epsilon <= .5*lam(d-1)
    # making this all into form 'element of epsilon >= #':
    #
    # diagonal element of epsilon >= -.5*lam
    # off-diagonal element of epsilon >= -.5*lam/(d-1)
    # -off-diagonal element of epsilon >= -.5*lam(d-1)

    for i in range(n):
        for j in range(n):
            if i == j:  # if diagonal element of epsilon
                # diagonal element of epsilon >= -.5*lam
                constraint = []
                for variable in range(n**2):
                    constraint.append(0)
                constraint[i*n + j] = 1
                constraint.append(-.5*lam)
                constraints.append(constraint)
            else:  # if off-diagonal element of epsilon
                # off-diagonal element of epsilon >= -.5*lam/(d-1)
                # -off-diagonal element of epsilon >= -.5*lam(d-1)
                constraint_positive = []
                constraint_negative = []
                for variable in range(n**2):
                    constraint_positive.append(0)
                    constraint_negative.append(0)
                constraint_positive[i*n + j] = 1
                constraint_negative[i * n + j] = -1
                constraint_positive.append(-.5*lam/(D-1))
                constraint_negative.append(-.5 * lam / (D - 1))
                constraints.append(constraint_positive)
                constraints.append(constraint_negative)

    return constraints


def make_vector_from_linear_polynomial(poly, n):
    """
    input poly, Polynomial
    n, length of vector
    2x_1 + 3x_2 + x_3 + 8x_4, 4  ->  [2, 3, 1, 8]
    5x_2 + 3x_4, 5 ->  [0, 0, 0, 3, 0]
    """
    # initialize res to be all zero's
    res = []
    for i in range(n ** 2):
        res.append(0)

    # add non-linear terms to make sure all variables are present
    for i in range(n ** 2):
        poly += Polynomial('x' + str(i) + '^2')

    for term in poly.term_matrix[1:]:
        for variable in range(1, n ** 2 + 1):
            if term[variable] == 1:
                res[variable - 1] = term[0]
                break
    return res


if __name__ == '__main__':
    shortest_vectors = [[0, 1, 0], [0, -1, 0]]
    n = len(shortest_vectors[0])
    # for p in make_constraints(shortest_vectors):
    #     print(p[0][0].term_matrix)
    constraints = make_constraints(shortest_vectors, 3, 3.3)
    for c in constraints:
        print(c)

    e = Matrix.identity(3)
    si = make_simplex_input(e, constraints)
    print(si)
    sim_out = simplex_method(np.array(si))
    print(sim_out)
    # print(Matrix(sim_out.tolist()))

    # A = Matrix(constraints[2:])
    # print(A)
    # b = A.column_sub_matrix(len(A[0]), len(A[0])-1)
    # A = A.column_sub_matrix(len(A[0])-1)
    # A = np.array(A)
    # b = np.array(b)
    # c = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    # c = np.array(c)
    # from scipy.optimize import linprog
    # output = linprog(c, A, b, method='simplex')
    # print(output)
