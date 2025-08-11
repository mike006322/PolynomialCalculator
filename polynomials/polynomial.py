import logging
import os
from dataclasses import dataclass
from numbers import Integral
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

from polynomials.display import format_number
from polynomials.formulas import solve
from polynomials.poly_parser import (
    InputError,
    construct_expression_tree,
    decide_operation,
    order_prefix,
    parse_function,
)
from polynomials.primitives.polycalc_numbers import Integer, Rational
from polynomials.primitives.variable import Variable
from utils.dfs import dfs_post_order as dfs

try:
    from typing import TypeAlias  # type: ignore[attr-defined]
except Exception:
    try:
        from typing_extensions import TypeAlias  # type: ignore
    except Exception:  # pragma: no cover - fallback for very old typing
        from typing import Any as _Any
        TypeAlias = _Any  # type: ignore

logger = logging.getLogger(__name__)
_DEBUG = os.environ.get("POLYCALC_DEBUG") in {"1", "true", "True"}

# Public exports from this module
__all__ = [
    "Polynomial",
    "Monomial",
    "TermsView",
    "NonFactor",
    "divides",
    "monomial_divide",
    "division_algorithm",
    "division_string",
    "gcd",
    "lcm",
]

NumberLike: TypeAlias = Union[int, float, complex, Integer, Rational]


# Core monomial for sparse dict representation: Monomial -> coeff
@dataclass(frozen=True)
class Monomial:
    """Immutable monomial key (cached hash for speed)."""
    vars: Tuple[str, ...]
    exps: Tuple[int, ...]

    def __post_init__(self):  # cache hash (Python spends time hashing in large products)
        object.__setattr__(self, "_hash", hash((self.vars, self.exps)))

    def __hash__(self):  # pragma: no cover - trivial
        return getattr(self, "_hash", hash((self.vars, self.exps)))  # type: ignore[attr-defined]

    def degree(self) -> int:
        return sum(self.exps)

    def mul(self, other: "Monomial") -> "Monomial":  # pragma: no cover - simple
        assert self.vars == other.vars
        return Monomial(self.vars, tuple(a + b for a, b in zip(self.exps, other.exps)))

    @staticmethod
    def unit(vars: Tuple[str, ...]) -> "Monomial":  # pragma: no cover - simple
        return Monomial(vars, tuple(0 for _ in vars))


class TermsView:
    """
    A dict-like and callable view over a Polynomial's internal term map.
    - Mapping interface proxies to the underlying dict of {Monomial: coeff}.
    - Calling the object (view()) yields an iterator of term Polynomials
      for backward compatibility with code/tests that used terms() as a method.
    """
    def __init__(self, owner: "Polynomial", backing: Dict["Monomial", Any]):
        self._owner = owner
        self._backing = backing

    # Callable: returns iterator of term polynomials
    def __call__(self) -> Iterable["Polynomial"]:
        return self._owner.iter_terms()

    # Mapping protocol
    def __getitem__(self, key: "Monomial"):
        return self._backing[key]

    def __setitem__(self, key: "Monomial", value: Any) -> None:
        self._backing[key] = value

    def __delitem__(self, key: "Monomial") -> None:
        del self._backing[key]

    def get(self, key: "Monomial", default: Any = None) -> Any:
        return self._backing.get(key, default)

    def items(self):
        return self._backing.items()

    def keys(self):
        return self._backing.keys()

    def values(self):
        return self._backing.values()

    def update(self, *args, **kwargs) -> None:
        self._backing.update(*args, **kwargs)

    def clear(self) -> None:
        self._backing.clear()

    def pop(self, *args, **kwargs):
        return self._backing.pop(*args, **kwargs)

    def __iter__(self):
        return iter(self._backing)

    def __len__(self) -> int:
        return len(self._backing)

    def __bool__(self) -> bool:
        return bool(self._backing)


def reindex_poly(p: "Polynomial", target: Tuple[str, ...]) -> "Polynomial":
    if p.vars == target:
        return p.copy()
    pos = {v: i for i, v in enumerate(target)}
    rp = Polynomial(0, p.field_characteristic)
    rp.vars = target
    rp.terms = {}
    for m, c in p.terms.items():
        exps = [0] * len(target)
        for v, e in zip(m.vars, m.exps):
            if e:
                exps[pos[v]] = e
        nm = Monomial(target, tuple(exps))
        rp.terms[nm] = rp.terms.get(nm, 0) + c
    rp._filter_zero_terms()
    return rp


def align_polynomials(polys: Sequence["Polynomial"]) -> List["Polynomial"]:
    var_names = set()
    for p in polys:
        var_names.update(p.vars)
    unified = tuple(sorted(var_names))
    return [reindex_poly(p, unified) for p in polys]


