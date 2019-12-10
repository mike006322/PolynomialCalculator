"""
Torquato-Jiao (TJ) algorithm for finding sphere packings with high center density
Adapted for lattice packings in the following paper:
https://arxiv.org/pdf/1304.5003.pdf
"""
import logging
from core.lll import lll_reduction
from core.norms import euclidean_norm as norm, sum_of_squared_coefficietns
from core.lattice_enumeration import find_vectors_less_than
from simplex_method import *
from core.matrix import Matrix
from core.polynomial import Polynomial
import numpy as np
from core.lattice import Lattice


def removearray(L, arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind], arr):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')


def lattice_tj(m):
    """
    input m, that represents a basis for a lattice sphere packing
    returns lattice packing with a density that is a local maximum
    """
    n = len(m)
    logging.info('Starting lattice_tj for \n' + str(m))
    b = np.array(lll_reduction(m, 0.75))  # perform LLL reduction on the matrix
    logging.debug('b: \n' + str(b))
    D = norm(b[0])  # D is length of shortest vector because b is LLL reduced
    R = D * 2
    epsilon = Matrix.identity(n)
    threshold = 1e-12
    while sum_of_squared_coefficietns(epsilon) > threshold:
        det_b = np.linalg.det(b)
        logging.info('Finding shortest vectors.')
        logging.debug('max length of vectors: ' + str(R))
        # print(b)
        logging.info('Finding shortst vectors.')
        shortest_vectors = find_vectors_less_than(b.transpose(), R)
        removearray(shortest_vectors, np.zeros(len(b)))
        logging.debug('shortest_vectors = ' + str(shortest_vectors))
        constraints = make_constraints(shortest_vectors, D, R, n)
        logging.debug('constraints: \n' + str(Matrix(constraints)))
        simplex_input = make_simplex_input(epsilon, constraints)
        simplex_input = np.array(simplex_input)
        # simplex_input[-1] *= -1
        # logging.debug('simplex input \n' + str(simplex_input))
        logging.info('Performing Simplex Method.')
        epsilon = simplex_method_scipy(simplex_input, unrestricted=True)
        epsilon = np.array(epsilon).reshape((len(b), len(b)))
        logging.debug('epsilon: ' + str(epsilon))
        logging.debug('trace of epsilon (objective function) ' + str(np.trace(epsilon)))
        logging.info('sum_of_squared_coefficients(epsilon): ' + str(sum_of_squared_coefficietns(epsilon)))
        updated_b = b + epsilon @ b
        logging.debug('updated b: ' + str(updated_b))
        logging.debug('det of b: ' + str(det_b))
        updated_det = np.linalg.det(updated_b)
        if det_b > 0:
            if updated_det > det_b:
                logging.debug('Updated determinant large. Halving epsilon')
                epsilon *= .5
                updated_b = b + epsilon @ b
                logging.debug('updated determinant ' + str(updated_det))
                updated_det = np.linalg.det(updated_b)
        else:
            if updated_det < det_b:
                logging.debug('Updated determinant large. Halving epsilon')
                epsilon *= .5
                updated_b = b + epsilon @ b
                logging.debug('updated determinant ' + str(updated_det))
                updated_det = np.linalg.det(updated_b)
        b = updated_b
        logging.debug('new, denser b = ' + str(b.tolist()))
        print('center density = ' + str(Lattice(b).center_density))

    logging.info('Finished lattice_tj for \n' + str(m))
    return b


