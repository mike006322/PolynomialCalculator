from polynomials.poly_parser import construct_expression_tree, order_prefix, parse_function, decide_operation, InputError
from polynomials.orderings import order_lex as order
from polynomials.orderings import graded_lex as graded_order
from polynomials.collect_like_terms import collect_like_terms
from polynomials.formulas import solve
from polynomials.primitives.polycalc_numbers import Integer, Rational
from utils.dfs import dfs_post_order as dfs
from polynomials.primitives.variable import Variable
import numpy as np

class NonFactor(Exception):
    def __init__(self, q, p):
        super().__init__("{} does not divide {}".format(q, p))

class Polynomial:

    def _filter_zero_terms(self):
        """Remove zero terms from the term matrix, except for canonical zero polynomial."""
        if not self.term_matrix or len(self.term_matrix) < 2:
            return
        header = self.term_matrix[0]
        # A term is zero if its coefficient is zero.
        nonzero_terms = [term for term in self.term_matrix[1:] if term[0] != 0]
        if nonzero_terms:
            self.term_matrix = [header] + nonzero_terms
        else:
            # Canonical zero polynomial
            self.term_matrix = [header, [0.0] + [0] * (len(header) - 1)]

    @staticmethod
    def make_polynomial_from_tree(node):
        def make_primitive_polynomial(s: str):
            if s.isnumeric() or '.' in s:
                return Polynomial(float(s))
            else:
                return Polynomial([['constant', Variable(s)], [1, 1]])

        def make_poly(child):
            if isinstance(child.value, str):
                child.value = make_primitive_polynomial(child.value)
                return child
            else:
                return child

        def collapse(current_node):
            if current_node.has_children():
                left = make_poly(current_node.left)
                right = make_poly(current_node.right)
                current_node.value = decide_operation(left.value, right.value, current_node.value)
            else:
                current_node = make_poly(current_node)

        dfs(node, collapse)
        return node.value

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            # First check if they have the same term matrix structure
            if self.term_matrix == other.term_matrix:
                return True
            
            # If not, check if they represent the same mathematical polynomial
            # by normalizing both polynomials (cleaning and ordering) before comparison
            self_copy = self.copy()
            other_copy = other.copy()
            
            # Clean both polynomials to remove zero-coefficient variables
            self_copy.term_matrix = Polynomial.clean(self_copy.term_matrix)
            other_copy.term_matrix = Polynomial.clean(other_copy.term_matrix)
            
            # Apply consistent ordering to both polynomials for comparison
            if len(self_copy.term_matrix) > 1:
                self_copy.term_matrix = order(self_copy.term_matrix)
            if len(other_copy.term_matrix) > 1:
                other_copy.term_matrix = order(other_copy.term_matrix)
            
            return self_copy.term_matrix == other_copy.term_matrix
        elif other == 0:
            # Check if this is the zero polynomial (all coefficients are zero)
            if len(self.term_matrix) < 2:
                return True
            # Check if all terms have zero coefficients
            return all(term[0] == 0 for term in self.term_matrix[1:])
        elif other == 1:
            # Check if this is the constant polynomial 1
            cleaned = Polynomial.clean(self.term_matrix)
            return cleaned == [['constant'], [1.0]]
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        a, b = Polynomial.combine_variables(self, other)
        tm = collect_like_terms([a.term_matrix[0]] + a.term_matrix[1:] + b.term_matrix[1:])
        tm = order(tm)  # Apply consistent ordering
        result = Polynomial(tm, self.field_characteristic)
        result._filter_zero_terms()
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        a, b = Polynomial.combine_variables(self, other)
        neg_b = [[-x if i == 0 else x for i, x in enumerate(term)] for term in b.term_matrix[1:]]
        tm = collect_like_terms([a.term_matrix[0]] + a.term_matrix[1:] + neg_b)
        tm = order(tm)  # Apply consistent ordering
        result = Polynomial(tm, self.field_characteristic)
        result._filter_zero_terms()
        return result

    def __rsub__(self, other):
        return Polynomial(other, self.field_characteristic).__sub__(self)

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        a, b = Polynomial.combine_variables(self, other)
        header = a.term_matrix[0]
        terms = []
        for ta in a.term_matrix[1:]:
            for tb in b.term_matrix[1:]:
                coeff = ta[0] * tb[0]
                exps = [ta[i] + tb[i] for i in range(1, len(header))]
                terms.append([coeff] + exps)
        tm = collect_like_terms([header] + terms)
        tm = order(tm)  # Apply consistent ordering
        result = Polynomial(tm, self.field_characteristic)
        result._filter_zero_terms()
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
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
            result = q[0]
        else:
            result = q
        if isinstance(result, Polynomial):
            result._filter_zero_terms()
        elif isinstance(result, list):
            for poly in result:
                if isinstance(poly, Polynomial):
                    poly._filter_zero_terms()
        return result
    def __mod__(self, other):
        """Implements the % operator for polynomials."""
        if not isinstance(other, Polynomial):
            other = Polynomial(other, self.field_characteristic)
        _, r = division_algorithm(self, other)
        r._filter_zero_terms()
        return r
    def __call__(self, *args, **kwargs):
        """Evaluate the polynomial at given variable values."""
        # Map variables to values
        var_list = self.variables
        if args:
            if len(args) != len(var_list):
                raise ValueError(f"Expected {len(var_list)} arguments, got {len(args)}")
            subs = dict(zip(var_list, args))
        else:
            subs = kwargs
        
        # Determine which variables will remain in the result
        remaining_vars = []
        substitutions = {}
        
        for var in var_list:
            if var in subs:
                val = subs[var]
                if isinstance(val, str):
                    # String values represent variable names that should remain
                    remaining_vars.append(val)
                    substitutions[var] = val
                elif isinstance(val, Polynomial):
                    # Polynomial values - if they're simple variables, treat as variable substitution
                    if len(val.variables) == 1 and len(val.term_matrix) == 2 and val.term_matrix[1][0] == 1 and val.term_matrix[1][1] == 1:
                        # This is a simple variable like Polynomial('a')
                        new_var_name = val.variables[0]
                        remaining_vars.append(new_var_name)
                        substitutions[var] = new_var_name
                    else:
                        # More complex polynomial substitution - for now, handle as numeric if it's constant
                        if len(val.variables) == 0:
                            substitutions[var] = val.term_matrix[1][0]
                        else:
                            # Complex polynomial substitution - not fully implemented
                            raise NotImplementedError("Complex polynomial substitution not yet supported")
                else:
                    # Numeric values get substituted
                    substitutions[var] = val
            else:
                # Variables not provided remain in the result
                remaining_vars.append(var)
        
        # Build the result polynomial
        if not remaining_vars:
            # All variables substituted with numeric values
            result_value = 0.0
            for term in self.term_matrix[1:]:
                coeff = term[0]
                prod = coeff
                for i, var in enumerate(var_list):
                    exp = term[i+1]
                    if exp != 0:
                        val = substitutions.get(var, 0)
                        if not isinstance(val, str):
                            prod *= val ** exp
                result_value += prod
            # Handle complex results
            if isinstance(result_value, complex):
                return Polynomial([['constant'], [result_value]], self.field_characteristic)
            else:
                return Polynomial([['constant'], [float(result_value)]], self.field_characteristic)
        else:
            # Some variables remain - construct a new polynomial
            header = ['constant'] + remaining_vars
            new_terms = []
            
            for term in self.term_matrix[1:]:
                coeff = term[0]
                new_term = [coeff]
                
                # Calculate coefficient after substituting numeric values
                for i, var in enumerate(var_list):
                    exp = term[i+1]
                    if exp != 0 and var in substitutions:
                        val = substitutions[var]
                        if not isinstance(val, str):
                            coeff *= val ** exp
                
                new_term[0] = coeff
                
                # Add exponents for remaining variables
                for rem_var in remaining_vars:
                    if rem_var in var_list:
                        # Original variable
                        var_idx = var_list.index(rem_var)
                        new_term.append(term[var_idx + 1])
                    else:
                        # New variable from string substitution
                        for i, orig_var in enumerate(var_list):
                            if orig_var in substitutions and substitutions[orig_var] == rem_var:
                                new_term.append(term[i + 1])
                                break
                        else:
                            new_term.append(0)
                
                new_terms.append(new_term)
            
            result_tm = [header] + new_terms
            result = Polynomial(result_tm, self.field_characteristic)
            result._filter_zero_terms()
            return result

    def __rtruediv__(self, other):
        return Polynomial(other, self.field_characteristic).__truediv__(self)

    def __pow__(self, n):
        # Accept int, float (if integer-valued), or Polynomial (if constant integer)
        if isinstance(n, Polynomial):
            # Only allow constant polynomials as exponents
            if n.number_of_variables == 0 and len(n.term_matrix) == 2:
                n_val = n.term_matrix[1][0]
            else:
                raise ValueError("Exponent must be a constant integer or integer-valued float, not a non-constant Polynomial.")
        else:
            n_val = n
        # Accept float if it is integer-valued
        if isinstance(n_val, float):
            if n_val.is_integer():
                n_val = int(n_val)
            else:
                raise ValueError("Exponent must be integer-valued, got float {}".format(n_val))
        if not isinstance(n_val, int):
            raise ValueError("Exponent must be an integer, got {}".format(type(n_val)))
        if n_val < 0:
            raise ValueError("Negative exponents not supported.")
        result = Polynomial(1, self.field_characteristic)
        for _ in range(n_val):
            result *= self
        return result

    def __repr__(self):
        return f"Polynomial({self.term_matrix})"

    def __str__(self):
        if len(self.term_matrix) == 1:
            return "0"
        res = ""
        for term in self.term_matrix[1:]:
            coeff = term[0]
            term_str = ""
            
            # Check if this is a constant term (all variable powers are 0)
            is_constant_term = all(term[i] == 0 for i in range(1, len(term)))
            
            if is_constant_term:
                # For constant terms, always show the coefficient
                term_str = str(coeff)
            else:
                # For variable terms, handle coefficient display
                if coeff == 1:
                    pass  # Don't show coefficient of 1
                elif coeff == -1:
                    term_str = "-"
                else:
                    term_str = str(coeff)
            
            # Handle variables
            for i in range(1, len(self.term_matrix[0])):
                if term[i] != 0:
                    term_str += self.term_matrix[0][i]
                    if term[i] != 1:
                        term_str += f"^{term[i]}"
            
            res += term_str + " + "
        
        if res.endswith(" + "):
            res = res[:-3]
        res = res.replace('+ -', '- ')
        return res

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def LT(self):
        if len(self.term_matrix) == 1:
            return Polynomial(0, self.field_characteristic)
        self.term_matrix = order(self.term_matrix)
        res = [[], []]
        for variable in self.term_matrix[0]:
            res[0].append(variable)
        for coefficient in self.term_matrix[1]:
            res[1].append(coefficient)
        res = Polynomial.clean(res)
        return Polynomial(res, self.field_characteristic)

    def LM(self):
        res = self.LT()
        if res != 0:
            res.term_matrix[1][0] /= res.term_matrix[1][0]
        return res

    def terms(self):
        for term in self.term_matrix[1:]:
            yield Polynomial(Polynomial.clean([self.term_matrix[0], term]), self.field_characteristic)

    def __iter__(self):
        for term in self.term_matrix[1:]:
            yield Polynomial([self.term_matrix[0], term], self.field_characteristic)

    def mod_char(self, tm):
        if self.field_characteristic == 0:
            return tm
        header = tm[0]
        new_terms = []
        for term in tm[1:]:
            new_terms.append([term[0] % self.field_characteristic] + term[1:])
        # Filter zero terms after modular reduction
        nonzero_terms = [term for term in new_terms if not (isinstance(term[0], (int, float, complex)) and term[0] == 0 and all((isinstance(x, (int, float, complex)) and x == 0) for x in term[1:]))]
        if nonzero_terms:
            return [header] + nonzero_terms
        else:
            return [header, [0.0] + [0]*(len(header)-1)]

    def degree(self):
        if len(self.term_matrix[0]) == 1:
            return 0
        t = self.copy()
        t.term_matrix = graded_order(t.term_matrix)
        return sum(t.term_matrix[1][1:])

    @property
    def variables(self):
        return [variable for variable in self.term_matrix[0] if variable != 'constant']

    @property
    def number_of_variables(self):
        return len(self.variables)

    @staticmethod
    def clean(term_matrix):
        res = term_matrix
        j = 0
        while j < len(term_matrix[0]):
            for i in range(1, len(res[0])):
                all_zero = True
                for term in res[1:]:
                    if term[i] != 0:
                        all_zero = False
                if all_zero:
                    if i < len(res[0]) - 1:
                        res = [x[0:i] + x[i + 1:] for x in res]
                    else:
                        res = [x[0:i] for x in res]
                    break
            j += 1
        return res

    @staticmethod
    def combine_variables(a, b):
        a = a.copy()
        b = b.copy()
        var_set = set(a.term_matrix[0]).union(set(b.term_matrix[0]))
        str_vars = sorted([v for v in var_set if isinstance(v, str)])
        nonstr_vars = [v for v in var_set if not isinstance(v, str)]
        res = [str_vars + nonstr_vars]
        for var in res[0]:
            if var not in a.term_matrix[0]:
                a.term_matrix[0].append(var)
                for term in a.term_matrix[1:]:
                    term.append(0)
            if var not in b.term_matrix[0]:
                b.term_matrix[0].append(var)
                for term in b.term_matrix[1:]:
                    term.append(0)
        a.term_matrix = order(a.term_matrix)
        b.term_matrix = order(b.term_matrix)
        return a, b

    def isolate(self, variable):
        poly = self.copy()
        if variable in poly.variables:
            i = poly.term_matrix[0].index(variable)
        else:
            return Polynomial([['constant', str(variable)]], self.field_characteristic)
        if i != len(poly.variables):
            remaining_vars = poly.term_matrix[0][:i] + poly.term_matrix[0][i + 1:]
        else:
            remaining_vars = poly.term_matrix[0][:i]
        header = ['constant', str(variable)]
        res_terms = [header]  # Start with just the header, don't use Polynomial constructor
        for term in poly.term_matrix[1:]:
            term_copy = term.copy()  # Make a copy so we don't modify the original
            variable_power = term_copy.pop(i)
            remaining_term = term_copy
            coeff_poly = Polynomial(Polynomial.clean([[str(v) for v in remaining_vars], remaining_term]))
            res_terms.append([coeff_poly, variable_power])
        
        # Manually collect like terms for polynomial coefficients
        # Group terms by their power (variable_power)
        power_groups = {}
        for term in res_terms[1:]:  # Skip header
            coeff_poly, power = term
            if power not in power_groups:
                power_groups[power] = []
            power_groups[power].append(coeff_poly)
        
        # Sum polynomial coefficients for each power
        collected_terms = [header]
        for power in sorted(power_groups.keys()):  # Sort by ascending power
            coeff_list = power_groups[power]
            if len(coeff_list) == 1:
                collected_terms.append([coeff_list[0], power])
            else:
                # Sum the polynomial coefficients
                total_coeff = coeff_list[0]
                for coeff in coeff_list[1:]:
                    total_coeff = total_coeff + coeff
                collected_terms.append([total_coeff, power])
        
        # Create the result polynomial manually to avoid automatic zero-term addition
        res = Polynomial.__new__(Polynomial)  # Create without calling __init__
        res.field_characteristic = poly.field_characteristic
        res.term_matrix = collected_terms
        # Don't apply ordering since we already sorted manually and the structure is non-standard
        if len(res.term_matrix) == 1:
            res.term_matrix = [header, [0.0, 0]]
        return res

    def derivative(self, var=None):
        res = self.copy()
        if var is None:
            if len(res.term_matrix[0]) == 1:
                return Polynomial([['constant'], [0.0]], self.field_characteristic)
            var = res.term_matrix[0][1]
        if var not in res.term_matrix[0]:
            return Polynomial([['constant'], [0.0]], self.field_characteristic)
        variable_index = res.term_matrix[0].index(var)
        for i in range(1, len(res.term_matrix)):
            if res.term_matrix[i][variable_index] != 0:
                res.term_matrix[i][0] *= res.term_matrix[i][variable_index]
                res.term_matrix[i][variable_index] -= 1
            else:
                for j in range(len(res.term_matrix[i])):
                    res.term_matrix[i][j] = 0
        header = self.term_matrix[0] if isinstance(self.term_matrix[0][0], str) else None
        collected = collect_like_terms(res.term_matrix, preserve_header=True)
        if header and collected and (not isinstance(collected[0][0], str)):
            res.term_matrix = [header] + collected
        else:
            res.term_matrix = collected
        res.term_matrix = order(res.term_matrix)  # Apply consistent ordering
        return res

    @property
    def grad(self):
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
                        res.append(Polynomial([['constant'], [float(val)]]))
                return res
            def __repr__(self):
                res = ''
                for term in self:
                    res += str(term)
                return res
            def __str__(self):
                return self.__repr__()
        g = Gradient()
        g.variables_in_order = tuple(self.term_matrix[0][1:])
        for i in range(1, len(self.term_matrix[0])):
            g.append(self.derivative(self.term_matrix[0][i]))
        return g

    @property
    def hessian(self):
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
                            # If it's still a polynomial after evaluation, try to evaluate it numerically
                            if len(val.term_matrix) == 2 and val.term_matrix[0] == ['constant'] and isinstance(val.term_matrix[1][0], (int, float)):
                                row.append(val.term_matrix[1][0])
                            else:
                                row.append(val)
                        else:
                            row.append(float(val))
                    res.append(row)
                return res
        h = Hessian()
        h.variables_in_order = tuple(self.term_matrix[0][1:])
        number_of_variables = len(self.variables)
        for i in range(number_of_variables):
            h.append([])
            for j in range(number_of_variables):
                var1 = self.term_matrix[0][i + 1]
                var2 = self.term_matrix[0][j + 1]
                h[i].append(self.derivative(var1).derivative(var2))
        return h

    def solve(self):
        return solve(self)

    def __init__(self, poly, char=0):
        self.field_characteristic = char
        # Always construct with header for constants/zeros
        if poly == 0 or poly == [['constant']] or poly == [['constant'], [0]] or poly == [['constant'], [0.0]]:
            self.term_matrix = [['constant'], [0.0]]
        elif isinstance(poly, int) and poly != 0:
            self.term_matrix = [['constant'], [float(poly)]]
        elif isinstance(poly, float) and poly != 0:
            self.term_matrix = [['constant'], [float(poly)]]
        elif isinstance(poly, complex) and poly != 0:
            self.term_matrix = [['constant'], [complex(poly)]]
        elif isinstance(poly, (Integer, Rational, np.int32)) and poly != 0:
            self.term_matrix = [['constant'], [float(poly)]]
        elif isinstance(poly, list):
            # Ensure all variable names in header are strings
            if poly and isinstance(poly[0], list):
                header = poly[0]
                header = ['constant'] + [str(v) for v in header[1:]]
                self.term_matrix = [header] + poly[1:]
            else:
                # If it's a list of numbers, treat as constant vector
                if all(isinstance(x, (int, float, complex)) for x in poly):
                    self.term_matrix = [['constant'], [float(poly[0])]]
                else:
                    self.term_matrix = poly
        elif isinstance(poly, str):
            poly = construct_expression_tree(order_prefix(parse_function(poly)))
            self.term_matrix = Polynomial.make_polynomial_from_tree(poly).term_matrix
        elif isinstance(poly, Variable):
            self.term_matrix = Polynomial(poly.label).term_matrix
        else:
            raise InputError
        # Always normalize: if header missing, add it
        if not (self.term_matrix and isinstance(self.term_matrix[0][0], str)):
            self.term_matrix = [['constant']] + self.term_matrix
        # If only header row, add zero row
        if len(self.term_matrix) == 1:
            self.term_matrix = [self.term_matrix[0], [0.0]]
        self.term_matrix = self.mod_char(self.term_matrix)
        self._filter_zero_terms()

    
