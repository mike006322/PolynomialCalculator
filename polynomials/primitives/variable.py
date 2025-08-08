"""
Variable object
aka indeterminate or unknown
"""

from __future__ import annotations

from typing import Any


class Variable:

    def __init__(self, label: Any):
        if not label:
            raise Exception('Variable must be a letter with optional number, e.g. "X", "X1')
        if isinstance(label, str):
            self.label: str = label
        elif isinstance(label, Variable):
            self.label = label.label
        else:
            self.label = str(label)

    def __str__(self) -> str:
        return self.label

    def __repr__(self) -> str:
        return self.label

    def __gt__(self, other: Any):
        if isinstance(other, Variable):
            return self.label > other.label
        return self.label > other

    def __lt__(self, other: Any):
        if isinstance(other, Variable):
            return self.label < other.label
        return self.label < other

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Variable):
            return self.label == other.label
        return self.label == other

    def __add__(self, other: Any):
        if isinstance(other, Variable):
            return self.label == other.label
        return self.label + other

    def __radd__(self, other: Any):
        if isinstance(other, Variable):
            return self.label == other.label
        return other + self.label

    def __hash__(self) -> int:
        return hash(repr(self))


if __name__ == "__main__":
    pass