def make_constraints(shortest_vectors, D, R_i, n):
    """
    makes constraints out of the shortest vectors
    as per algorithm specifications
    to be used in simplex method
    """
    epsilon = np.zeros((n, n)).tolist()
    epsilon = Matrix(epsilon)
    # fill epsilon with variables
    for i in range(len(epsilon)):
        for j in range(len(epsilon[0])):
            epsilon[i][j] = Polynomial('x' + str(n * i + j))

    constraints = []
    # shortest vector constraints
    if shortest_vectors:
        for vector in shortest_vectors:
            vector = Matrix([vector])
            constraint = -1 * vector * epsilon * vector.transpose()
            constraint = make_vector_from_linear_polynomial(constraint[0][0], n)
            v_v_t = vector * vector.transpose()
            v_v_t = v_v_t[0][0]  # chance from Matrix type to just a number
            constraint.append(-1 * (D ** 2 - v_v_t) / 2)
            constraints.append(constraint)
    # example [1, 2, 3, 2, 4, 6, 3, 6, 9, -5]
    # meaning x_0 + 2x_1 + 3x_2 + 2x_3 + 4x_4 + 5x_5 + 3x_6 + 6x_7 + 9x_8 >= -5

    lam = (1 - (D / R_i) ** 2) / 2  # lambda
    # bound lowest eigenvalue of epsilon from below by -lamda
    # -.5*lam <= diagonal element of epsilon
    # -.5*lam/(d-1) <= off-diagonal element of epsilon
    # off-diagonal element of epsilon <= .5*lam(d-1)
    # making this all into form 'element of epsilon <= #':
    #
    # - diagonal element of epsilon <= .5*lam
    # - off-diagonal element of epsilon <= .5*lam/(d-1)
    # off-diagonal element of epsilon <= .5*lam(d-1)

    for i in range(n):
        for j in range(n):
            if i == j:  # if diagonal element of epsilon
                # - diagonal element of epsilon <= .5*lam
                constraint = []
                for variable in range(n ** 2):
                    constraint.append(0)
                constraint[i * n + j] = -1
                constraint.append(.5 * lam)
                constraints.append(constraint)
            else:  # if off-diagonal element of epsilon
                # -off-diagonal element of epsilon <= .5*lam/(d-1)
                # off-diagonal element of epsilon <= .5*lam(d-1)
                constraint_positive = []
                constraint_negative = []
                for variable in range(n ** 2):
                    constraint_positive.append(0)
                    constraint_negative.append(0)
                constraint_positive[i * n + j] = 1
                constraint_negative[i * n + j] = -1
                constraint_positive.append(.5 * lam / (n - 1))
                constraint_negative.append(.5 * lam / (n - 1))
                constraints.append(constraint_positive)
                constraints.append(constraint_negative)

    return constraints


def make_simplex_input(epsilon, constraints):
    """
    we need to multiply the constraints by negative one because
    "simplex_method" is standardized to "<=" vectors instead of ">=" vectors

    output matrix:
    constraints         [constraint vars ][constants ]
    .                   .                   .
    .                   .                   .
    .                   .                   .

    objective function  [obj func vars  ][          ]

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
    """
    # make the objective function vector
    objective_function = []
    for i in range(len(epsilon)):
        for j in range(len(epsilon[0])):
            if i == j:
                objective_function.append(1)
                # objective_function.append(epsilon[i][j])
            else:
                objective_function.append(0)
    objective_function.append(0)

    # begin to make the output matrix by putting the objective function after the constraints

    output_matrix = Matrix(constraints)
    output_matrix.append(objective_function)
    n = len(epsilon)
    # output_matrix now has length n**2 + 1, where epsilon is n by n
    return output_matrix


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


def main():
    logging.basicConfig(filename='lattice_tj.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s',
                        filemode='w')
    m = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    m = Matrix.identity(3)
    m = [[2, 1, 4], [18, -3, 0], [-3, 1, 6]]

    print(Lattice(m).center_density)

    denser_matrix = lattice_tj(m)
    print('Output: \n', denser_matrix)
    print(Lattice(denser_matrix.tolist()).center_density)

    # m = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    # denser_matrix = lattice_tj(m)
    # print(denser_matrix)
    #
    # differences = []
    # for i in range(10):
    #     b = np.random.rand(3, 3)
    #     while np.linalg.matrix_rank(b) < len(b):
    #         b = np.random.randint(3, 3)
    #     # print(' b: \n', b)
    #     starting_density = Lattice(b.tolist()).center_density
    #     # print('starting density: ', starting_density)
    #     denser_matrix = lattice_tj(b)
    #     ending_density = Lattice(denser_matrix.tolist()).center_density
    #     print('ending density: ', ending_density)
    #     difference = ending_density - starting_density
    #     print('difference = ', difference)
    #     differences.append(difference)
    # print(differences)


def get_density_test():
    m = [[204.9263234521485, -14.19193281871663, -94.11311607854634],
         [-6434.343736245679, 442.14554087457657, 2958.394695219982],
         [-16816.819735412955, 1163.1333278027298, 7724.832669426398]]


    print(Lattice(m).center_density)


if __name__ == '__main__':
    main()
    # get_density_test()
