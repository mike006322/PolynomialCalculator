import pytest

from polynomials.polynomial import Polynomial
from polynomials.collect_like_terms import collect_like_terms
import polynomials.orderings as ord


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


def _synthetic_term_matrix(n_terms: int, n_vars: int):
    # Header: variable names as x1, x2, ...
    header = [" "] + [f"x{i+1}" for i in range(n_vars)]
    data = []
    for i in range(n_terms):
        coef = (i * 13) % 7 + 1
        exps = [((i + j * 3) % 5) for j in range(n_vars)]
        data.append([coef] + exps)
    return [header] + data


@pytest.mark.parametrize("n_terms,n_vars", [(200, 1), (200, 3), (1000, 3)])
def test_collect_like_terms_benchmark(benchmark, n_terms, n_vars):
    tm = _synthetic_term_matrix(n_terms, n_vars)

    def do_collect():
        return collect_like_terms(tm, preserve_header=True)

    res = benchmark(do_collect)
    assert isinstance(res, list)
    assert len(res) > 0


@pytest.mark.parametrize("n_terms,n_vars", [(200, 1), (200, 3), (1000, 3)])
def test_orderings_grevl_benchmark(benchmark, n_terms, n_vars):
    tm = _synthetic_term_matrix(n_terms, n_vars)

    def do_order():
        return ord.grev_lex(tm)

    res = benchmark(do_order)
    assert isinstance(res, list)
