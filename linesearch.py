from core.polynomial import *
from core.matrix import *


def euclidean_norm(vector):
    return (sum([component ** 2 for component in vector])) ** .5


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
    k = 0
    while abs(f(*x)) > 10 ** (-8) and norm(f.grad(*x)) > 10 ** (-8):
        # print('norm(f.grad(*x)), abs(f(*x)) ', norm(f.grad(*x)), abs(f(*x)))
        p = descent_direction_function(f, x)  # Newton's, Steepest Descent
        # alpha = find_step_length(f, x, p)
        alpha = backtracking_algorithm(f, x, p)
        print('x_' + str(k) + ': ' + str(x) + ', f(x_k): ' + str(float(f(*x))) + ', p: ' +
                          str(p) + ', alpha_k: ' + str(alpha))
        iterations.append('x_k: ' + str(x) + ', f(x_k): ' + str(f(*x)) + ', p: ' +
                          str(p) + ', alpha_k: ' + str(alpha))
        # x = x + alpha*p
        x = vector_plus_vector(x, constant_times_vector(alpha, p))
        k += 1
    return x


def steepest_descent(f, x):
    """
    input polynomial f, tuple x representing point
    returns the direction vector, p, of steepest descent
    p = -f.grad(x)/euclidean_norm(f.grad(x))
    Using steepest descent the linesearch will converge to local minimum but at linear speed (slow)
    """
    p = f.grad(*x)
    norm = euclidean_norm
    denominator = -1 * norm(p)
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
    hess = f.hessian(*x)
    for i in range(len(hess)):
        for j in range(len(hess[0])):
            hess[i][j] = float(hess[i][j])
    inverse_hessian = get_matrix_inverse(hess)
    p = matrix_times_vector(inverse_hessian, f.grad(*x))
    p = constant_times_vector(-1, p)
    return list(map(float, p))


def backtracking_algorithm(f, x_k, p):
    """
    Backtracking Algorithm to find step lengths alpha
    """
    alpha = 1
    rho = .5
    c = 10 ** (-4)
    # while f(x_k + alpha*p) > f(x_k) + c*alpha*p_transpose*f.grad(x_k):
    while abs(f(*vector_plus_vector(x_k, constant_times_vector(alpha, p)))) > \
            abs(f(*x_k) + c * alpha * vector_times_vector(p, f.grad(*x_k))):
        alpha = rho * alpha
    return alpha


def find_step_length(f, x, p):
    """
    iterates to find an appropriate step length
    returns alpha_star
    """
    # phi(alpha) = f(x + alpha*p)
    phi = f(*map(Polynomial.__add__, constant_times_vector(Polynomial('a'), p), x))
    # Set alpha_0 = 0, choose alpha_1 > 0, alpha_max, c_1, and c_2, i = 1
    alpha_0 = 0  # alpha previous, i.e. alpha_(i-1)
    alpha_1 = 1  # alpha current, i.e. alpha_i
    alpha_max = 2
    c_1 = 10 ** -4
    c_2 = 0.9
    i = 0
    phi_prime = phi.derivative()
    while True:
        phi_alpha_1 = phi(alpha_1)
        if (phi_alpha_1 > phi(0) + c_1 * alpha_1 * phi_prime(0)) or (phi(alpha_1) >= phi(alpha_0) and i > 1):
            alpha_star = zoom(phi, alpha_0, alpha_1, c_1, c_2)
            break
        phi_prime_alpha_1 = phi_prime(alpha_1)
        if abs(phi_prime_alpha_1) <= -c_2 * phi_prime(0):
            alpha_star = alpha_1
            break
        if phi_prime_alpha_1 >= 0:
            alpha_star = zoom(phi, alpha_1, alpha_0, c_1, c_2)
            break
        # Choose alpha_1+1 ∈ [alpha_1, alpha_max]
        alpha_0 = alpha_1
        alpha_1 = alpha_1 + (alpha_max - alpha_1) / 2
        i += 1
    return alpha_star


