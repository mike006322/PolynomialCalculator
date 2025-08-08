from typing import List, Union, Dict, Tuple, Optional, TypeAlias, cast

# Type aliases for readability
Coef: TypeAlias = Union[int, float, complex]
Term = List[Coef]
HeaderRow = List[Union[str, int, float, complex]]
TermMatrix = List[HeaderRow | Term]
Key: TypeAlias = Tuple[Union[int, float, complex], ...]


def collect_like_terms(term_matrix: TermMatrix, preserve_header: bool = True) -> TermMatrix:
    """
    input is polynomial in form of term_matrix from poly_parser.py
    output is another term_matrix with terms collected
    term_matrix = [[" ", variable1, variable2...], [coefficient, exponent1, exponent2...],...]
    preserve_header: if True, keep the header row if present; if False, always return headerless matrix
    """
    if not term_matrix:
        return []

    # Detect and preserve header row if present
    header: Optional[HeaderRow] = None
    data: List[Term]
    if isinstance(term_matrix[0][0], str):
        header = cast(HeaderRow, term_matrix[0])
        data = cast(List[Term], term_matrix[1:])
    else:
        data = cast(List[Term], term_matrix)

    # Group terms by their exponents (all columns except the first)
    import numbers

    term_dict: Dict[Key, Coef] = {}
    for term in data:
        coef = term[0]
        key = tuple(term[1:])
        if key not in term_dict:
            term_dict[key] = coef
        else:
            # If both are numbers, sum as numbers; else, use __add__
            if isinstance(term_dict[key], numbers.Number) and isinstance(coef, numbers.Number):
                term_dict[key] = term_dict[key] + coef
            else:
                term_dict[key] = term_dict[key] + coef

    # Remove zero-coefficient terms (only include terms where coef is a number and not zero)
    collected: TermMatrix = []
    for exps, coef in term_dict.items():
        # Debug: catch accidental list or non-numeric coefficients
        assert not isinstance(coef, list), f"Coefficient is a list: {coef} (exps={exps})"
        if isinstance(coef, numbers.Number):
            if coef != 0:
                collected.append([coef] + list(exps))
        else:
            # Optionally, skip or handle non-numeric coefficients
            pass

    if not collected:
        return [["constant"]]

    # Remove extra variables (columns where all exponents are zero) only if no header
    if not (preserve_header and header):
        num_vars = len(collected[0]) - 1
        to_remove: List[int] = []
        for i in range(num_vars):
            if all(term[i + 1] == 0 for term in collected):
                to_remove.append(i + 1)
        # Remove from right to left to avoid index shift
        for idx in reversed(to_remove):
            for term in collected:
                del term[idx]

    if preserve_header and header:
        return [header] + collected

    return collected


if __name__ == '__main__':
    pass
