from core.polynomial import *
import random

# Find irreducible polynomial of degree n in F_q[x]
# 1. Randomly choose monic f in F_q[x] of degree n
# 2. For i from 1 to n//2:
# g_i = gcd(x^(q^i) - x, f)
# if g_i != 1 then go to 1.
# return f


def random_monic(p, n):
    """
    returns a random monic polynomial of degree n over field F_q
    """
    x = Polynomial('x', p)
    f = x**n
    m = n - 1
    while m >= 0:
        f += random.randint(0, p-1)*(x**m)
        m -= 1
    return f


def find_irreducible(p, q, n):
    """
    q is a power of prime p
    returns an irreducible polynomial of degree n over F_q
    """
    while True:
        f = random_monic(p, n)
        i = 0
        reducible = False
        while i <= n//2:
            g_i = gcd(Polynomial('x', p)**(q**i) - Polynomial('x', p), f)
            if g_i != 1 and g_i != f:
                reducible = True
            i += 1
        if not reducible:
            return f


if __name__ == '__main__':
    pass
