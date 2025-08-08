import pytest

from polynomials.primitives.polycalc_numbers import Integer, Rational


@pytest.mark.parametrize("base", [2, 7, 13])
@pytest.mark.parametrize("exp", [0, 1, 2, 5])
def test_integer_pow_small_exponents_benchmark(benchmark, base, exp):
    a = Integer(base)

    def run():
        return a ** exp

    benchmark(run)


@pytest.mark.parametrize("num,den", [(3, 5), (7, 11)])
@pytest.mark.parametrize("scalar", [0, 1, -1, 2])
def test_rational_mul_scalar_fastpath_benchmark(benchmark, num, den, scalar):
    r = Rational(num, den)

    def run():
        return r * scalar

    benchmark(run)


@pytest.mark.parametrize("num,den", [(3, 5), (7, 11)])
@pytest.mark.parametrize("scalar", [1, -1])
def test_rational_div_scalar_fastpath_benchmark(benchmark, num, den, scalar):
    r = Rational(num, den)

    def run():
        return r / scalar

    benchmark(run)


@pytest.mark.parametrize("num,den", [(5, 5), (9, 9)])
def test_rational_mul_identity_benchmark(benchmark, num, den):
    r = Rational(7, 11)
    s = Rational(num, den)

    def run():
        return r * s

    benchmark(run)


@pytest.mark.parametrize("num,den", [(5, 5), (9, 9)])
def test_rational_div_identity_benchmark(benchmark, num, den):
    r = Rational(7, 11)
    s = Rational(num, den)

    def run():
        return r / s

    benchmark(run)