class NonFactor(Exception):
    def __init__(self, q, p):
        super().__init__(f"{q} does not divide {p}")


class Polynomial:
    @staticmethod
    def from_constant(c, vars=(), char=0):
        p = Polynomial(0, char)
        p.vars = tuple(vars)
        p.terms = {} if c == 0 else {Monomial.unit(p.vars): c}
        return p

    @staticmethod
    def from_term(coeff, vars, exps, char=0):
        p = Polynomial(0, char)
        p.vars = tuple(vars)
        m = Monomial(p.vars, tuple(int(e) for e in exps))
        p.terms = {} if coeff == 0 else {m: coeff}
        return p

    __slots__ = ("field_characteristic", "_lt_cache", "vars", "_terms")

    # Expose dict-like terms with callable behavior via a TermsView
    @property
    def terms(self) -> TermsView:
        return TermsView(self, self._terms)

    @terms.setter
    def terms(self, value: Dict[Monomial, Any]) -> None:
        # Accept either a raw dict or an existing TermsView
        if isinstance(value, TermsView):
            self._terms = dict(value.items())
        else:
            self._terms = dict(value)

    def _invalidate_caches(self) -> None:
        self._lt_cache = None

    def _cleanup_zeros(self) -> None:
        if not hasattr(self, "_terms") or not self._terms:
            return
        to_del = [m for m, c in self._terms.items() if c == 0]
        for m in to_del:
            del self._terms[m]

    def _filter_zero_terms(self) -> None:
        self._cleanup_zeros()
        self._invalidate_caches()

    # Basic operations on aligned vars
    def add(self, other: "Polynomial") -> "Polynomial":
        assert self.vars == other.vars
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        res.terms = dict(self.terms.items())
        for m, c in other.terms.items():
            res.terms[m] = res.terms.get(m, 0) + c
        res.mod_char()
        res._filter_zero_terms()
        return res

    def sub(self, other: "Polynomial") -> "Polynomial":
        assert self.vars == other.vars
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        res.terms = dict(self.terms.items())
        for m, c in other.terms.items():
            res.terms[m] = res.terms.get(m, 0) - c
        res.mod_char()
        res._filter_zero_terms()
        return res

    def scale(self, k) -> "Polynomial":
        if k == 0:
            return Polynomial(0, self.field_characteristic)
        if k == 1:
            return self.copy()
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        res.terms = {m: c * k for m, c in self.terms.items()}
        res.mod_char()
        res._filter_zero_terms()
        return res

    def mul(self, other: "Polynomial") -> "Polynomial":
        assert self.vars == other.vars
        # Micro-optimised nested multiplication (hot path in benchmarks)
        if not self.terms or not other.terms:
            return Polynomial(0, self.field_characteristic)
        # Single term short-circuits
        if len(self.terms) == 1:
            (m1, c1), = self.terms.items()
            return other.scale(c1).shift_exponents(m1.exps, self.vars)
        if len(other.terms) == 1:
            (m2, c2), = other.terms.items()
            return self.scale(c2).shift_exponents(m2.exps, self.vars)
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        out: Dict[Monomial, Any] = {}
        vars_tuple = self.vars
        # Localize for speed
        self_items = list(self.terms.items())
        other_items = list(other.terms.items())
        for m1, c1 in self_items:
            e1 = m1.exps
            for m2, c2 in other_items:
                # Combine exponents without creating intermediate list comprehension object
                exps = tuple(a + b for a, b in zip(e1, m2.exps))
                nm = Monomial(vars_tuple, exps)
                out[nm] = out.get(nm, 0) + c1 * c2
        res.terms = out
        res.mod_char()
        res._filter_zero_terms()
        return res

    def shift_exponents(self, delta: Tuple[int, ...], vars_tuple: Tuple[str, ...]) -> "Polynomial":
        """Internal helper: shift all monomials by delta exponent vector (non-negative)."""
        if not any(delta):
            return self.copy()
        res = Polynomial(0, self.field_characteristic)
        res.vars = vars_tuple
        new_terms: Dict[Monomial, Any] = {}
        for m, c in self.terms.items():
            exps = tuple(a + b for a, b in zip(m.exps, delta))
            new_terms[Monomial(vars_tuple, exps)] = new_terms.get(Monomial(vars_tuple, exps), 0) + c
        res.terms = new_terms
        res._filter_zero_terms()
        return res

    def items_sorted(self):
        def order_key(m: Monomial):
            return (m.degree(), m.exps)
        return sorted(self.terms.items(), key=lambda kv: order_key(kv[0]), reverse=True)

    def leading_term(self, order_key=None):
        if not self.terms:
            return None
        if order_key is None:
            def order_key(m: Monomial):
                return (m.degree(), m.exps)
        m = max(self.terms, key=order_key)
        return m, self.terms[m]

    @staticmethod
    def make_polynomial_from_tree(node) -> "Polynomial":
        def make_primitive_polynomial(s: str) -> "Polynomial":
            if s.isnumeric() or "." in s:
                return Polynomial(float(s))
            p = Polynomial(0)
            p.vars = (s,)
            p.terms = {Monomial((s,), (1,)): 1.0}
            return p

        def make_poly(child):
            if isinstance(child.value, str):
                child.value = make_primitive_polynomial(child.value)
            return child

        def collapse(current_node) -> None:
            if current_node.has_children():
                left = make_poly(current_node.left)
                right = make_poly(current_node.right)
                current_node.value = decide_operation(left.value, right.value, current_node.value)
            else:
                current_node = make_poly(current_node)

        dfs(node, collapse)
        return node.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Polynomial):
            a, b = align_polynomials([self, other])
            if len(a.terms) != len(b.terms):
                return False
            for (ma, ca), (mb, cb) in zip(a.items_sorted(), b.items_sorted()):
                if ma.exps != mb.exps:
                    return False
                # Compare coefficients with a small tolerance to avoid formatting/rounding diffs
                try:
                    fa = float(ca)
                    fb = float(cb)
                    if abs(fa - fb) > 1e-9:
                        return False
                except Exception:
                    if ca != cb:
                        return False
            return True
        if other == 0:
            return len(self.terms) == 0
        if other == 1:
            if len(self.terms) != 1:
                return False
            (m, c), = list(self.terms.items())
            return all(e == 0 for e in m.exps) and float(c) == 1.0
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _add_poly(self, other: "Polynomial") -> "Polynomial":
        assert self.vars == other.vars
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        res.terms = dict(self.terms)
        for m, c in other.terms.items():
            res.terms[m] = res.terms.get(m, 0) + c
        res.mod_char()
        res._filter_zero_terms()
        return res

    def _sub_poly(self, other: "Polynomial") -> "Polynomial":
        assert self.vars == other.vars
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        res.terms = dict(self.terms)
        for m, c in other.terms.items():
            res.terms[m] = res.terms.get(m, 0) - c
        res._filter_zero_terms()
        return res

    def _scale_poly(self, k) -> "Polynomial":
        if k == 0:
            return Polynomial(0, self.field_characteristic)
        if k == 1:
            return self.copy()
        res = Polynomial(0, self.field_characteristic)
        res.vars = self.vars
        res.terms = {m: c * k for m, c in self.terms.items()}
        res.mod_char()
        res._filter_zero_terms()
        return res

    def __add__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        # Fast numeric zero/one paths without constructing temporary Polynomial objects
        if isinstance(other, (int, float, complex, Integer, Rational)):
            if other == 0:
                return self
            if not self.terms:
                return Polynomial(other, self.field_characteristic)
            # Treat numeric as constant polynomial
            other = Polynomial(other, self.field_characteristic)
        if not isinstance(other, Polynomial):  # fallback
            other = Polynomial(other, self.field_characteristic)
        if not self.terms:
            return other
        if not other.terms:
            return self
        if self.vars == other.vars:
            return self._add_poly(other)
        a, b = align_polynomials([self, other])
        return a._add_poly(b)

    def __radd__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        return self.__add__(other)

    def __sub__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        if isinstance(other, (int, float, complex, Integer, Rational)):
            if other == 0:
                return self
            other = Polynomial(other, self.field_characteristic)
        elif not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        if not other.terms:
            return self
        if not self.terms:
            return -other
        if self.vars == other.vars:
            return self._sub_poly(other)
        a, b = align_polynomials([self, other])
        return a._sub_poly(b)

    def __rsub__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        return Polynomial(other, self.field_characteristic).__sub__(self)

    def __neg__(self) -> "Polynomial":
        return self._scale_poly(-1)

    def __mul__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        # Scalar fast paths
        if isinstance(other, (int, float, complex, Integer, Rational)):
            if other == 0:
                return Polynomial(0, self.field_characteristic)
            if other == 1:
                return self
            return self._scale_poly(other)
        # Coerce
        if not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        # Zero checks
        if not self.terms or not other.terms:
            return Polynomial(0, self.field_characteristic)
        # Constant * poly
        if self.number_of_variables == 0:
            (m0, c0), = self.terms.items()
            return other._scale_poly(c0)
        if other.number_of_variables == 0:
            (m0, c0), = other.terms.items()
            return self._scale_poly(c0)
        # Align variable order if needed
        if self.vars != other.vars:
            a, b = align_polynomials([self, other])
        else:
            a, b = self, other
        # Internal optimized multiplication
        out = a.mul(b)
        out.mod_char()
        return out

    def __rmul__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        return self.__mul__(other)

    def __truediv__(
        self, other: Union["Polynomial", int, float, complex]
    ) -> Union["Polynomial", List["Polynomial"]]:
        if not isinstance(other, Polynomial):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            other = Polynomial(other, self.field_characteristic)
        elif other == 0:
            raise ZeroDivisionError("division by zero")
        q, r = division_algorithm(self, other)
        if r != Polynomial(0):
            raise NonFactor(other, self)
        if len(q) == 1:
            result: Union["Polynomial", List["Polynomial"]] = q[0]
        else:
            result = q
        if isinstance(result, Polynomial):
            result._filter_zero_terms()
        elif isinstance(result, list):
            for poly in result:
                if isinstance(poly, Polynomial):
                    poly._filter_zero_terms()
        return result

    def __mod__(self, other: Union["Polynomial", int, float, complex]) -> "Polynomial":
        if not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        _, r = division_algorithm(self, other)
        r._filter_zero_terms()
        return r

    def __call__(self, *args: Any, **kwargs: Any) -> "Polynomial":
        # Map variables to values
        var_list = self.variables
        if args:
            if len(args) != len(var_list):
                raise ValueError(f"Expected {len(var_list)} arguments, got {len(args)}")
            subs = dict(zip(var_list, args))
        else:
            subs = kwargs

        remaining_vars: List[str] = []
        substitutions: Dict[Any, Any] = {}
        provided_subs: Dict[str, Any] = {}
        for var, val in zip(var_list, args):
            provided_subs[str(var)] = val
        for k, v in kwargs.items():
            provided_subs[str(k)] = v

        for var in var_list:
            if var in subs:
                val = subs[var]
                if isinstance(val, str):
                    remaining_vars.append(val)
                    substitutions[var] = val
                elif isinstance(val, Polynomial):
                    if len(val.variables) == 1 and len(val.terms) == 1:
                        (m_v, c_v), = val.terms.items()
                        if float(c_v) == 1.0 and sum(m_v.exps) == 1 and max(m_v.exps) == 1:
                            new_var_name = val.variables[0]
                            remaining_vars.append(new_var_name)
                            substitutions[var] = new_var_name
                            continue
                    if val.number_of_variables == 0:
                        if not val.terms:
                            substitutions[var] = 0
                        else:
                            (m0, c0), = val.terms.items()
                            if all(e == 0 for e in m0.exps):
                                substitutions[var] = c0
                            else:
                                raise NotImplementedError("Complex polynomial substitution not yet supported")
                    else:
                        raise NotImplementedError("Complex polynomial substitution not yet supported")
                else:
                    substitutions[var] = val
            else:
                remaining_vars.append(var)

        if not remaining_vars:
            result_value: NumberLike = 0.0
            vals_map = {str(v): substitutions.get(v, 0) for v in var_list}
            for m, c in self.terms.items():
                prod: NumberLike = c
                for v, e in zip(m.vars, m.exps):
                    if e:
                        val = vals_map.get(v, 0)
                        prod = prod * (val ** e)
                result_value = result_value + prod
            return Polynomial.from_constant(result_value, self.vars, self.field_characteristic)
        else:
            target_vars = tuple(remaining_vars)
            idx_map = {v: i for i, v in enumerate(target_vars)}
            dsp_terms: Dict[Monomial, Any] = {}
            for m, c in self.terms.items():
                coeff_val: Any = c
                if isinstance(coeff_val, Polynomial):
                    try:
                        coeff_eval = coeff_val(**provided_subs) if provided_subs else coeff_val
                    except Exception:
                        coeff_eval = coeff_val
                    if isinstance(coeff_eval, Polynomial):
                        if not coeff_eval.terms:
                            coeff_val = 0.0
                        elif len(coeff_eval.terms) == 1:
                            (m0, c0), = coeff_eval.terms.items()
                            if all(e == 0 for e in m0.exps):
                                coeff_val = c0
                            else:
                                coeff_val = coeff_eval
                        else:
                            coeff_val = coeff_eval
                    else:
                        coeff_val = coeff_eval
                exps = [0] * len(target_vars)
                for v, e in zip(m.vars, m.exps):
                    if e == 0:
                        continue
                    if v in substitutions:
                        sub_val = substitutions[v]
                        if isinstance(sub_val, str):
                            j = idx_map.get(sub_val)
                            if j is not None:
                                exps[j] += e
                        else:
                            coeff_val = coeff_val * (sub_val ** e)
                    else:
                        j = idx_map.get(v)
                        if j is not None:
                            exps[j] += e
                nm = Monomial(target_vars, tuple(exps))
                dsp_terms[nm] = dsp_terms.get(nm, 0) + coeff_val
            result = Polynomial(0, self.field_characteristic)
            result.vars = target_vars
            result.terms = dsp_terms
            result._cleanup_zeros()
            result._filter_zero_terms()
            return result

    def __rtruediv__(
        self, other: Union["Polynomial", int, float, complex]
    ) -> Union["Polynomial", List["Polynomial"]]:
        return Polynomial(other, self.field_characteristic).__truediv__(self)

    def __pow__(self, n: Union[int, float, "Polynomial"]) -> "Polynomial":
        if isinstance(n, Polynomial):
            if n.number_of_variables == 0:
                if len(n.terms) == 0:
                    n_val = 0
                elif len(n.terms) == 1:
                    (m, c), = n.terms.items()
                    if all(e == 0 for e in m.exps):
                        n_val = c
                    else:
                        raise ValueError("Exponent polynomial must be constant.")
                else:
                    raise ValueError("Exponent polynomial must be constant.")
            else:
                raise ValueError("Exponent polynomial must be constant.")
        else:
            n_val = n
        if isinstance(n_val, float):
            if n_val.is_integer():
                n_val = int(n_val)
            else:
                raise ValueError(f"Exponent must be integer-valued, got float {n_val}")
        if not isinstance(n_val, int):
            raise ValueError(f"Exponent must be an integer, got {type(n_val)}")
        if n_val < 0:
            raise ValueError("Negative exponents not supported.")
        result = Polynomial(1, self.field_characteristic)
        base = self.copy()
        exp = n_val
        while exp > 0:
            if exp & 1:
                result *= base
            base *= base
            exp >>= 1
        return result

    def __repr__(self) -> str:
        parts = []
        for m, c in self.items_sorted():
            parts.append(f"({c},{m.exps})")
        vars_part = ",".join(self.vars)
        inner = ", ".join(parts) if parts else "0"
        return f"Polynomial(vars=({vars_part}), terms={inner})"

    def __str__(self) -> str:
        if not self.terms:
            return format_number(0.0)
        parts: List[str] = []
        for m, c in self.items_sorted():
            mon = []
            for v, e in zip(m.vars, m.exps):
                if e == 0:
                    continue
                if e == 1:
                    mon.append(v)
                else:
                    mon.append(f"{v}^{e}")
            mon_str = "".join(mon)
            if mon_str:
                if c == 1:
                    parts.append(mon_str)
                elif c == -1:
                    parts.append("-" + mon_str)
                else:
                    parts.append(f"{format_number(c)}{mon_str}")
            else:
                parts.append(format_number(c))
        s = " + ".join(parts)
        return s.replace("+ -", "- ")

    def copy(self) -> "Polynomial":
        import copy
        return copy.deepcopy(self)

    def LT(self) -> "Polynomial":
        if self._lt_cache is not None:
            return self._lt_cache
        if not self.terms:
            self._lt_cache = Polynomial(0, self.field_characteristic)
            return self._lt_cache
        (m, c) = self.items_sorted()[0]
        nz = [(v, e) for v, e in zip(m.vars, m.exps) if e != 0]
        if nz:
            vars_t, exps_t = zip(*nz)
            self._lt_cache = Polynomial.from_term(c, vars_t, exps_t, self.field_characteristic)
        else:
            self._lt_cache = Polynomial.from_constant(c, (), self.field_characteristic)
        return self._lt_cache

    def LM(self) -> "Polynomial":
        if not self.terms:
            return Polynomial(0, self.field_characteristic)
        (m, _) = self.items_sorted()[0]
        nz = [(v, e) for v, e in zip(m.vars, m.exps) if e != 0]
        if not nz:
            return Polynomial(1, self.field_characteristic)
        vars_t, exps_t = zip(*nz)
        return Polynomial.from_term(1.0, vars_t, exps_t, self.field_characteristic)

    def iter_terms(self) -> Iterable["Polynomial"]:
        for m, c in self.items_sorted():
            nz = [(v, e) for v, e in zip(m.vars, m.exps) if e != 0]
            if nz:
                vars_t, exps_t = zip(*nz)
                yield Polynomial.from_term(c, vars_t, exps_t, self.field_characteristic)
            else:
                yield Polynomial.from_constant(c, (), self.field_characteristic)

    def __iter__(self) -> Iterator["Polynomial"]:
        for term in self.iter_terms():
            yield term

    def degree(self) -> int:
        if not self.terms:
            return 0
        return max(m.degree() for m in self.terms.keys())

    def mod_char(self) -> "Polynomial":
        char = self.field_characteristic
        if char == 0 or not self.terms:
            return self
        new_terms: Dict[Monomial, Any] = {}
        for m, c in self.terms.items():
            try:
                new_c = c % char  # type: ignore[operator]
            except Exception:
                new_c = c
            if isinstance(new_c, (int, float, complex)) and new_c == 0:
                continue
            new_terms[m] = new_terms.get(m, 0) + new_c
        self.terms = new_terms
        self._filter_zero_terms()
        return self

    @property
    def variables(self) -> List[str]:
        used: List[str] = []
        seen = set()
        for m, _ in self.terms.items():
            for v, e in zip(m.vars, m.exps):
                if e and v not in seen:
                    seen.add(v)
                    used.append(v)
        return used

    @property
    def number_of_variables(self) -> int:
        return len(self.variables)

    @staticmethod
    def combine_variables(a: "Polynomial", b: "Polynomial") -> Tuple["Polynomial", "Polynomial"]:
        a_aligned, b_aligned = align_polynomials([a, b])
        return a_aligned, b_aligned

    def isolate(self, variable: Union[str, "Variable"]) -> "Polynomial":
        var_name = str(variable)
        if var_name not in self.variables:
            return Polynomial.from_constant(0.0, self.vars, self.field_characteristic)
        return self.copy()

    def derivative(self, var: Optional[Union[str, "Variable"]] = None) -> "Polynomial":
        if var is None:
            if not self.vars:
                return Polynomial.from_constant(0.0, self.vars, self.field_characteristic)
            var_name = self.vars[0]
        else:
            var_name = str(var)
        if var_name not in self.vars:
            return Polynomial.from_constant(0.0, self.vars, self.field_characteristic)
        vidx = self.vars.index(var_name)
        res = Polynomial.from_constant(0.0, self.vars, self.field_characteristic)
        for m, c in self.terms.items():
            e = m.exps[vidx]
            if e == 0:
                continue
            new_exps = list(m.exps)
            new_exps[vidx] = e - 1
            nm = Monomial(self.vars, tuple(new_exps))
            res.terms[nm] = res.terms.get(nm, 0) + c * e
        res._cleanup_zeros()
        return res

    @property
    def grad(self) -> List["Polynomial"]:
        class Gradient(list):
            def __init__(self, *args):
                super().__init__(*args)
                self.variables_in_order = tuple()

            def __call__(self, *args, **kwargs):
                kwargs.update(zip(map(str, self.variables_in_order), args))
                res = []
                for partial_derivative in self:
                    val = partial_derivative(**kwargs)
                    if isinstance(val, Polynomial):
                        res.append(val)
                    else:
                        res.append(Polynomial.from_constant(float(val)))
                return res

            def __repr__(self):
                res = ""
                for term in self:
                    res += str(term)
                return res

            def __str__(self):
                return self.__repr__()

        g = Gradient()
        vars_list = self.variables
        g.variables_in_order = tuple(vars_list)
        for v in vars_list:
            g.append(self.derivative(v))
        return g

    @property
    def hessian(self) -> List[List["Polynomial"]]:
        class Hessian(list):
            def __init__(self, *args):
                super().__init__(*args)
                self.variables_in_order = tuple()

            def __call__(self, *args, **kwargs):
                kwargs.update(zip(self.variables_in_order, args))
                res = []
                for line in self:
                    row = []
                    for partial_derivative in line:
                        val = partial_derivative(**kwargs)
                        if isinstance(val, Polynomial):
                            if not val.terms:
                                row.append(0.0)
                            elif len(val.terms) == 1:
                                (m_v, c_v), = val.terms.items()
                                if all(e == 0 for e in m_v.exps) and isinstance(c_v, (int, float)):
                                    row.append(float(c_v))
                                else:
                                    row.append(val)
                            else:
                                row.append(val)
                        else:
                            row.append(float(val))
                    res.append(row)
                return res

        h = Hessian()
        vars_list = self.variables
        h.variables_in_order = tuple(vars_list)
        n = len(vars_list)
        for i in range(n):
            h.append([])
            for j in range(n):
                var1 = vars_list[i]
                var2 = vars_list[j]
                h[i].append(self.derivative(var1).derivative(var2))
        return h

    def solve(self) -> Any:
        return solve(self)

    def __init__(self, poly: Any, char: int = 0):
        self.field_characteristic = char
        self._lt_cache = None
        if poly == 0:
            self.vars = tuple()
            self._terms = {}
        elif isinstance(poly, (int, float, complex, Integer, Rational, Integral)) and poly != 0:  # type: ignore[arg-type]
            self.vars = tuple()
            self._terms = {}
            m = Monomial(self.vars, tuple())
            self._terms[m] = float(poly)
        elif isinstance(poly, list):
            raise InputError
        elif isinstance(poly, str):
            tree = construct_expression_tree(order_prefix(parse_function(poly)))
            parsed = Polynomial.make_polynomial_from_tree(tree)
            self.vars = parsed.vars
            # parsed.terms may be a TermsView; handle via setter
            self.terms = dict(parsed.terms.items())
        elif isinstance(poly, Variable):
            tmp = Polynomial(str(poly.label))
            self.vars = tmp.vars
            self.terms = dict(tmp.terms.items())
        elif isinstance(poly, Monomial):
            self.vars = poly.vars
            self._terms = {poly: 1.0}
        elif isinstance(poly, Polynomial):
            self.vars = poly.vars
            self.terms = dict(poly.terms.items())
        else:
            raise InputError
        self._cleanup_zeros()
        self.mod_char()
        self._filter_zero_terms()


