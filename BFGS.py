"""
Broyden-Fletcher-Goldfarb-Shanno (BFGS)Quasi-Newton  Optimization
This optimization algorithm that doesn't require calculating the Hessian
Cost per iteration: O(n^2)
Convergence rate:  super linear
"""

from core.polynomial import Polynomial
from core.vector import Vector
from core.matrix import *
from core.norms import euclidean_norm as norm
from linesearch import backtracking_algorithm, line_search, newtons_algorithm, find_step_length


def bfgs(f, x_0, e):
    """
    inputs: function f, initial point x_0, convergence tolerance e
    output minimum of f local to x
    """
    k = 0
    x_k = x_0
    identity = Matrix.identity(len(f.grad))
    h = identity

    while norm(f.grad(*x_k)) > e:
        # print('norm: ', norm(f.grad(*x_k)))
        # print('x: ', x_k)
        # print('abs(f(*x_k)): ', abs(f(*x_k)))
        p = Vector(matrix_times_vector(-h, f.grad(*x_k)))
        # print('p: ', p)
        alpha = backtracking_algorithm(f, x_k, p)  # k = 132
        # alpha = find_step_length(f, x_k, p) # k = 106
        # print('alpha ', alpha)
        x_k_1 = x_k + alpha * p
        # if x_k_1 == x_k:
        #     break
        s = x_k_1 - x_k
        y = Vector(f.grad(*x_k_1)) - Vector(f.grad(*x_k))
        rho = 1 / (y * s)
        s, y = Matrix([s]), Matrix([y])
        h = (identity - (rho * (s.transpose() * y))) * h * (identity - (rho * (y.transpose() * s))) + (
                    rho * (s.transpose() * s))
        k += 1

        x_k = x_k_1
        # print('x_k = ', x_k)
        # print('k = ', k)
    return x_k


def h_descent_direction_function(h):
    """
    returns a function: p(f, x) = -h * f.grad(*x)
    """

    def p(f, x):
        # have p be a vector, not a matrix
        print(f.grad(*x))
        res = []
        for term in -h * Matrix([f.grad(*x)]).transpose():
            res.append(float(*term))
        return res

    return p


def rosenbrock_function(dimension):
    x = dict()
    for i in range(dimension):
        x[i] = Polynomial('x' + str(i))
    res = Polynomial(0)
    for i in range(dimension - 1):
        res += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
    return res


def main():
    dimension = 6
    f = rosenbrock_function(dimension)

    e = 10e-6
    x = Vector(1.2, 1.2, 1.1, 1.1, 1.05, 1.05, 1.025, 1.025, -1.2, 1.0, -0.1, 1.0, 0.45, 1.0, 0.725, 1.0, -2.4, 2.0)
    x = Vector(x[0:dimension])
    m = bfgs(f, x, e)
    print(m)


def test_rosenbrock():
    f = rosenbrock_function(2)
    assert f == Polynomial('100x0^4 - 200x0^2x1 + x0^2 - 2x0 + 100x1^2 + 1')


def newtons():
    dimension = 7
    f = rosenbrock_function(dimension)
    x = Vector(1.2, 1.2, 1.1, 1.1, 1.05, 1.05, 1.025, 1.025, -1.2, 1.0, -0.1, 1.0, 0.45, 1.0, 0.725, 1.0, -2.4, 2.0)
    x = Vector(x[0:dimension])
    m = line_search(f, x, newtons_algorithm)
    print(m)


if __name__ == '__main__':
    main()
    # test_rosenbrock()
    # newtons()
