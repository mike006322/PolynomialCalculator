"""
Input a string that represents a polynomial equal to 0
Output coded polynomial as [[" ", variable1, variable2...], [coefficient, exponent1, exponent2...],...]
Matrix will be as follows:

(blank)    , varable1 label, variable2 label,...
coefficient, exponent1     , exponent2
coefficient, exponent1     , exponent2
  .
  .
  .
"""


def find_vars(s):
    variables = set()
    possible_variables = {'x', 'y', 'z', 't', 'u', 'v', 'r'}
    for term in s:
        for t in range(len(term)):
            if term[t] in possible_variables:
                if t < len(term) - 1:
                    if term[t+1].isnumeric():
                        variables.add(term[t]+term[t+1])
                    else:
                        variables.add(term[t])
                else:
                    variables.add(term[t])
    return variables


def add_var(var, s, term_matrix):
    # if var is present, adds var to the list of variables
    for term in s:
        if var in term:
            if var not in term_matrix[0]:
                term_matrix[0].append(var)


def add_exp(k, s, term_matrix):
    # replaces 0 in kth entry of term in term_matrix with exponent
    var = term_matrix[0][k]
    for j in range(len(s)):
        term = s[j]
        if var in term:
            i = term.index(var)
            var_len = len(var)
            if i < len(term) - var_len:
                if term[i+var_len] == '^':
                    term_matrix[j+1][k] = int(term[i+1+var_len])
                else:
                    term_matrix[j+1][k] = 1
            else:
                term_matrix[j+1][k] = 1


def add_coeff(s, term_matrix):
    for j in range(len(s)):
        t = s[j]
        coeff = ''
        if t[0] == '-':
            coeff += '-'
            t = t[1:]
            i = 0
            while t[i].isnumeric():
                coeff += t[i]
                i += 1
                if i == len(s[j]) - 1: # minus one because we removed the '-'
                    break
        elif t[0].isnumeric == 'False':
            coeff = '1'
        else:
            i = 0
            while t[i].isnumeric():
                coeff += t[i]
                i += 1
                if i == len(s[j]):
                    break
        if coeff == '-' or coeff == '':
            coeff += '1'
        term_matrix[j+1][0] = float(coeff)


def parse_poly(s_input):
    s = s_input.replace(" ", "").replace("-", "+-").replace("*", "").replace("++", "+").lower().split("+")
    term_matrix = [[" "]]
    num_terms = len(s)
    for _ in range(num_terms):
        term_matrix.append([])
    num_var = 0
    variables = find_vars(s)
    for v in variables:
        add_var(v, s, term_matrix)
        num_var += 1
    for i in range(1, len(term_matrix)):
        term_matrix[i].append('coeff')
    add_coeff(s, term_matrix)
    for i in range(1, len(term_matrix)):
        for _ in range(num_var):
            term_matrix[i].append(0)
    for i in range(1, num_var+1):
        add_exp(i, s, term_matrix)

    return term_matrix


if __name__ == "__main__":
    pass
