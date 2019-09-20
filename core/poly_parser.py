from numbers import *

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


"""
Expression Tree
Node attributes:
string representing a binary operation or and indicator of variable/number
list with two children or variable or number
e.g. ((2+x)*y)**5+13

          +
        /   \
      **     13
    /    \   
    *     5  
  /   \   
  +    y  
/   \  
2   x  

To make a polynomial do a depth first traversal of the tree.

To make the tree: make a list of the operations from first executed to last, PEMDAS,
then make tree with this list in reverse order.

"""


class InputError(Exception):

    def __init__(self):
        print("Polynomial input needs to be similar to following example: 'x^2+2xy^3+4'")
        print("Alternatively, try a term matrix in form [['constant, 'x', 'y'], [1.0, 2, 0], [2.0, 1, 3], [4.0, 0, 0]]")


def find_corresponding_right_parenthesis(s, i):
    """
    input string, s, and index of left parenthesis, i
    returns index of corresponding right parenthesis
    """
    nesting_level = 0
    for j, char in enumerate(s[i+1:]):
        if char == '(':
            nesting_level += 1
        if char == ')':
            if nesting_level == 0:
                return i + j + 1
            else:
                nesting_level -= 1
    raise InputError


def parse_function(function_string):
    """
    returns the function string but as a list of tuples with variables and numbers labeled
    parenthesis are a list of nested parse function
    [[[('2', Integer), ('+', operation), ('x', variable)]('*', operation)('y', variable)], ('**', Operation), ...]
    """
    function_string = function_string.replace(' ', '')
    single_char_operations = '+-/^'
    res = []
    i = 0
    while i < len(function_string):
        if function_string[i] == '(':
            j = find_corresponding_right_parenthesis(function_string, i)
            res.append(parse_function(function_string[i+1:j]))
            i = j + 1
        elif function_string[i] in single_char_operations:
            res.append((function_string[i], 'operation'))
            i += 1
        elif function_string[i] == '*':
            if function_string[i+1] == '*':
                res.append(('**', 'operation'))
                i += 2
            else:
                res.append(('*', 'operation'))
                i += 1
        elif function_string[i:i+1].isalpha():
            index_size = 0
            if i + 1 + index_size < len(function_string):
                while function_string[i + 1 + index_size].isnumeric():
                    index_size += 1
                    if i + 1 + index_size == len(function_string):
                        break
            res.append((function_string[i+index_size], 'variable'))
            i += 1 + index_size
        elif function_string[i:i+1].isnumeric():
            index_size = 0
            if i + 1 + index_size < len(function_string):
                while function_string[i: i + 2 + index_size].isnumeric():
                    index_size += 1
                    if i + 1 + index_size == len(function_string):
                        break
            res.append((function_string[i+index_size], 'number'))
            i += 1 + index_size
    return res


def order_prefix(token_list):
    """
    puts the operations in prefix order
    2+4*3 -> +2*4,3
    """
    order_parenthesis(token_list)
    res = []
    unpack_token_list(token_list, res)
    return res


def unpack_token_list(token_list, res):
    """
    removes nested lists from token list
    """
    for i in range(len(token_list)):
        if type(token_list[i]) == list:
            unpack_token_list(token_list[i], res)
        else:
            res.append(token_list[i])


def swap_positions(l, index_1, index_2):
    l[index_1], l[index_2] = l[index_2], l[index_1]
    return l


def order_parenthesis(token_list):
    """
    place parenthesis by going in PEMDAS order
    """
    # pre-processing step, if there is any variable adjacent to a number, add a '*'
    for i in range(len(token_list)-1):
        if token_list[i][1] != 'operation' and token_list[i+1][1] != 'operation':
            token_list.insert(i+1, ('*', 'operation'))
    # iterate through the operations in reverse order, given "operand, operator, operand", swap first two elements
    # subtraction and addition
    for i in range(len(token_list)-1):
        if token_list[i][0] == '+' or token_list[i][0] == '-':
            swap_positions(token_list, i, i-1)
    # mult and division
    for i in range(len(token_list)-1):
        if token_list[i][0] == '*' or token_list[i][0] == '/':
            swap_positions(token_list, i, i-1)
    # exponentiation
    for i in range(len(token_list)-1):
        if token_list[i][0] == '**':
            swap_positions(token_list, i, i-1)
    # parenthesis
    for i in range(len(token_list)):
        if type(token_list[i]) == list:
            order_parenthesis(token_list[i])


class ExpressionTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def construct_expression_tree(prefix_ordered_items):
    """
    0. Make first node

    1. insert on left until you reach operand
    2. then backtrack until last operator
    3. fill in the right hand side
    4. back to one
    """
    root = ExpressionTree(prefix_ordered_items[0][0])
    stack = [root]
    for i in range(1, len(prefix_ordered_items)):
        t = stack[-1]
        t_1 = ExpressionTree(prefix_ordered_items[i][0])
        if prefix_ordered_items[i][1] == 'operation':
            if not t.left:
                t.left = t_1
                stack.append(t_1)
            else:
                t.right = t_1
                stack.append(t_1)
        else:
            if not t.left:
                t.left = t_1
            else:
                if not t.right:
                    t.right = t_1
                    stack.pop()
    return root


def find_vars(s):
    variables = set()
    possible_variables = {'x', 'y', 'z', 't', 'u', 'v', 'r'}
    for term in s:
        for t in range(len(term)):
            if term[t] in possible_variables:
                if t < len(term) - 1:
                    i = 1
                    while term[t+i].isnumeric():
                        i += 1
                        if t+i > len(term) - 1:
                            break
                    v = term[t]
                    for j in range(1, i):
                        v += term[t+j]
                    variables.add(v)
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
                    a = 0
                    while term[i+1+a+var_len].isnumeric():
                        a += 1
                        if i+1+a+var_len > len(term) - 1:
                            break
                    term_matrix[j+1][k] = int(term[i+1+var_len: i+1+a+var_len])
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
        term_matrix[j+1][0] = Integer(coeff)


def parse_poly(s_input):
    s = s_input.replace(" ", "").replace("-", "+-").replace("*", "").replace("++", "+").lower().split("+")
    while '' in s:
        s.remove('')
    term_matrix = [['constant']]
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
