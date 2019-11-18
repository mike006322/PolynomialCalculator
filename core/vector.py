class Vector(list):

    def sdot(self):
        return self.dot(self)

    def dot(self, rhs: "Vector"):
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return sum(map(lambda x: x[0] * x[1], zip(self, rhs)))

    def proj_coeff(self, rhs: "Vector"):
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return self.dot(rhs) / self.sdot()

    def proj(self, rhs: "Vector") -> "Vector":
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return self.proj_coeff(rhs) * self

    def __sub__(self, rhs: "Vector") -> "Vector":
        rhs = Vector(rhs)
        assert len(self) == len(rhs)
        return Vector(x - y for x, y in zip(self, rhs))

    def __mul__(self, rhs) -> "Vector":
        return Vector(x * rhs for x in self)

    def __rmul__(self, lhs) -> "Vector":
        return Vector(x * lhs for x in self)

    def __repr__(self) -> str:
        return "[{}]".format(", ".join(str(x) for x in self))


if __name__ == '__main__':
    pass