# Standalone helpers

def divides(a: "Polynomial", b: "Polynomial") -> bool:
    lt_a = a.leading_term()
    lt_b = b.leading_term()
    if lt_a is None or lt_b is None:
        return False
    (m_a, _), (m_b, _) = lt_a, lt_b
    exp_a = {v: e for v, e in zip(m_a.vars, m_a.exps)}
    exp_b = {v: e for v, e in zip(m_b.vars, m_b.exps)}
    for v in set(exp_a.keys()) | set(exp_b.keys()):
        if exp_a.get(v, 0) > exp_b.get(v, 0):
            return False
    return True


def monomial_divide(a: "Polynomial", b: "Polynomial") -> "Polynomial":
    lt_a = a.leading_term()
    lt_b = b.leading_term()
    if lt_a is None or lt_b is None:
        return Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
    (m_a, c_a), (m_b, c_b) = lt_a, lt_b
    if c_b == 0:
        return Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
    exp_a = {v: e for v, e in zip(m_a.vars, m_a.exps)}
    exp_b = {v: e for v, e in zip(m_b.vars, m_b.exps)}
    all_vars = sorted(set(exp_a.keys()) | set(exp_b.keys()))
    exps: List[int] = []
    for v in all_vars:
        diff = exp_a.get(v, 0) - exp_b.get(v, 0)
        if diff < 0:
            return Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
        exps.append(diff)
    coeff = c_a / c_b
    nz = [(v, e) for v, e in zip(all_vars, exps) if e != 0]
    if nz:
        vvars, vexps = zip(*nz)
        return Polynomial.from_term(coeff, vvars, vexps, a.field_characteristic)
    else:
        return Polynomial.from_constant(coeff, (), a.field_characteristic)


