# Trust region of f at x_k using a quadratic model:
# model_k(p) = f(x_k) + p*f.grad(x) + .5*p*B_k*p
# B_k = f.hessian(x_k)

from core.polynomial import *
from core.matrix import *


def make_quadratic_model(f, x, p):
    """
    p is vector of variables, e.g. (p1, p2)
    x is a vector point, e.g. (1, 2)
    f is a Polynomial
    """
    p = [Polynomial(variable) for variable in p]
    b = f.hessian(*x)
    model = f(*x) + vector_times_vector(p, f.grad(*x)) + \
            vector_times_vector(vector_times_matrix(constant_times_vector(.5, p), b), p)
    return model


def make_full_step_p(f, x):
    """
    unconstrained minimum of the quadratic model
    p = -B_k^(-1)*f.grad(x)
    """
    inverse_b = get_matrix_inverse(f.hessian(*x))
    negative_grad = constant_times_vector(-1, f.grad(*x))
    p = matrix_times_vector(inverse_b, negative_grad)
    return tuple(map(float, p))


def make_steepest_descent_direction(f, x):
    """
    unconstrained minimum of the quadratic model along the steepest descent direction
    """
    b = f.hessian(*x)
    f_grad = f.grad(*x)
    numerator = vector_times_vector(constant_times_vector(-1, f_grad), f_grad)
    denominator = vector_times_vector(vector_times_matrix(f_grad, b), f_grad)
    p = constant_times_vector(numerator / denominator, f_grad)
    return tuple(map(float, p))


def trust_region_subproblem(f, x, delta):
    """
    Dogleg method
    1. calculate full step, p_fs
    2. if full step is within trust region, return full step
    3. calculate steepest descent step, p_u
    4. if steepest descent step is outside trust region,
        return p_u such that ||t*p_u||^2 = delta^2, t in [0, 1]
        t = delta / norm(p)
    5. else return point that solves ||p_u + (t-1)(p_fs - p_u)||^2 = delta^2 for t in interval [1, 2]
    """
    p_fs = make_full_step_p(f, x)
    norm = euclidean_norm
    if norm(p_fs) <= delta:
        step = p_fs
        # print('2. step = ', step)
        return vector_plus_vector(x, step)
    p_u = make_steepest_descent_direction(f, x)
    if norm(p_u) > delta:
        step = constant_times_vector(delta / norm(p_u), p_u)
        # print('4. step = ', step)
        return vector_plus_vector(x, step)
    p_fs_minus_p_u = vector_plus_vector(p_fs, constant_times_vector(-1, p_u))
    quadratic_equation = norm_squared(
        vector_plus_vector(p_u, constant_times_vector(Polynomial('t'), p_fs_minus_p_u))) - delta ** 2
    t_minus_one = max(quadratic_equation.solve())
    step = vector_plus_vector(p_u, constant_times_vector(t_minus_one, p_fs_minus_p_u))
    # print('5. step = ', step)
    return vector_plus_vector(x, step)


def euclidean_norm(vector):
    return (sum([component ** 2 for component in vector])) ** .5


def norm_squared(vector):
    res = 0
    for component in vector:
        res += component ** 2
    return res


def main():
    p = ('p1', 'p2')
    f = Polynomial('10(x2-x1^2)^2+(1-x1)^2')
    x = (0, -1)
    delta = 2
    print(make_quadratic_model(f, x, p))

    # print(trust_region_subproblem(f, x, delta))

    def polynomial_to_numpy(polynomial, *variables):
        """
        input polynomial, a Polynomial class
        and variables, numpy variables
        converts Polynomial class to a numpy function
        """
        z = 0
        # for each term add consant*variable[0]^power[0]*variable[1]^power[1]...
        for term in polynomial.term_matrix[1:]:
            product = term[0]
            for i, variable in enumerate(variables):
                product *= variable ** term[i + 1]
            z += product
        return z

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    x_scale = .5
    y_scale = 1.25
    x1 = np.linspace(-x_scale, x_scale, 100)
    x2 = np.linspace(-y_scale, y_scale, 100)
    x1, x2 = np.meshgrid(x1, x2)
    z = polynomial_to_numpy(f, x1, x2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cpf = ax.contourf(x1, x2, z, 20, cmap='RdGy')
    # Set the colours of the contours and labels so they're white where the
    # contour fill is dark (Z < 0) and black where it's light (Z >= 0)
    colours = ['w' if level < 0 else 'k' for level in cpf.levels]
    cp = ax.contour(x1, x2, z, 20, colors=colours)
    ax.clabel(cp, fontsize=10, colors=colours)
    ax.set_title('Quadratic Model Contour Lines')
    plot_points = [x]
    for i in range(1, 15):
        new_delta = delta / i
        plot_points.append(trust_region_subproblem(f, x, new_delta))
    for point in plot_points:
        print(point)
    xs = [x[0] for x in plot_points]
    ys = [x[1] for x in plot_points]
    plt.scatter(xs, ys)
    plt.show()


if __name__ == '__main__':
    main()
