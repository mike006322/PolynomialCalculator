"""Number types used by the polynomial library (Integer and Rational)."""
from __future__ import annotations

from typing import Any, Optional, Union

from polynomials.primitives.vector import Vector
import math

NumberLike = Union[int, float, "Integer", "Rational"]


class Integer:
    """
    Integer class represents members of ring of integers, Z
    division of integers that don't share common divisors yields a Rational number
    """

    __slots__ = ("value",)

    def __init__(self, i: Union[int, float, "Integer"]) -> None:
        self.value = int(i)

    def __int__(self) -> int:
        return self.value

    def __float__(self) -> float:
        return float(self.value)

    def __eq__(self, other: Any) -> bool:  # noqa: C901 keep legacy branching
        if isinstance(other, Integer):
            return self.value == other.value
        elif isinstance(other, Rational):
            return self.value == other.value()
        elif isinstance(other, int):
            return self.value == other
        else:
            try:
                return int(self) == other
            except Exception:
                return False

    def __bool__(self) -> bool:
        return self.value != 0

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Union[int, float, "Integer"]) -> bool:
        if isinstance(other, Integer):
            return self.value < other.value
        if isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented  # type: ignore[return-value]

    def __le__(self, other: Union[int, "Integer"]) -> bool:
        if isinstance(other, Integer):
            return self.value <= other.value
        if isinstance(other, int):
            return self.value <= other
        return NotImplemented  # type: ignore[return-value]

    def __gt__(self, other: Union[int, float, "Integer"]) -> bool:
        if isinstance(other, Integer):
            return self.value > other.value
        if isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented  # type: ignore[return-value]

    def __ge__(self, other: Union[int, "Integer"]) -> bool:
        if isinstance(other, Integer):
            return self.value >= other.value
        if isinstance(other, int):
            return self.value >= other
        return NotImplemented  # type: ignore[return-value]

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __add__(self, other: Any):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        if isinstance(other, int):
            return Integer(self.value + other)
        elif isinstance(other, Rational):
            return Rational(self) + other
        else:
            return self.value + other

    def __radd__(self, other: Any):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        if isinstance(other, int):
            return Integer(self.value + other)
        elif isinstance(other, Rational):
            return Rational(self) + other
        else:
            return self.value + other

    def __sub__(self, other: Any):
        return self + -other

    def __rsub__(self, other: Any):
        return -self + other

    def __abs__(self) -> "Integer":
        if self.value < 0:
            return Integer(-self)
        return self

    def __neg__(self) -> "Integer":
        return Integer(-self.value)

    def __mul__(self, other: Any):
        if isinstance(other, int):
            return Integer(self.value * other)
        if isinstance(other, complex):
            return self.value * other
        if isinstance(other, float):
            return self * Rational(other)
        if isinstance(other, Rational):
            return Rational(self * other.numerator, other.denominator)
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        if isinstance(other, Vector):
            return Vector.__mul__(other, self)
        else:
            return self.value * other

    def __rmul__(self, other: Any):
        return self * other

    def __pow__(self, power, modulo=None):  # type: ignore[override]
        # Small exponent fast paths
        if isinstance(power, Integer):
            p = int(power)
        else:
            p = power
        if isinstance(p, int):
            if p == 0:
                return Integer(1)
            if p == 1:
                return Integer(self.value)
            if p == 2:
                return Integer(self.value * self.value)
            # fall through for other integers
        if isinstance(power, Integer):
            return Integer(self.value ** int(power))
        res = self.value ** power
        if isinstance(res, int):
            return Integer(res)
        else:
            return res

    def __rpow__(self, other: Any):
        return other ** self.value

    def __mod__(self, other: Union[int, "Integer"]):
        if isinstance(other, Integer):
            return Integer(self.value % other.value)
        elif isinstance(other, int):
            return Integer(self.value % other)
        return NotImplemented  # type: ignore[return-value]

    def __floordiv__(self, other: "Integer") -> "Integer":
        return Integer(self.value // other.value)

    def __truediv__(self, other: Any):
        if isinstance(other, Integer):
            if self.value % other.value == 0:
                return self // other
            else:
                return Rational(self, other)
        if isinstance(other, Rational):
            return Rational(self * other.denominator, other.numerator)
        else:
            return self.value / other

    def __rtruediv__(self, other: Any):
        return other / self.value


class Rational:
    """
    Rational class represents members of field of rational numbers, Q
    """

    __slots__ = ("numerator", "denominator")

    def __init__(self, a: Any, b: Optional[Any] = None) -> None:
        if isinstance(a, Rational):
            if not b:
                self.numerator = a.numerator
                self.denominator = a.denominator
            else:
                temp = Rational(a, b)
                self.numerator = temp.numerator
                self.denominator = temp.denominator
                Rational.normalize(self)
        elif isinstance(a, float):
            integer_ratio = a.as_integer_ratio()
            if not b:
                self.numerator = Integer(integer_ratio[0])
                self.denominator = Integer(integer_ratio[1])
            if b:
                integer_ratio_a = integer_ratio
                if isinstance(b, float):
                    integer_ratio_b = b.as_integer_ratio()
                    self.numerator = Integer(integer_ratio_a[0] * integer_ratio_b[1])
                    self.denominator = Integer(integer_ratio_a[1] * integer_ratio_b[0])
                elif isinstance(b, (int, Integer)):
                    self.numerator = Integer(integer_ratio_a[0] * b)
                    self.denominator = Integer(integer_ratio_a[1])
            Rational.normalize(self)
        elif isinstance(a, str):
            if "/" in a:
                self.numerator = Integer(int(a[: a.find("/")]))
                self.denominator = Integer(int(a[a.find("/") + 1 :]))
            else:
                integer_ratio = float(a).as_integer_ratio()
                self.numerator = Integer(integer_ratio[0])
                self.denominator = Integer(integer_ratio[1])
            Rational.normalize(self)
        else:
            self.numerator = Integer(a)
            if not b:
                self.denominator = Integer(1)
            else:
                self.denominator = Integer(b)
            Rational.normalize(self)

    @staticmethod
    def gcd(a: Integer, b: Integer) -> Integer:
        # Fast path: use Python's highly optimized math.gcd on raw ints
        return Integer(math.gcd(int(a), int(b)))

    @staticmethod
    def normalize(q: "Rational") -> None:
        if q.numerator != 0:
            n = int(q.numerator)
            d = int(q.denominator)
            g = math.gcd(abs(n), abs(d))
            n //= g
            d //= g
            if d < 0:
                n = -n
                d = -d
            q.numerator = Integer(n)
            q.denominator = Integer(d)

    def value(self) -> float:
        return self.numerator.value / self.denominator.value

    def __abs__(self) -> "Rational":
        if self.numerator < 0:
            return -self
        else:
            return self

    def __float__(self) -> float:
        return self.numerator.value / self.denominator.value

    def __int__(self) -> int:
        # Truncate toward zero using integer arithmetic (no floats)
        n = self.numerator.value
        d = self.denominator.value
        if d == 0:
            raise ZeroDivisionError("division by zero in Rational.__int__")
        q = abs(n) // abs(d)
        return q if (n >= 0) == (d >= 0) else -q

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Rational):
            if self.numerator == 0:
                return other.numerator == 0
            return self.numerator == other.numerator and self.denominator == other.denominator
        if isinstance(other, Integer):
            return self.value() == other.value
        if isinstance(other, (float, int)):
            return self == Rational(other)
        else:
            try:
                return self.value() == other
            except Exception:
                return False

    def __str__(self) -> str:
        if self.denominator == 1 or self.numerator == 0:
            return str(self.numerator)
        return str(self.numerator) + "/" + str(self.denominator)

    def __repr__(self) -> str:
        return str(self)

    def __mul__(self, other: Any):
        # Quick zeros/ones
        if isinstance(other, (int, float, Integer)):
            if other == 0 or other == 0.0:
                return Integer(0)
            if other == 1 or other == 1.0:
                return self
            if other == -1 or other == -1.0:
                return -self
        if isinstance(other, Rational):
            if other.numerator == other.denominator:
                return self
            if other.numerator == 0:
                return Integer(0)
            return Rational(self.numerator * other.numerator, self.denominator * other.denominator)
        if isinstance(other, Integer):
            return Rational(self.numerator * other, self.denominator)
        if isinstance(other, int):
            return Rational(self.numerator * other, self.denominator)
        if isinstance(other, float):
            return self * Rational(other)
        if isinstance(other, Vector):
            return Vector.__mul__(other, self)
        else:
            return self.value() * other

    def __rmul__(self, other: Any):
        return self * other

    def __truediv__(self, other: Any):
        # Quick zeros/ones
        if isinstance(other, (int, float, Integer)):
            if other == 1 or other == 1.0:
                return self
            if other == -1 or other == -1.0:
                return -self
            if other == 0 or other == 0.0:
                raise ZeroDivisionError("division by zero")
        if isinstance(other, Rational):
            if other.numerator == other.denominator:
                return self
            if other.numerator == 0:
                raise ZeroDivisionError("division by zero")
            return Rational(self.numerator * other.denominator, self.denominator * other.numerator)
        if isinstance(other, Integer):
            return Rational(self.numerator, self.denominator * other)
        if isinstance(other, float):
            return self / Rational(*other.as_integer_ratio())
        else:
            return self.value() / other

    def __rtruediv__(self, other: Any):
        return Rational(other) / self

    def __floordiv__(self, other: Any):
        if isinstance(other, (float, int, Integer)):
            return self // Rational(other)
        c = self / other
        return Rational(c.numerator // c.denominator)

    def __rfloordiv__(self, other: Any):
        return Rational(other) // self

    def __add__(self, other: Any):
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.denominator + other.numerator * self.denominator,
                self.denominator * other.denominator,
            )
        else:
            return self + Rational(other)

    def __radd__(self, other: Any):
        return self + Rational(other)

    def __sub__(self, other: Any):
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.denominator - other.numerator * self.denominator,
                self.denominator * other.denominator,
            )
        else:
            return self - Rational(other)

    def __rsub__(self, other: Any):
        return -(self - other)

    def __neg__(self) -> "Rational":
        return Rational(-self.numerator, self.denominator)

    def __pow__(self, power: int, modulo=None):  # type: ignore[override]
        return Rational(self.numerator ** power, self.denominator ** power)

    def __gt__(self, other: Union[int, float, "Rational"]) -> bool:
        if isinstance(other, Rational):
            return self.numerator * other.denominator > other.numerator * self.denominator
        if isinstance(other, int):
            return self.numerator > other * self.denominator
        if isinstance(other, float):
            return self > Rational(other)
        return NotImplemented  # type: ignore[return-value]

    def __lt__(self, other: Union[int, float, "Rational"]) -> bool:
        if isinstance(other, Rational):
            return self.numerator * other.denominator < other.numerator * self.denominator
        if isinstance(other, (int, float)):
            return self.numerator < other * self.denominator
        return NotImplemented  # type: ignore[return-value]

    def __ge__(self, other: Union[int, float, "Rational"]) -> bool:
        return bool(self == other or self > other)

    def __le__(self, other: Union[int, float, "Rational"]) -> bool:
        return bool(self == other or self < other)

    def __round__(self) -> Integer:
        part_less_than_one = (self.numerator % self.denominator) / self.denominator
        if part_less_than_one <= 0.5:
            return Integer(self.numerator // self.denominator)
        else:
            return Integer(self.numerator // self.denominator) + 1

    def __mod__(self, other: Any):
        t = self // other
        return self - t * other

    def __rmod__(self, other: Any):
        return Rational(other) % self


if __name__ == "__main__":
    pass