def division_algorithm(
    input_poly: "Polynomial", *others: "Polynomial"
) -> Tuple[List["Polynomial"], "Polynomial"]:
    char = input_poly.field_characteristic
    polys = [input_poly] + list(others)
    aligned = align_polynomials(polys)
    p_work, *divisors = [p.copy() for p in aligned]
    unified_vars = p_work.vars
    if not divisors:
        r_only = p_work.copy()
        r_only.mod_char()
        return [], r_only
    quotients: List[Polynomial] = [Polynomial.from_constant(0, unified_vars, char) for _ in divisors]
    remainder = Polynomial.from_constant(0, unified_vars, char)

    def is_zero(poly: Polynomial) -> bool:
        return not poly.terms

    if is_zero(p_work):
        qs = [q.copy() for q in quotients]
        r = remainder.copy()
        return qs, r

    precomp_others_lt = [d.leading_term() for d in divisors]
    max_steps = 1000
    steps = 0

    while not is_zero(p_work):
        if steps > max_steps:
            if _DEBUG:
                logger.debug(
                    "division_algorithm: exceeded max steps, possible infinite loop. p=%s",
                    str(p_work),
                )
            break
        prev_p_work = p_work.copy()
        i = 0
        division_occurred = False
        lt_p = p_work.leading_term()
        while i < len(divisors) and not division_occurred:
            lt_d = precomp_others_lt[i]
            if lt_p is None or lt_d is None:
                i += 1
                continue
            (m_p, c_p) = lt_p
            (m_d, c_d) = lt_d
            divisible = True
            for ep, ed in zip(m_p.exps, m_d.exps):
                if ed > ep:
                    divisible = False
                    break
            if divisible and c_d != 0:
                exps_q = tuple(ep - ed for ep, ed in zip(m_p.exps, m_d.exps))
                coeff_q = c_p / c_d
                if all(e == 0 for e in exps_q):
                    mono_q = Polynomial.from_constant(coeff_q, unified_vars)
                else:
                    mono_q = Polynomial.from_term(coeff_q, unified_vars, exps_q)
                quotients[i] = quotients[i].add(mono_q)
                p_work = p_work.sub(divisors[i].mul(mono_q))
                division_occurred = True
            else:
                i += 1
        if not division_occurred:
            if lt_p is None:
                break
            (m_p, c_p) = lt_p
            mono = (
                Polynomial.from_constant(c_p, unified_vars)
                if all(e == 0 for e in m_p.exps)
                else Polynomial.from_term(c_p, unified_vars, m_p.exps)
            )
            remainder = remainder.add(mono)
            p_work = p_work.sub(mono)
        if p_work.terms == prev_p_work.terms:
            if _DEBUG:
                logger.debug(
                    "division_algorithm: no progress, breaking to avoid infinite loop. p=%s",
                    str(p_work),
                )
            break
        steps += 1
    a: List[Polynomial] = [q.copy() for q in quotients]
    r = remainder.copy()
    for poly in a:
        poly.mod_char()
    r.mod_char()
    return a, r


