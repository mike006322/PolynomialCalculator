from core.polynomial import *
import random

# Construct a Finite Field/Galois Field of order p^i, GF(p^i)
# Zech logarithm table stores every element of GF(p^i)
# Multiplication in the finite field is converted to integer addition
# need to be able to input element and receive power of primitive element
# need to be able to input power of primitive element and receive polynomial
# therefore need to store hashmaps to accommodate those functions
# https://en.wikipedia.org/wiki/Zech%27s_logarithm


class ZechLogarithmTable:

    def __init__(self, p, i):
        """
        Multiplication table for GF(p^i)
        finds an irreducible polynomial over field F_p[x], called h
        then finds the primitive element, beta, of the multiplication group of F_p[x]/h
        then makes a Zech logarithm table populated with powers of the primitive element
        """
        self.field_characteristic = p**i
        h = find_irreducible(p, self.field_characteristic, 2)
        # find primitive element beta
        # start with polynomial of small degree and work upwards checking if the order is p**i - 1
        poly_to_power = dict()
        power_to_poly = dict()
        for j in range(self.field_characteristic - 1):
            pass


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
    # Find irreducible polynomial of degree n in F_q[x]
    # 1. Randomly choose monic f in F_q[x] of degree n
    # 2. For i from 1 to n//2:
    # g_i = gcd(x^(q^i) - x, f)
    # if g_i != 1 then go to 1.
    # return f
    while True:
        f = random_monic(p, n)
        # print('f = ', f)
        i = 1
        reducible = False
        while i <= n//2:
            g_i = gcd(Polynomial('x', p)**(q**i) - Polynomial('x', p), f)
            # print(g_i)
            # g_i = gcd(x^(q^i) - x, f)
            if g_i != 1 and g_i != f:
                reducible = True
                break
            i += 1
        if not reducible:
            return f


def find_primitive_element(h, p, i):
    """
    input irreducible polynomial h over field with characteristic q
    output element of F_q[x] that generates the multiplication group of F_q[x]/h
    """
    # related: https://arxiv.org/pdf/1304.1206v4.pdf
    # https://www.sciencedirect.com/science/article/pii/S1071579705000456
    q = p**i
    # print('h = ', h)

    def order(b):
        if b == 0:
            return 0
        b = b.copy()
        b_j = b.copy()
        j = 1
        while b_j != 1:
            b_j *= b
            b_j %= h
            if b_j == 0:
                # print('order = 0')
                return 0
            # print(b_j)
            j += 1
        # print('order = ', j)
        return j

    f = Polynomial('x', p)
    while order(f) != q-1:
        f = Polynomial(0, p)
        a = random.randint(1, i-1)
        for k in range(a):
            f += random.randint(0, p-1)*Polynomial('x')**k
        # print('f = ', f)
    return f


if __name__ == '__main__':
    pass
