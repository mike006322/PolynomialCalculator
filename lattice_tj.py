"""
Torquato-Jiao (TJ) algorithm for finding sphere packings with high center density
Adapted for lattice packings in the following paper:
https://arxiv.org/pdf/1304.5003.pdf
"""
import logging
import time
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
    starting_time = time.time()
    n = len(m)
    logging.info('Starting lattice_tj for \n' + str(m))
    b = np.array(lll_reduction(m, 0.75))  # perform LLL reduction on the matrix
    logging.debug('b: \n' + str(b))
    D = norm(b[0])  # D is length of shortest vector because b is LLL reduced
    R = D * 1.1
    epsilon = Matrix.identity(n)
    threshold = 1e-12
    while sum_of_squared_coefficietns(epsilon) > threshold:
        det_b = np.linalg.det(b)
        logging.info('Finding shortest vectors.')
        logging.debug('max length of vectors: ' + str(R))
        logging.info('Finding shortst vectors.')
        shortest_vectors = find_vectors_less_than(b.transpose(), R)
        removearray(shortest_vectors, np.zeros(len(b)))
        logging.debug('shortest_vectors = ' + str(shortest_vectors))
        constraints = make_constraints(shortest_vectors, D, R, n)
        logging.debug('constraints: \n' + str(Matrix(constraints)))
        simplex_input = make_simplex_input(epsilon, constraints)
        logging.debug('simplex input: \n' + str(simplex_input))
        simplex_input = np.array(simplex_input)
        logging.info('Performing Simplex Method.')
        epsilon_variables = simplex_method_scipy(simplex_input, unrestricted=True)
        epsilon = np.array(make_epsilon(epsilon_variables, n))
        logging.debug('epsilon: ' + str(epsilon))
        logging.debug('trace of epsilon (objective function) ' + str(np.trace(epsilon)))
        logging.info('sum_of_squared_coefficients(epsilon): ' + str(sum_of_squared_coefficietns(epsilon)))
        updated_b = b + b @ epsilon
        logging.debug('updated b: ' + str(updated_b))
        logging.debug('det of b: ' + str(det_b))
        updated_det = np.linalg.det(updated_b)
        # if det_b > 0:
        #     if updated_det > det_b:
        #         logging.debug('Updated determinant large. Halving epsilon')
        #         epsilon *= .5
        #         updated_b = b + epsilon @ b
        #         logging.debug('updated determinant ' + str(updated_det))
        #         updated_det = np.linalg.det(updated_b)
        # else:
        #     if updated_det < det_b:
        #         logging.debug('Updated determinant large. Halving epsilon')
        #         epsilon *= .5
        #         updated_b = b + epsilon @ b
        #         logging.debug('updated determinant ' + str(updated_det))
        #         updated_det = np.linalg.det(updated_b)
        b = updated_b
        logging.debug('new, denser b = ' + str(b.tolist()))
        print('center density = ' + str(Lattice(b).center_density))

    logging.info('Finished lattice_tj for \n' + str(m))
    ending_time = time.time()
    print('time = ' + str(ending_time - starting_time))
    return b