def divides(a, b):
    a, b = Polynomial.combine_variables(a, b)
    a_tm = a.term_matrix
    b_tm = b.term_matrix
    if len(a_tm) < 2 or len(b_tm) < 2:
        return False
    a_term = a_tm[1]
    b_term = b_tm[1]
    max_len = max(len(a_term), len(b_term))
    for i in range(1, max_len):
        a_exp = a_term[i] if i < len(a_term) else 0
        b_exp = b_term[i] if i < len(b_term) else 0
        if a_exp > b_exp:
            return False
    return True

def monomial_divide(a, b):
    a, b = Polynomial.combine_variables(a, b)
    res = a.copy()
    if len(b.term_matrix) < 2 or all(x == 0 for x in b.term_matrix[1]):
        return Polynomial([['constant'], [0.0]], a.field_characteristic)
    if len(a.term_matrix) < 2:
        return Polynomial([['constant'], [0.0]], a.field_characteristic)
    header_len = len(res.term_matrix[0])
    a_term = list(res.term_matrix[1]) + [0] * (header_len - len(res.term_matrix[1]))
    b_term = list(b.term_matrix[1]) + [0] * (header_len - len(b.term_matrix[1]))
    if b_term[0] == 0:
        return Polynomial([['constant'], [0.0]], a.field_characteristic)
    a_term[0] = a_term[0] / b_term[0]
    for i in range(1, header_len):
        a_term[i] -= b_term[i]
    res.term_matrix[1] = a_term
    return res

