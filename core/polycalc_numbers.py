# This module defines number classes so that numbers can be manipulated and presented symbolically

from core.vector import Vector


class Integer:
    """
    Integer class represents members of ring of integers, Z
    division of integers that don't share common divisors yields a Rational number
    """

    def __init__(self, i):
        self.value = int(i)

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        if type(other) == Integer:
            if self.value == other.value:
                return True
            else:
                return False
        elif type(other) == Rational:
            if self.value == other.value():
                return True
            else:
                return False
        elif type(other) == int:
            return self.value == other
        else:
            if int(self) == other:
                return True
            else:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if type(other) == Integer:
            return self.value < other.value
        if type(other) in {int, float}:
            return self.value < other

    def __le__(self, other):
        if type(other) == Integer:
            return self.value <= other.value
        if type(other) == int:
            return self.value <= other

    def __gt__(self, other):
        if type(other) == Integer:
            return self.value > other.value
        if type(other) in {int, float}:
            return self.value > other

    def __ge__(self, other):
        if type(other) == Integer:
            return self.value >= other.value
        if type(other) == int:
            return self.value >= other

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        if type(other) == Integer:
            return Integer(self.value + other.value)
        if type(other) == int:
            return Integer(self.value + other)
        elif type(other) == Rational:
            return Rational(self) + other
        else:
            return self.value + other

    def __radd__(self, other):
        if type(other) == Integer:
            return Integer(self.value + other.value)
        if type(other) == int:
            return Integer(self.value + other)
        elif type(other) == Rational:
            return Rational(self) + other
        else:
            return self.value + other

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __abs__(self):
        if self.value < 0:
            return Integer(-self)
        return self

    def __neg__(self):
        return Integer(-self.value)

    def __mul__(self, other):
        if type(other) == int:
            return Integer(self.value * other)
        if type(other) == complex or type(other) == float:
            return self.value * other
        if type(other) == Rational:
            return Integer(self.value * other.value())
        if type(other) == Integer:
            return Integer(self.value * other.value)
        if type(other) == Vector:
            return Vector.__mul__(other, self)
        else:
            return self.value * other

    def __rmul__(self, other):
        if type(other) == int:
            return Integer(self.value * other)
        if type(other) == complex or type(other) == float:
            return self.value * other
        if type(other) == Rational:
            return Integer(self.value * other.value())
        else:
            return Integer(self.value * other.value)

    def __pow__(self, power, modulo=None):
        if type(power) == Integer:
            return Integer(self.value ** int(power))
        if type(self.value ** power) == int:
            return Integer(self.value ** power)
        else:
            return self.value ** power

    def __rpow__(self, other):
        return other ** self.value

    def __mod__(self, other):
        if type(other) == Integer:
            return Integer(self.value % other.value)
        elif type(other) == int:
            return Integer(self.value % other)

    def __floordiv__(self, other):
        return Integer(self.value // other.value)

    def __truediv__(self, other):
        if type(other) == Integer:
            if self.value % other.value == 0:
                return self // other
            else:
                return Rational(self, other)
        if type(other) == Rational:
            return Rational(self * other.denominator, other.numerator)
        else:
            return self.value / other

    def __rtruediv__(self, other):
        return other / self.value


class Rational:
    """
    Rational class represents members of field of rational numbers, Q
    """
    __slots__ = ('numerator', 'denominator')

    def __init__(self, a, b=None):
        if type(a) == Rational:
            if not b:
                self.numerator = a.numerator
                self.denominator = a.denominator
            else:
                temp = Rational(a, b)
                self.numerator = temp.numerator
                self.denominator = temp.denominator
        elif type(a) == float:
            integer_ratio = a.as_integer_ratio()
            if not b:
                self.numerator = Integer(integer_ratio[0])
                self.denominator = Integer(integer_ratio[1])
            if b:
                integer_ratio_a = integer_ratio
                if type(b) == float:
                    integer_ratio_b = b.as_integer_ratio()
                    self.numerator = Integer(integer_ratio_a[0] * integer_ratio_b[1])
                    self.denominator = Integer(integer_ratio_a[1] * integer_ratio_b[0])
                elif type(b) in {int, Integer}:
                    self.numerator = Integer(integer_ratio_a[0] * b)
                    self.denominator = Integer(integer_ratio_a[1])
        elif type(a) == str:
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

    def __abs__(self):
        if self.numerator < 0:
            return -self
        else:
            return self

    def __float__(self):
        return self.numerator.value / self.denominator.value

    def __int__(self):
        return int(self.numerator / self.denominator)

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
        if self.denominator == 1:
            return str(self.numerator)
        return str(self.numerator) + '/' + str(self.denominator)

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator * other.numerator, self.denominator * other.denominator)
        if type(other) == Vector:
            return Vector.__mul__(other, self)
        else:
            return self.value() * other

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator * other.denominator, self.denominator * other.numerator)
        if type(other) == Integer:
            return Rational(self.numerator, self.denominator * other)
        else:
            return self.value() / other

    def __floordiv__(self, other):
        c = self / other
        return c.numerator // c.denominator

    def __add__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator * other.denominator + other.numerator * self.denominator,
                            self.denominator * other.denominator)
        else:
            return self + Rational(other)

    def __radd__(self, other):
        return self + Rational(other)

    def __sub__(self, other):
        if type(other) == Rational:
            return Rational(self.numerator * other.denominator - other.numerator * self.denominator,
                            self.denominator * other.denominator)
        else:
            return self - Rational(other)

    def __rsub__(self, other):
        return -(self - other)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __pow__(self, power, modulo=None):
        return Rational(self.numerator ** power, self.denominator ** power)

    def __gt__(self, other):
        if type(other) == Rational:
            return self.numerator * other.denominator > other.numerator * self.denominator
        if type(other) in {int, float}:
            return self.numerator > other * self.denominator

    def __lt__(self, other):
        if type(other) == Rational:
            return self.numerator * other.denominator < other.numerator * self.denominator
        if type(other) in {int, float}:
            return self.numerator < other * self.denominator

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other

    def __round__(self):
        part_less_than_one = (self.numerator % self.denominator) / self.denominator
        if part_less_than_one <= 0.5:
            return Integer(self.numerator//self.denominator)
        else:
            return Integer(self.numerator//self.denominator) + 1


if __name__ == '__main__':
    pass
