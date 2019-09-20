from core.polynomial import *
from matrix.matrix_operations import *


def euclidean_norm(vector):
    return (sum([component**2 for component in vector]))**.5


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


def line_search_steepest_descent(f, initial_point):
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
        print('f(*x) = ', f(*x))
        print('norm(f.grad(*x)) = ', norm(f.grad(*x)))
    return x


def line_search_newtons_algorithm(f, initial_point):
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
        print('f(*x) = ', f(*x))
        print('norm(f.grad(*x)) = ', norm(f.grad(*x)))
    return x


def backtracking_algorithm(f, x_k, p):
    """
    Backtracking Algorithm to find step lengths alpha
    """
    alpha = 1
    rho = .5
    c = 10**(-4)
    # while f(x_k + alpha*p) > f(x_k) + c*alpha*p_transpose*f.grad(x_k):
    while f(*vector_plus_vector(x_k, constant_times_vector(alpha, p))) > f(*x_k) + c*alpha*vector_times_vector(p, f.grad(*x_k)):
        # print('alpha = ', alpha)
        alpha = rho*alpha
    return alpha
    

# TODO: Steepest descent + Wolfe conditions will give globally convergent method
# Also true for Newton's method if Hessian is positive definite and condition number is uniformly bounded

# Wolfe conditions is inherent in backtracking line search

# we know the following for nice enough f: 
# if we ensure p_k is not perpendicular to grad(x_k), i.e. cos(theta_k) >= delta > 0
# compute cos(theta_k) in each iteration, and turn p_k in the steepest descent direction if
# needed (cos(theta_k) < delta)
# and alpha_k statisfies the wolve conditions
# then we have a globally convergent algorithm

# we can perform angle tests (|cos(theta_k)| > delta) and subsequently "turn" p_k to ensure global convergence
# however, this will slow down convergence rate
# they brak quasi newton methors which are important for large problems


if __name__ == '__main__':
    # rosenbrock_function = Polynomial('100(x2 − x1^2)^2 + (1-x_1)^2')
    # rosenbrock_function = Polynomial('100x2^2 - 200x1^2x2 + 100x1^4 + 1-2x1 + x1^2')
    # print(line_search_newtons_algorithm(rosenbrock_function, (-1.2, 1)))
    # print(line_search_steepest_descent(rosenbrock_function, (-1.2, 1)))
    M = [[1, 1], [1, 2]]
    print(matrix_times_vector(M, [Polynomial('x1'), Polynomial('x2')]))