def division_algorithm(input_poly, *others):
    a = []
    for i in range(len(others)):
        a.append(Polynomial([['constant'], [0.0]], input_poly.field_characteristic))
    p = input_poly.copy()
    r = Polynomial([['constant'], [0.0]], input_poly.field_characteristic)
    max_steps = 1000
    steps = 0
    if p == Polynomial(0):
        return a, r
    while p != Polynomial(0):
        if steps > max_steps:
            print("division_algorithm: exceeded max steps, possible infinite loop. p=", p)
            break
        prev_p = p.copy()
        i = 0
        division_occurred = False
        while i < len(others) and not division_occurred:
            if divides(others[i], p):
                a[i] += monomial_divide(p.LT(), others[i].LT())
                p -= monomial_divide(p.LT(), others[i].LT()) * others[i]
                division_occurred = True
            else:
                i += 1
        if not division_occurred:
            p_LT = p.LT()
            r += p_LT
            p -= p.LT()
        if p == prev_p:
            print("division_algorithm: no progress, breaking to avoid infinite loop. p=", p)
            break
        steps += 1
    for poly in a:
        poly.term_matrix = input_poly.mod_char(poly.term_matrix)
        if poly.term_matrix and isinstance(poly.term_matrix[0][0], str):
            header = poly.term_matrix[0]
            # Handle complex coefficients
            poly.term_matrix = [header] + [[term[0] if isinstance(term[0], complex) else float(term[0])] + term[1:] for term in poly.term_matrix[1:]]
    if r.term_matrix and isinstance(r.term_matrix[0][0], str):
        header = r.term_matrix[0]
        # Handle complex coefficients
        r.term_matrix = [header] + [[term[0] if isinstance(term[0], complex) else float(term[0])] + term[1:] for term in r.term_matrix[1:]]
    r.term_matrix = input_poly.mod_char(r.term_matrix)
    return a, r

