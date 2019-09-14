from core.polynomial import *
from matrix_inverse import *


def euclidean_norm(vector):
    res = 0
    for component in vector:
        res += component**2
    return res**.5


def steepest_descent(f, x):
    """
    input polynomial f, tuple x representing point
    returns the direction vector, p, of steepest descent
    p = -f.grad(x)/euclidean_norm(f.grad(x))
    """
    p = f.grad(*x)
    norm = euclidean_norm
    denominator = -1*norm(p)
    for i in range(len(p)):
        p[i] /= denominator
    return p


def newtons_algorithm(f, x):
    """
    input polynomial f, tuple x representing point
    returns the direction vector, p, of steepest descent
    p = -f.hessian(x)^(-1) * f.grad(x)
    """
    inverse_hessian = get_matrix_inverse(f.hessian(*x))
    p = matrix_times_vector(inverse_hessian, f.grad(*x))
    p = constant_times_vector(-1, p)
    return p


def line_search_with_backtracking_and_steepest_descent(f, initial_point):
    """
    input f: polynomial, p: descent direction, initial point
    minimizes the polynomial
    return a local minimum
    x_(k+1) = x_k + alpha_k*p_k
    """
    x = initial_point
    norm = euclidean_norm
    while abs(f(*x)) > 10**(-8) and norm(f.grad(*x)) > 10**(-8):
        p = steepest_descent(f, x)
        alpha = backtracking_algorithm(f, x, p)
        # x = x + alpha*p
        x = vector_plus_vector(x, constant_times_vector(alpha, p))
        print('x_k = ', x)
        print('norm(f.grad(*x)) = ', norm(f.grad(*x)))
    return x


def line_search_with_backtracking_and_newtons_algorithm(f, initial_point):
    """
    input f: polynomial, p: descent direction, initial point
    minimizes the polynomial
    return a local minimum
    x_(k+1) = x_k + alpha_k*p_k
    """
    x = initial_point
    norm = euclidean_norm
    while abs(f(*x)) > 10**(-8) and norm(f.grad(*x)) > 10**(-8):
        p = newtons_algorithm(f, x)
        alpha = backtracking_algorithm(f, x, p)
        # x = x + alpha*p
        x = vector_plus_vector(x, constant_times_vector(alpha, p))
        print('x_k = ', x)
        print('norm(f.grad(*x)) = ', norm(f.grad(*x)))
    return x


def backtracking_algorithm(f, x_k, p):
    """
    Backtracking Algorithm to find step lengths alpha:
    1.) find a descent direction p_k (Newton's or Steepest descent)
    2.) set alpha bar > 0, 0 < rho < 1, 0 < c < 1, alpha = alpha bar
    3.) While f(x_k + alpha*p_k) > f(x_k) + c*alpha*p_k^T*gradf(x_k):
          alpha = rho*alpha
    4.) set alpha_k = alpha
    """
    alpha = 1
    rho = .5
    c = 10**(-4)
    # while f(x_k + alpha*p) > f(x_k) + c*alpha*p_transpose*f.grad(x_k):
    while f(*vector_plus_vector(x_k, constant_times_vector(alpha, p))) > f(*x_k) + c*alpha*vector_times_vector(p, f.grad(*x_k)):
        # print('alpha = ', alpha)
        alpha = rho*alpha
    return alpha


def vector_plus_vector(v_1, v_2):
    res = []
    for i, component in enumerate(v_1):
        res.append(component + v_2[i])
    return res


def vector_times_vector(v_1, v_2):
    res = 0
    for i, component in enumerate(v_1):
        res += component * v_2[i]
    return res


def constant_times_vector(constant, vector):
    res = []
    for component in vector:
        res.append(constant*component)
    return res


def matrix_times_vector(matrix, vector):
    res = []
    for row in matrix:
        dot_product = 0
        for i, item in enumerate(row):
            dot_product += item * vector[i]
        res.append(dot_product)
    return res


if __name__ == '__main__':
    # rosenbrock_function = Polynomial('100(x2 − x1^2)^2 + (1-x_1)^2')
    rosenbrock_function = Polynomial('100x2^2 - 200x1^2x2 + 100x1^4 + 1-2x1 + x1^2')
    # print(line_search_with_backtracking_and_newtons_algorithm(rosenbrock_function, (-1.2, 1)))
    print(line_search_with_backtracking_and_steepest_descent(rosenbrock_function, (-1.2, 1)))
