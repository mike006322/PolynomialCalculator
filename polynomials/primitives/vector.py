from functools import lru_cache
from typing import Sequence, Union


Number = Union[int, float]
VectorLike = Sequence[Number]


class Vector(list):

    def __init__(self, *args: VectorLike):
        if len(args) == 1:
            super().__init__(*args)
        elif len(args) > 1:
            super().__init__(list(args))

    @lru_cache(maxsize=None)
    def sdot(self) -> Number:
        return self.dot(self)

    @lru_cache(maxsize=None)
    def dot(self, rhs: "Vector") -> Number:
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return sum(map(lambda x: x[0] * x[1], zip(self, rhs)))

    @lru_cache(maxsize=None)
    def proj_coeff(self, rhs: "Vector") -> Number:
        # Project self onto rhs: <self, rhs> / <rhs, rhs>
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return self.dot(rhs) / rhs.dot(rhs)

    @lru_cache(maxsize=None)
    def proj(self, rhs: "Vector") -> "Vector":
        # Projection of self onto rhs: proj_coeff * rhs
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return self.proj_coeff(rhs) * rhs

    @lru_cache(maxsize=None)
    def __add__(self, other: "Vector") -> "Vector":
        assert len(self) == len(other)
        return Vector([x + y for x, y in zip(self, other)])

    def __sub__(self, rhs: "Vector") -> "Vector":
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return Vector([x - y for x, y in zip(self, rhs)])

    def __mul__(self, rhs: Union[Number, "Vector"]):
        if isinstance(rhs, Vector):
            return self.dot(rhs)
        return Vector([x * rhs for x in self])

    def __rmul__(self, lhs: Number) -> "Vector":
        return Vector([x * lhs for x in self])

    def __repr__(self) -> str:
        return "[{}]".format(", ".join(str(x) for x in self))

    def __hash__(self) -> int:
        return hash(repr(self))


if __name__ == '__main__':
    pass