def division_string(p: "Polynomial", *others: "Polynomial") -> str:
    from polynomials.display import display_mode

    with display_mode("float"):
        a, r = division_algorithm(p, *others)
        res = str(p) + " = "
        for i in range(len(a)):
            res += "(" + str(a[i]) + ")" + "*" + "(" + str(others[i]) + ")" + " + "
        if res.endswith(" + "):
            res = res[:-3]
        res += " + (remainder:) " + str(r)
        return res


def gcd(a: "Polynomial", b: "Polynomial") -> "Polynomial":
    a = a.copy()
    b = b.copy()
    import math
    if (len(a.terms) == 1) and (len(b.terms) == 1):
        a_aligned, b_aligned = align_polynomials([a, b])
        lt_a = a_aligned.leading_term()
        lt_b = b_aligned.leading_term()
        if lt_a is None or lt_b is None:
            return Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
        (m_a, c_a) = lt_a
        (m_b, c_b) = lt_b
        coeff_gcd = math.gcd(int(abs(c_a)), int(abs(c_b)))
        exps = [min(ea, eb) for ea, eb in zip(m_a.exps, m_b.exps)]
        result = Polynomial.from_term(float(coeff_gcd), a_aligned.vars, exps, a.field_characteristic)
        result._filter_zero_terms()
        return result
    if len(set(a.variables).union(set(b.variables))) <= 1:
        g = gcd_singlevariate(a, b)
        if not g.terms:
            return Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
        if len(g.terms) == 1:
            (m_g, c_g), = g.terms.items()
            if all(e == 0 for e in m_g.exps):
                return Polynomial.from_constant(float(c_g), (), a.field_characteristic)
        return g
    if (len(a.terms) > 1) or (len(b.terms) > 1):
        raise NotImplementedError(
            "gcd for multivariate polynomials with more than one term is not implemented"
        )
    if (not a.terms) or (not b.terms):
        return Polynomial.from_constant(0.0)
    (_, c_a), = a.terms.items()
    (_, c_b), = b.terms.items()
    res = gcd_singlevariate(Polynomial(c_a), Polynomial(c_b))
    if not res.terms:
        res = Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
    elif len(res.terms) == 1:
        (m_r, c_r), = res.terms.items()
        if all(e == 0 for e in m_r.exps):
            res = Polynomial.from_constant(float(c_r), (), a.field_characteristic)
    return res