def make_constraints(shortest_vectors, D, R_i, n):
    """
    makes constraints out of the shortest vectors
    as per algorithm specifications
    to be used in simplex method
    """
    epsilon = np.zeros((n, n)).tolist();
    epsilon = Matrix(epsilon)
    variable_numbers = []
    # fill epsilon with variables
    for i in range(len(epsilon)):
        for j in range(len(epsilon[0])):
            if i > j:
                epsilon[i][j] = epsilon[j][i]
            else:
                epsilon[i][j] = Polynomial('x' + str(n * i + j))
                variable_numbers.append((i, j))

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


    for v, variable in enumerate(variable_numbers):
        i, j = variable
        if i == j:  # if diagonal element of epsilon
            # - diagonal element of epsilon <= .5*lam
            constraint = []
            for _ in range(len(variable_numbers)):
                constraint.append(0)
            constraint[v] = -1
            constraint.append(.5 * lam)
            constraints.append(constraint)
        else:  # if off-diagonal element of epsilon
            # -off-diagonal element of epsilon <= .5*lam/(d-1)
            # off-diagonal element of epsilon <= .5*lam(d-1)
            constraint_positive = []
            constraint_negative = []
            for _ in range(len(variable_numbers)):
                constraint_positive.append(0)
                constraint_negative.append(0)
            constraint_positive[v] = 1
            constraint_negative[v] = -1
            constraint_positive.append(.5 * lam / (n - 1))
            constraint_negative.append(.5 * lam / (n - 1))
            constraints.append(constraint_positive)
            constraints.append(constraint_negative)

    # for i in range(n):
    #     for j in range(n):
    #         if i == j:  # if diagonal element of epsilon
    #             # - diagonal element of epsilon <= .5*lam
    #             constraint = []
    #             for variable in range(number_of_variables):
    #                 constraint.append(0)
    #             constraint[i * n + j] = -1
    #             constraint.append(.5 * lam)
    #             constraints.append(constraint)
    #         else:  # if off-diagonal element of epsilon
    #             # -off-diagonal element of epsilon <= .5*lam/(d-1)
    #             # off-diagonal element of epsilon <= .5*lam(d-1)
    #             constraint_positive = []
    #             constraint_negative = []
    #             for variable in range(number_of_variables):
    #                 constraint_positive.append(0)
    #                 constraint_negative.append(0)
    #             constraint_positive[i * n + j] = 1
    #             constraint_negative[i * n + j] = -1
    #             constraint_positive.append(.5 * lam / (n - 1))
    #             constraint_negative.append(.5 * lam / (n - 1))
    #             constraints.append(constraint_positive)
    #             constraints.append(constraint_negative)

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
        for j in range(i, len(epsilon[0])):
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
    number_of_variables = n*(n+1)//2
    # initialize res to be all zero's
    res = []
    for i in range(number_of_variables):
        res.append(0)

    # add non-linear terms to make sure all variables are present
    for i in range(number_of_variables):
        poly += Polynomial('x' + str(i) + '^2')

    for term in poly.term_matrix[1:]:
        for variable in range(1, number_of_variables + 1):
            if term[variable] == 1:
                res[variable - 1] = term[0]
                break
    return res


def make_epsilon(variables, n):
    epsilon = []
    variable_index = 0
    for i in range(n):
        epsilon.append([])
        for j in range(n):
            if i > j:
                epsilon[i].append(epsilon[j][i])


            elif i == j:
                epsilon[i].append(variables[variable_index])
                variable_index += 1
            elif i < j:
                epsilon[i].append(variables[variable_index])
                variable_index += 1
    return epsilon


def main():
    logging.basicConfig(filename='lattice_tj.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s',
                        filemode='w')
    # m = [[1, 1, 1, 3], [-1, 0, 2, 3], [3, 5, 6, 4], [3, -4, -5, 6]]
    m = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    # m = Matrix.identity(3)
    # m = [[2, 1, 4], [18, -3, 0], [-3, 1, 6]]

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
    m = [[-2992.9880115283113, -10.72655918418694, -373.644364082849, -79.76874811239823],
         [1118.502728914449, 5.872511951906576, 139.03821745089388, 31.520105005997586],
         [1183.3611207871302, 2.8580632518764837, 148.10165826317575, 30.42962084140757],
         [2217.808564341084, 8.538061925470647, 276.7082101552752, 59.66740931905222]]
    # actual center density: 0.0593872379809836881793289678657
    # My algorith, said 0.13181955941418586
    # (4, [-2992.9880115283113, -10.72655918418694, -373.644364082849, -79.76874811239823, 1118.502728914449, 5.872511951906576, 139.03821745089388, 31.520105005997586, 1183.3611207871302, 2.8580632518764837, 148.10165826317575, 30.42962084140757, 2217.808564341084, 8.538061925470647, 276.7082101552752, 59.66740931905222]])
    print(Lattice(m).center_density)


if __name__ == '__main__':
    main()
    # get_density_test()