def zoom(phi, alpha_low, alpha_high, c_1, c_2):
    """
    the zoom function arguments alpha_low and alpha_high must satisfy the following conditions:
    1. The interval bounded by alha_low and alpha_high contains step lengths which satisfy the strong Wolfe conditions.
    2. alpha_low is the alpha corresponding to the lower function value, i.e. phi(alpha_low) < phi(alpha_high).
    3. alpha_low and alpha_high satisfy: phi′(alpha_low)*(alpha_high − alpha_low) < 0.
    """
    while True:
        # Interpolate to find alpha_j between alpha_low and alpha_high
        phi_prime = phi.derivative()
        alpha_j = interpolate(phi, alpha_low, alpha_high)
        phi_alpha_j = phi(alpha_j)
        if (phi_alpha_j > phi(0) + (c_1 * alpha_j * phi_prime(0))) or (phi_alpha_j >= phi(alpha_low)):
            alpha_high = alpha_j
        else:
            phi_prime_alpha_j = phi_prime(alpha_j)
            if abs(phi_prime_alpha_j) <= -c_2 * phi_prime(0):
                alpha_star = alpha_j
                return alpha_star
            if phi_prime_alpha_j * (alpha_high - alpha_low) >= 0:
                alpha_high = alpha_low
            alpha_low = alpha_j


def interpolate(phi, alpha_left, alpha_right):
    """
    H_3 is the cubic interpolation of phi
    return alpha in interval [alpha_(k-1), alpha_k] such that H_3(alpha) is minimal.
    [alpha_(k-1), alpha_k] = [alpha_left, alpha_right]
    alpha is either such that H_3'(alpha) = 0, or and endpoint H_3(alpha_(k-1)) or H_3(alpha_k)
    """
    phi_prime = phi.derivative()
    def H_3(a):
        return (1 + (a - alpha_left)/(alpha_right - alpha_left))*((a - alpha_right)/(alpha_right - alpha_left))**2*phi(alpha_left) +\
        (1 + 2*(alpha_right - a)/(alpha_right - alpha_left))*((a - alpha_left)/(alpha_right-alpha_left))**2*phi(alpha_right) +\
        (a - alpha_left)*((alpha_right - a)/(alpha_right - alpha_left))**2*phi_prime(alpha_left) +\
        (a - alpha_right)*((a - alpha_left)/(alpha_right - alpha_left))**2*phi_prime(alpha_right)
    # e_1 = .1
    # e_2 = .5
    # if abs(alpha_left - alpha_right) < e_1 or alpha_right < e_2:
    #     alpha_right = alpha_left/2
    d_1 = phi_prime(alpha_left) + phi_prime(alpha_right) - (3 * (phi(alpha_left) - phi(alpha_right)) / (
            alpha_left - alpha_right))
    d_2 = sign(alpha_right - alpha_left) * (d_1 ** 2 - phi_prime(alpha_left) * phi_prime(alpha_right)) ** .5
    denominator = phi_prime(alpha_right) - phi_prime(alpha_left) + 2 * d_2
    interior_point = alpha_right - (alpha_right - alpha_left) * (phi_prime(alpha_right) + d_2 - d_1) / denominator
    if H_3(interior_point) < H_3(alpha_left):
        if H_3(interior_point) < H_3(alpha_right):
            return interior_point
        else: 
            return alpha_right
    else:
        if H_3(alpha_left) < H_3(alpha_right):
            return alpha_left
        else:
            return alpha_right
    

def sign(number):
    if number >= 0:
        return 1
    else:
        return -1


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
    # iterations = line_search(f, (1, 1), steepest_descent)

    rosenbrock_function = Polynomial('100(x2-x1^2)^2 + (1-x1)^2')
    # 100.0x1^4 - 200.0x1^2x2 + x1^2 - 2.0x1 + 100.0x2^2 + 1.0
    print(rosenbrock_function)
    min = line_search(rosenbrock_function, (-1, 1.2), newtons_algorithm)
    print(min)
    # iterations = line_search(rosenbrock_function, (-1, 1.2), newtons_algorithm)
    # iterations = line_search(rosenbrock_function, (1.2, 1.2), steepest_descent)
    # print_results(iterations)


if __name__ == '__main__':
    main()
