"""
Variable object
aka indeterminate or unknown
"""


class Variable:

    def __init__(self, label):
        if not label:
            raise Exception('Variable must be a letter with optional number, e.g. "X", "X1')
        if isinstance(label, str):
            self.label = label
        elif isinstance(label, Variable):
            self.label = Variable.label

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label

    def __gt__(self, other):
        if isinstance(other, Variable):
            return self.label > other.label
        return self.label > other

    def __lt__(self, other):
        if isinstance(other, Variable):
            return self.label < other.label
        return self.label < other

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.label == other.label
        return self.label == other

    def __add__(self, other):
        if isinstance(other, Variable):
            return self.label == other.label
        return self.label + other

    def __radd__(self, other):
        if isinstance(other, Variable):
            return self.label == other.label
        return other + self.label

    def __hash__(self):
        return hash(repr(self))


if __name__ == '__main__':
    pass