def division_string(p, *others):
    a, r = division_algorithm(p, *others)
    res = str(p) + ' = '
    for i in range(len(a)):
        res += '(' + str(a[i]) + ')' + '*' + '(' + str(others[i]) + ')' + ' + '
    if res.endswith(" + "):
        res = res[:-3]
    res += ' + (remainder:) ' + str(r)
    return res

def gcd(a, b):
    a = a.copy()
    b = b.copy()
    
    # Special case for monomial polynomials (single term each)
    if (len(a.term_matrix) == 2 and len(b.term_matrix) == 2 and 
        len([t for t in a.term_matrix[1:] if t[0] != 0]) == 1 and
        len([t for t in b.term_matrix[1:] if t[0] != 0]) == 1):
        
        # Both are monomials, compute GCD directly
        a_combined, b_combined = Polynomial.combine_variables(a, b)
        
        # GCD of coefficients
        import math
        coeff_gcd = math.gcd(int(abs(a_combined.term_matrix[1][0])), int(abs(b_combined.term_matrix[1][0])))
        
        # For each variable, take minimum exponent
        result_term = [float(coeff_gcd)]
        for i in range(1, len(a_combined.term_matrix[0])):
            a_exp = a_combined.term_matrix[1][i] if i < len(a_combined.term_matrix[1]) else 0
            b_exp = b_combined.term_matrix[1][i] if i < len(b_combined.term_matrix[1]) else 0
            result_term.append(min(a_exp, b_exp))
        
        result_tm = [a_combined.term_matrix[0], result_term]
        result = Polynomial(result_tm, a.field_characteristic)
        result._filter_zero_terms()
        return result
    
    # Fallback to original implementation for non-monomials
    if len(set(a.variables).union(set(b.variables))) <= 1:
        g = gcd_singlevariate(a, b)
        if len(g.term_matrix) < 2:
            g = Polynomial([['constant'], [0.0]], a.field_characteristic)
        elif len(g.term_matrix) == 2 and (len(g.term_matrix[1]) == 1 or all(x == 0 for x in g.term_matrix[1][1:])):
            g = Polynomial([['constant'], [float(g.term_matrix[1][0])]], a.field_characteristic)
        return g
    if len(a.term_matrix) > 2 or len(b.term_matrix) > 2:
        raise NotImplemented
    if len(a.term_matrix) < 2 or len(b.term_matrix) < 2:
        return Polynomial([['constant'], [0.0]])
    res = gcd_singlevariate(Polynomial(a.term_matrix[1][0]), Polynomial(b.term_matrix[1][0]))
    for variable in set(a.variables).union(set(b.variables)):
        isolated_a = a.isolate(variable)
        isolated_b = b.isolate(variable)
        if len(isolated_a.term_matrix) < 2 or len(isolated_b.term_matrix) < 2:
            continue
        if len(isolated_a.term_matrix[1]) > 1 and len(isolated_b.term_matrix[1]) > 1:
            if variable in isolated_a.variables and variable in isolated_b.variables:
                res *= Polynomial(variable) ** min(isolated_a.term_matrix[1][1], isolated_b.term_matrix[1][1])
    if len(res.term_matrix) < 2:
        res = Polynomial([['constant'], [0.0]], a.field_characteristic)
    elif len(res.term_matrix) == 2 and (len(res.term_matrix[1]) == 1 or all(x == 0 for x in res.term_matrix[1][1:])):
        res = Polynomial([['constant'], [float(res.term_matrix[1][0])]], a.field_characteristic)
    return res

def gcd_singlevariate(a, b):
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
                print("gcd_singlevariate: exceeded max steps, possible infinite loop. a=", a, "b=", b, "r=", r)
                break
            a = b
            b = r
            if b == Polynomial([['constant']]) or (hasattr(b, 'term_matrix') and len(b.term_matrix) < 2):
                return a
            r = a % b
            steps += 1
        return b
    else:
        return gcd(b, a)

def lcm(a, b):
    l = a * b / gcd(a, b)
    if isinstance(l, Polynomial):
        if len(l.term_matrix) < 2:
            l = Polynomial([['constant'], [0.0]], a.field_characteristic)
        elif len(l.term_matrix) == 2 and (len(l.term_matrix[1]) == 1 or all(x == 0 for x in l.term_matrix[1][1:])):
            l = Polynomial([['constant'], [float(l.term_matrix[1][0])]], a.field_characteristic)
    return l
