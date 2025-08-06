from core.number_objects.polynomial import Polynomial, gcd
import random

# Construct a Finite Field/Galois Field of order p^i, GF(p^i)
# Zech logarithm table stores every element of GF(p^i)
# Multiplication in the finite field is converted to integer addition
# need to be able to input element and receive power of primitive element
# need to be able to input power of primitive element and receive polynomial
# therefore need to store hashmaps to accommodate those functions
# https://en.wikipedia.org/wiki/Zech%27s_logarithm


class ZechLogarithmTable:

    def __init__(self, p, i, h=None):
        """
        Multiplication table for GF(p^i)
        Uses or finds an irreducible polynomial over field F_p[x], called h
        then finds the primitive element, beta, of the multiplication group of F_p[x]/h
        then makes a Zech logarithm table populated with powers of the primitive element
        """
        self.field_characteristic = p**i
        if not h:
            self.h = find_irreducible(p, i)
        else:
            self.h = h
        # find primitive element beta
        beta = find_primitive_element(self.h, p, i)
        self.poly_to_power = dict()
        self.power_to_poly = dict()
        beta_j = 1
        for j in range(self.field_characteristic - 1):
            self.poly_to_power[str(beta_j)] = j
            self.power_to_poly[j] = beta_j
            beta_j = (beta_j*beta) % self.h
            j += 1

    def multiply(self, poly1, poly2):
        """
        input two polynomials
        look up their representation as powers of beta, the primitive field element
        return beta to the sum of the powers modulo p^i-1
        """
        i = self.poly_to_power[str(poly1)]
        j = self.poly_to_power[str(poly2)]
        return self.power_to_poly[(i+j) % (self.field_characteristic - 1)]


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


def find_irreducible(p, n):
    """
    returns an irreducible polynomial of degree n over F_q where q is a power of p
    https://math.stackexchange.com/questions/1654562/algorithm-to-find-the-irreducible-polynomial
    """
    # Find irreducible polynomial of degree n in F_q[x]
    # 1. Randomly choose monic f in F_p[x] of degree n
    # 2. For i from 1 to n//2:
    # g_i = gcd(x^(p^i) - x, f)
    # if g_i != 1 then go to 1.
    # return f
    while True:
        f = random_monic(p, n)
        i = 1
        reducible = False
        while i <= n//2:
            g_i = gcd(Polynomial('x', p)**(p**i) - Polynomial('x', p), f)
            # g_i = gcd(x^(p^i) - x, f)
            if g_i != 1:
                if g_i != f:
                    reducible = True
                elif Polynomial('x', p)**(p**i) - Polynomial('x', p) == f:
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
                return 0
            j += 1
        return j

    f = Polynomial('x', p)
    while order(f) != q-1:
        f = Polynomial(0, p)
        a = random.randint(1, i-1)
        for k in range(a):
            f += random.randint(0, p-1)*Polynomial('x')**k
    return f


if __name__ == '__main__':
    pass
