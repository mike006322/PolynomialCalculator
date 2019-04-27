# This module defines number classes so that numbers can be manipulated and presented symbolically


class Integer:
    """
    Integer class represents members of ring of integers, Z
    division of integers that don't share common divisors yields a Rational number
    """

    def __init__(self, i):
        self.value = int(i)

    def __int__(self):
        return self.value

    def __eq__(self, other):
        if type(other) == Integer or type(other) == Rational:
            if self.value == other.value:
                return True
            else:
                return False
        else:
            if int(self) == other:
                return True
            else:
                return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        if type(other) == int:
            return Integer(self.value*other)
        elif type(other) == Rational:
            return Rational(self)+other
        else:
            return Integer(self.value + other.value)

    def __sub__(self, other):
        return Integer(self.value - other.value)

    def __neg__(self):
        return Integer(-self.value)

    def __mul__(self, other):
        if type(other) == int:
            return Integer(self.value*other)
        else:
            return Integer(self.value*other.value)

    def __rmul__(self, other):
        return Integer(self)*Integer(other)

    def __pow__(self, power, modulo=None):
        return Integer(self.value**(int(power)))

    def __mod__(self, other):
        if type(other) == Integer:
            return Integer(self.value % other.value)
        else:
            return self % Integer(other)

    def __floordiv__(self, other):
        return Integer(self.value // other.value)

    def __truediv__(self, other):
        if type(other) == Integer:
            if self.value % other.value == 0:
                return self//other
            else:
                return Rational(self, other)
        else:
            return self / Integer(other)


class Rational:
    """
    Rational class represents members of field of rational numbers, Q
    """

    def __init__(self, a, b=None):
        if type(a) == str:
            if '/' in a:
                self.numerator = Integer(int(a[:a.find('/')]))
                self.denominator = Integer(int(a[a.find('/') + 1:]))
        else:
            self.numerator = Integer(a)
            if not b:
                self.denominator = Integer(1)
            else:
                self.denominator = Integer(b)
        Rational.normalize(self)

    @staticmethod
    def gcd(a, b):
        if a >= b:
            r = a % b
            while r != 0:
                a = b
                b = r
                r = a % b
            return b
        else:
            return Rational.gcd(b, a)

    @staticmethod
    def normalize(q):
        if q.numerator != 0:
            g = Rational.gcd(q.numerator, q.denominator)
            q.numerator = q.numerator // g
            q.denominator = q.denominator // g
            if q.denominator < Integer(0):
                q.denominator *= Integer(-1)
                q.numerator *= Integer(-1)

    def value(self):
        return self.numerator.value / self.denominator.value

    def __int__(self):
        return self.numerator // self.denominator

    def __eq__(self, other):
        if type(other) == Rational:
            if self.numerator == other.numerator and self.denominator == other.denominator:
                return True
            else:
                return False
        if type(other) == Integer:
            if self.value() == other.value:
                return True
            else:
                return False
        else:
            if self.value() == other:
                return True
            else:
                return False

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

    def __repr__(self):
        return str(self.numerator) + '/' + str(self.denominator)

    def __mul__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator*other.numerator, self.denominator*other.denominator)
        else:
            return self*Rational(other)

    def __truediv__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator*other.denominator, self.denominator*other.numerator)
        else:
            return self/Rational(other)

    def __add__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator*other.denominator + other.numerator*self.denominator, self.denominator*other.denominator)
        else:
            return self+Rational(other)

    def __sub__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator*other.denominator - other.numerator*self.denominator, self.denominator*other.denominator)
        else:
            return self-Rational(other)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __pow__(self, power, modulo=None):
        return Rational(self.numerator**power, self.denominator**power)