def gcd_singlevariate(a: "Polynomial", b: "Polynomial") -> "Polynomial":
    a = a.copy()
    b = b.copy()
    if a.degree() >= b.degree():
        r = a % b
        max_steps = 1000
        steps = 0
        if b == Polynomial(0):
            return a
        while r != 0:
            if steps > max_steps:
                if _DEBUG:
                    logger.debug(
                        "gcd_singlevariate: exceeded max steps, possible infinite loop. a=%s b=%s r=%s",
                        a,
                        b,
                        r,
                    )
                break
            a = b
            b = r
            if not b.terms:
                return a
            if len(b.terms) == 1:
                (m_b, c_b), = b.terms.items()
                if all(e == 0 for e in m_b.exps):
                    return Polynomial(1, a.field_characteristic)
            r = a % b
            steps += 1
        return b
    else:
        return gcd(b, a)


def lcm(a: "Polynomial", b: "Polynomial") -> Union["Polynomial", List["Polynomial"]]:
    lcm_poly = a * b / gcd(a, b)
    if isinstance(lcm_poly, Polynomial):
        if not lcm_poly.terms:
            lcm_poly = Polynomial.from_constant(0.0, a.vars, a.field_characteristic)
        elif len(lcm_poly.terms) == 1:
            (m_l, c_l), = lcm_poly.terms.items()
            if all(e == 0 for e in m_l.exps):
                lcm_poly = Polynomial.from_constant(float(c_l), a.vars, a.field_characteristic)
    return lcm_poly
