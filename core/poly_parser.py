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
    for j, char in enumerate(s[i + 1:]):
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
            res.append(parse_function(function_string[i + 1:j]))
            i = j + 1
        elif function_string[i] in single_char_operations:
            if function_string[i] == '^':
                res.append(('**', 'operation'))
            else:
                res.append((function_string[i], 'operation'))
            i += 1
        elif function_string[i] == '*':
            if function_string[i + 1] == '*':
                res.append(('**', 'operation'))
                i += 2
            else:
                res.append(('*', 'operation'))
                i += 1
        elif function_string[i:i + 1].isalpha():
            index_size = 0
            if i + 1 + index_size < len(function_string):
                while function_string[i + 1 + index_size].isnumeric():
                    index_size += 1
                    if i + 1 + index_size == len(function_string):
                        break
            res.append((function_string[i + index_size], 'variable'))
            i += 1 + index_size
        elif function_string[i:i + 1].isnumeric():
            index_size = 0
            if i + 1 + index_size < len(function_string):
                while function_string[i: i + 2 + index_size].isnumeric():
                    index_size += 1
                    if i + 1 + index_size == len(function_string):
                        break
            if i + 1 + index_size < len(function_string):
                if function_string[i + index_size + 1] == '.':
                    left_of_decimal = index_size
                    right_of_decimal = 0
                    if i + 2 + index_size < len(function_string):
                        while function_string[
                              i + left_of_decimal + 2: i + left_of_decimal + 3 + right_of_decimal].isnumeric():
                            right_of_decimal += 1
                            if i + 1 + left_of_decimal + right_of_decimal == len(function_string):
                                break
                    res.append((function_string[i: i + left_of_decimal + 1 + right_of_decimal], 'number'))
                    i += 2 + left_of_decimal + right_of_decimal
                else:
                    res.append((function_string[i + index_size], 'number'))
                    i += 1 + index_size
            else:
                res.append((function_string[i + index_size], 'number'))
                i += 1 + index_size
        else:
            raise InputError
    return res


def handle_negative_inputs(token_list):
    dont_print_next = False
    token_list_handling_negatives = []
    for i, char in enumerate(token_list):
        if type(char) == list:
            token_list_handling_negatives.append(handle_negative_inputs(char))
            dont_print_next = True
        if char[0] == '-':
            if i == 0:
                # turn -2 into 0-2
                token_list_handling_negatives.append(('0', 'number'))
                token_list_handling_negatives.append(('-', 'operation'))
            else:
                if token_list[i - 1][0] in '(+-*/**^':
                    token_list_handling_negatives.append([('0', 'number'), ('-', 'operation'), token_list[i + 1]])
                    dont_print_next = True
                else:
                    token_list_handling_negatives.append(('-', 'operation'))
        else:
            if dont_print_next:
                dont_print_next = False
            else:
                token_list_handling_negatives.append(char)
    return token_list_handling_negatives


def order_prefix(token_list):
    """
    puts the operations in prefix order
    2+4*3 -> +2*4,3
    """
    token_list = handle_negative_inputs(token_list)
    token_list = add_missing_multiply(token_list)
    # print('add missing *: ', token_list)
    group_operations(token_list)
    # print('group operations: ', token_list)
    order_parenthesis(token_list)
    # print('ordered parenthesis: ', token_list)
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


def add_missing_multiply(token_list):
    """
    pre-processing step, if there is any variable adjacent to a number, add a '*'
    """
    for i in range(len(token_list)):
        if type(token_list[i]) == list:
            token_list[i] = add_missing_multiply(token_list[i])
    res = []
    for i in range(len(token_list) - 1):
        if token_list[i][1] != 'operation' and token_list[i + 1][1] != 'operation':
            res.append(token_list[i])
            res.append(('*', 'operation'))
        else:
            res.append(token_list[i])
    res.append(token_list[-1])
    return res


def group_operations(token_list):
    """
    puts operations into their own parenthesis groups
    """
    # iterate through the operations in reverse order, given "operand, operator, operand", swap first two elements
    res = []
    # parenthesis
    for i in range(len(token_list)):
        if type(token_list[i]) == list:
            res.append(group_operations(token_list[i]))
    # exponentiation
    while ('**', 'operation') in token_list:
        for i in range(len(token_list) - 1):
            if token_list[i][0] == '**':
                token_list[i - 1] = [token_list[i - 1], token_list[i], token_list[i + 1]]
                del token_list[i + 1]
                del token_list[i]
                break
    # mult and division
    while ('*', 'operation') in token_list or ('/', 'operation') in token_list:
        for i in range(len(token_list) - 1):
            if token_list[i][0] == '*' or token_list[i][0] == '/':
                token_list[i - 1] = [token_list[i - 1], token_list[i], token_list[i + 1]]
                del token_list[i + 1]
                del token_list[i]
                break
    # subtraction and addition
    while ('+', 'operation') in token_list or ('-', 'operation') in token_list:
        for i in range(len(token_list) - 1):
            if token_list[i][0] == '+' or token_list[i][0] == '-':
                token_list[i - 1] = [token_list[i - 1], token_list[i], token_list[i + 1]]
                del token_list[i + 1]
                del token_list[i]
                break


def order_parenthesis(token_list):
    """
    place parenthesis by going in PEMDAS order
    """
    # iterate through the operations in reverse order, given "operand, operator, operand", swap first two elements
    # subtraction and addition
    for i in range(len(token_list) - 1):
        if token_list[i][0] == '+' or token_list[i][0] == '-':
            swap_positions(token_list, i, i - 1)
    # mult and division
    for i in range(len(token_list) - 1):
        if token_list[i][0] == '*' or token_list[i][0] == '/':
            swap_positions(token_list, i, i - 1)
    # exponentiation
    for i in range(len(token_list) - 1):
        if token_list[i][0] == '**':
            swap_positions(token_list, i, i - 1)
    # parenthesis
    for i in range(len(token_list)):
        if type(token_list[i]) == list:
            order_parenthesis(token_list[i])


class ExpressionTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def DFSUtil(self, v, visited):
        # Mark the current node as visited
        # and print it
        visited.add(v)
        print(v.value, end=' ')
        # Recur for both children vertices
        for side in (v.left, v.right):
            if side and side not in visited:
                self.DFSUtil(side, visited)

    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self):
        """
        Searches the tree and depth first and prints
        used for debugging
        """
        # Mark all the vertices as not visited
        visited = set()
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(self, visited)


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
        # root.DFS()
        # print()
        t_1 = ExpressionTree(prefix_ordered_items[i][0])
        if prefix_ordered_items[i][1] == 'operation':
            if not t.left:
                t.left = t_1
                stack.append(t_1)
            else:
                j = 2
                while t.right:
                    t = stack[-j]
                    j += 1
                t.right = t_1
                stack.append(t_1)
        else:
            if not t.left:
                t.left = t_1
            else:
                j = 2
                while t.right:
                    t = stack[-j]
                    j += 1
                t.right = t_1
                stack.pop()

    return root


def decide_operation(left, right, operation):
    """
    input operations is as string representing a built-in operation
    """
    if operation == '+':
        return left + right
    if operation == '-':
        return left - right
    if operation == '*':
        return left * right
    if operation == '/':
        return left / right
    if operation == '**':
        return left ** right
    if operation == '^':
        return left ** right


if __name__ == "__main__":
    pass
