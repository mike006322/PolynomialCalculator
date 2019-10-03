from core.polynomial import *
from matrix.matrix_operations import *


def euclidean_norm(vector):
    return (sum([component**2 for component in vector]))**.5


def line_search(f, initial_point, descent_direction_function):
    """
    Input polynomial f, initial point, descent direction p, and descent direction function.
    Minimizes the polynomial.
    Returns iterations that stop at the local minimum.
    x_(k+1) = x_k + alpha_k*p_k
    """
    iterations = []
    x = initial_point
    norm = euclidean_norm
    while abs(f(*x)) > 10**(-8) and norm(f.grad(*x)) > 10**(-8):
        p = descent_direction_function(f, x)  # Newton's or Steepest Descent
        alpha = backtracking_algorithm(f, x, p)
        iterations.append('x_k: ' + str(x) + ', f(x_k): ' + str(f(*x)) + ', p: ' +
                          str(p) + ', alpha_k: ' + str(alpha))
        # x = x + alpha*p
        x = vector_plus_vector(x, constant_times_vector(alpha, p))
    return iterations


def steepest_descent(f, x):
    """
    input polynomial f, tuple x representing point
    returns the direction vector, p, of steepest descent
    p = -f.grad(x)/euclidean_norm(f.grad(x))
    Using steepest descent the linesearch will converge to local minimum but at linear speed (slow)
    """
    p = f.grad(*x)
    norm = euclidean_norm
    denominator = -1*norm(p)
    for i in range(len(p)):
        p[i] /= denominator
    return p


def newtons_algorithm(f, x):
    """
    Input polynomial f and tuple x representing point.
    Returns the direction vector, p, of steepest descent
    p = -f.hessian(x)^(-1) * f.grad(x)
    Using Newton's algorithm the linesearch might not converge but it runs at quadratic speed (fast)
    """
    inverse_hessian = get_matrix_inverse(f.hessian(*x))
    p = matrix_times_vector(inverse_hessian, f.grad(*x))
    p = constant_times_vector(-1, p)
    return p


def backtracking_algorithm(f, x_k, p):
    """
    Backtracking Algorithm to find step lengths alpha
    """
    alpha = 1
    rho = .5
    c = 10**(-4)
    # while f(x_k + alpha*p) > f(x_k) + c*alpha*p_transpose*f.grad(x_k):
    while f(*vector_plus_vector(x_k, constant_times_vector(alpha, p))) > f(*x_k) + c*alpha*vector_times_vector(p, f.grad(*x_k)):
        alpha = rho*alpha
    return alpha


def find_step_length(phi):
    """
    iterates to find an appropriate step length
    returns alpha_star
    """
# Set alpha_0 = 0, choose alpha_1 > 0, alpha_max, c_1, and c_2, i = 1
# while True:
#   Compute phi(alpha_i)
#   if ( phi(alpha_i) > phi(0) + c_1*alpha_i*phi'(0) ) or (phi(alpha_i) >= phi(alpha_(i-1)) and i > 1):
#       alpha_star = zoom(alpha_(i-1), alpha_i)
#       break # return alpha_star?
#   Compute phi'(alpha_i)
#   if |phi'(alpha_i)| <= -c_2phi'(0):
#       alpha_star = alpha_i
#       break
#   if phi'(alpha_i) >= 0:
#       alpha_star = zoom(alpha_i, alpha_(i-1))
#       break
#   Choose αi+1 ∈ [alpha_i, alpha_max]
#   i += 1


def zoom(phi, alpha_low, alpha_high):
    """
    :param phi:
    :return:
    """
    pass
# while True:
#   Interpolate to find alpha_j between alpha_low and alpha_high
#   Compute phi(alpha_j)
#   if ( phi(alpha_j) > phi(0) + c_1*alpha_j*phi′(0) ) or (phi(alpha_j) >= phi(alpha_low) ):
#       alpha_high = alpha_j
#   else:
#       Compute phi'(alpha_j)
#       if |phi'(alpha_j)| <= -c_2*phi'(0):
#           alpha_star = alpha_j
#           return alpha_star
#       if phi'(alpha_j)*(alpha_high - alpha_low) >= 0:
#           alpha_high = alpha_low
#       alpha_low = alpha_j


def print_results(iterations):
    print('Number of iterations: ', len(iterations))
    if len(iterations) > 20:
        for line in iterations[0:11]:
            print(line)
        print('  .')
        print('  .')
        print('  .')
        for line in iterations[-10:]:
            print(line)
    else:
        for line in iterations:
            print(line)


def main():
    f = Polynomial('(x1+x2^2)^2')
    iterations = line_search(f, (1, 1), steepest_descent)

    # rosenbrock_function = Polynomial('100(x2-x1^2)^2 + (1-x1)^2')
    # iterations = line_search(rosenbrock_function, (1.2, 1.2), newtons_algorithm)
    # iterations = line_search(rosenbrock_function, (1.2, 1.2), steepest_descent)
    print_results(iterations)


if __name__ == '__main__':
    main()
