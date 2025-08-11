import pytest

from polynomials.polynomial import Polynomial, division_algorithm


def _rand_poly(deg: int, var: str = "x") -> Polynomial:
    # Simple deterministic pseudo-random polynomial with integer coefficients
    # Note: Using a fixed sequence to avoid importing numpy
    coeffs = [(i * 37) % 11 - 5 for i in range(deg + 1)]  # values in [-5,5]
    # Ensure leading coefficient non-zero and monic
    if coeffs[-1] == 0:
        coeffs[-1] = 1
    else:
        coeffs[-1] = 1 if coeffs[-1] > 0 else -1
    # Build string representation like "1*x^deg + ... + c"
    terms = []
    for k, c in enumerate(coeffs):
        if c == 0:
            continue
        power = k
        if power == 0:
            terms.append(f"{c}")
        elif power == 1:
            terms.append(f"{c}{var}")
        else:
            terms.append(f"{c}{var}^{power}")
    s = " + ".join(reversed(terms))
    return Polynomial(s)


@pytest.mark.parametrize("deg", [10, 50, 200])
def test_mul_benchmark(benchmark, deg):
    f = _rand_poly(deg)
    g = _rand_poly(deg - 1 if deg > 0 else 1)

    def do_mul():
        return f * g

    res = benchmark(do_mul)
    # Smoke check: result degree should be approx sum of degrees
    assert isinstance(res, Polynomial)
    assert res.degree() >= deg - 1


@pytest.mark.parametrize("deg", [10, 50, 200])
def test_add_benchmark(benchmark, deg):
    f = _rand_poly(deg)
    g = _rand_poly(deg)

    def do_add():
        return f + g

    res = benchmark(do_add)
    assert isinstance(res, Polynomial)


@pytest.mark.parametrize("deg", [10, 50])
def test_division_algorithm_like_benchmark(benchmark, deg):
    # Use simple division by a lower-degree polynomial; indirectly exercises internal normalization
    f = _rand_poly(deg)
    g = _rand_poly(max(1, deg // 2))

    def do_mod():
        return f % g

    res = benchmark(do_mod)
    assert isinstance(res, Polynomial)


# Removed legacy term-matrix based benchmarks (_synthetic_term_matrix, orderings grev_lex, and LT cache via _poly_from_tm) as term matrices are deprecated.


@pytest.mark.parametrize("deg", [50, 200])
def test_add_zero_fastpath_benchmark(benchmark, deg):
    p = _rand_poly(deg)
    z = Polynomial(0)

    def do_add_zero():
        return p + z

    res = benchmark(do_add_zero)
    assert isinstance(res, Polynomial)


@pytest.mark.parametrize("deg", [50, 200])
def test_mul_constant_fastpath_benchmark(benchmark, deg):
    p = _rand_poly(deg)

    def do_mul_const():
        return p * 2

    res = benchmark(do_mul_const)
    assert isinstance(res, Polynomial)


@pytest.mark.parametrize("k,deg", [(5, 50), (10, 50)])
def test_division_multi_divisors_benchmark(benchmark, k, deg):
    # Many divisors increases LT checks; caching their LTs reduces repeated work
    f = _rand_poly(deg)
    divisors = [
        _rand_poly(max(1, (i % max(1, deg // 3)) + 1)) for i in range(k)
    ]

    def do_division():
        qs, r = division_algorithm(f, *divisors)
        return r

    res = benchmark(do_division)
    assert isinstance(res, Polynomial)
