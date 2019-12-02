"""
Classic method for optimizing an objective function with a set of linear constraints
"""

"""
https://github.com/jdmoore7/simplex_algorithm/blob/master/simplex.py
Read-me:
Call functions in this order:
    problem = gen_matrix(v,c)
    constrain(problem, string)
    obj(problem, string)
    maxz(problem)
gen_matrix() produces a matrix to be given constraints and an objective function to maximize or minimize.
    It takes var (variable number) and cons (constraint number) as parameters.
    gen_matrix(2,3) will create a 4x7 matrix by design.
constrain() constrains the problem. It takes the problem as the first argument and a string as the second. The string should be
    entered in the form of 1,2,G,10 meaning 1(x1) + 2(x2) >= 10.
    Use 'L' for <= instead of 'G'
Use obj() only after entering all constraints, in the form of 1,2,0 meaning 1(x1) +2(x2) +0
    The final term is always reserved for a constant and 0 cannot be omitted.
Use maxz() to solve a maximization LP problem. Use minz() to solve a minimization problem.
Disclosure -- pivot() function, subcomponent of maxz() and minz(), has a couple bugs. So far, these have only occurred when
    minz() has been called.
    # I think this is because everything is naively multiplied by -1 to get min
"""

import numpy as np


def gen_matrix(var, cons):
    """
    generates an empty matrix with adequate size for variables and constraints.
    """
    tab = np.zeros((cons + 1, var + cons + 2))
    return tab


def next_round_r(table):
    """
    checks the furthest right column for negative values ABOVE the last row.
    If negative values exist, another pivot is required.
    """
    m = min(table[:-1, -1])
    if m >= 0:
        return False
    else:
        return True


def next_round(table):
    """
    checks that the bottom row, excluding the final column,
    for negative values. If negative values exist, another pivot is required.
    """
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m >= 0:
        return False
    else:
        return True


def find_neg_r(table):
    """
    Similar to next_round_r function, but returns row index of negative element in furthest right column
    """
    # lc = number of columns, lr = number of rows
    lc = len(table[0, :])
    # search every row (excluding last row) in final column for min value
    m = min(table[:-1, lc - 1])
    if m <= 0:
        # n = row index of m location
        n = np.where(table[:-1, lc - 1] == m)[0][0]
    else:
        n = None
    return n


def find_neg(table):
    """
    returns column index of negative element in bottom row
    """
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m <= 0:
        # n = row index for m
        n = np.where(table[lr - 1, :-1] == m)[0][0]
    else:
        n = None
    return n


def loc_piv_r(table):
    """
    locates pivot element in tableu to remove the negative element from the furthest right column.
    """
    total = []
    # r = row index of negative entry
    r = find_neg_r(table)
    # finds all elements in row, r, excluding final column
    row = table[r, :-1]
    # finds minimum value in row (excluding the last column)
    m = min(row)
    # c = column index for minimum entry in row
    c = np.where(row == m)[0][0]
    # all elements in column
    col = table[:-1, c]
    # need to go through this column to find smallest positive ratio
    for i, b in zip(col, table[:-1, -1]):
        # i cannot equal 0 and b/i must be positive.
        if i ** 2 > 0 and b / i > 0:
            total.append(b / i)
        else:
            # placeholder for elements that did not satisfy the above requirements.
            # Otherwise, our index number would be faulty.
            total.append(0)
    element = max(total)
    for t in total:
        if 0 < t < element:
            element = t
        else:
            continue

    index = total.index(element)
    return [index, c]


def loc_piv(table):
    """
    similar process, returns a specific array element to be pivoted on.
    """
    if next_round(table):
        total = []
        n = find_neg(table)
        for i, b in zip(table[:-1, n], table[:-1, -1]):
            if i ** 2 > 0 and b / i > 0:
                total.append(b / i)
            else:
                # placeholder for elements that did not satisfy the above requirements.
                # Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if 0 < t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index, n]


def parse(eq):
    """
    returns a list of numbers to be arranged in tableu
    "L" is "less than or equal to"
    "G" is "greater than or equal to"
    ‘1,3,L,5’ -> 1(x1) + 3(x2) ≤ 5
    """
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i) * -1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq


def convert_to_min(table):
    """
    change the table to a minimuization problem by multiplying the elements of last row by -1
    """
    table[-1, :-2] = [-1 * i for i in table[-1, :-2]]
    table[-1, -1] = -1 * table[-1, -1]
    return table


def gen_var(table):
    """
    generates x1,x2,...xn for the varying number of variables.
    """
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    v = []
    for i in range(var):
        v.append('x' + str(i + 1))
    return v


def pivot(row, col, table):
    """
    pivots the tableau such that negative elements are purged from the last row and last column
    """
    # number of rows
    lr = len(table[:, 0])
    # number of columns
    lc = len(table[0, :])
    t = np.zeros((lr, lc))
    pr = table[row, :]
    if table[row, col] ** 2 > 0:  # new
        e = 1 / table[row, col]
        r = pr * e
        for i in range(len(table[:, col])):
            k = table[i, :]
            c = table[i, col]
            if list(k) == list(pr):
                continue
            else:
                t[i, :] = list(k - r * c)
        t[row, :] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')


def is_room_for_constraint(table):
    """
    checks if there is room in the matrix to add another constraint
    """
    lr = len(table[:, 0])
    # want to know IF at least 2 rows of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j ** 2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There are at least 2 rows with all zero elements if the following is true
    if len(empty) > 1:
        return True
    else:
        return False


def add_constraint(table, eq):
    if is_room_for_constraint(table):
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - lr - 1
        # set up counter to iterate through the total length of rows
        j = 0
        while j < lr:
            # Iterate by row
            row_check = table[j, :]
            # total will be sum of entries in row
            total = 0
            # Find first row with all 0 entries
            for i in row_check:
                total += float(i ** 2)
            if total == 0:
                # We've found the first row with all zero entries
                row = row_check
                break
            j += 1

        eq = parse(eq)
        i = 0
        # iterate through all terms in the constraint function, excluding the last
        while i < len(eq) - 1:
            # assign row values according to the equation
            row[i] = eq[i]
            i += 1
        # row[len(eq)-1] = 1
        row[-1] = eq[-1]

        # add slack variable according to location in tableau.
        row[var + j] = 1
    else:
        print('Cannot add another constraint.')


def is_room_for_objective(table):
    lr = len(table[:, 0])
    # want to know IF exactly one row of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j ** 2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There is exactly one row with all zero elements if the following is true
    if len(empty) == 1:
        return True
    else:
        return False


def add_obj(table, eq):
    if is_room_for_objective(table) == True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:, 0])
        row = table[lr - 1, :]
        i = 0
        # iterate through all terms in the constraint function, excluding the last
        while i < len(eq) - 1:
            # assign row values according to the equation
            row[i] = eq[i] * -1
            i += 1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')


def simplex_method(table, output='summary', min=None):
    """
    solves maximization problem for optimal solution, returns dictionary w/ keys x1,x2...xn and max.
    """
    if min:
        table = convert_to_min(table)

    while next_round_r(table):
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table):
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)


    number_of_columns = len(table[0, :])
    number_of_rows = len(table[:, 0])
    number_of_variables = number_of_columns - number_of_rows - 1
    i = 0
    val = {}
    for i in range(number_of_variables):
        column = table[:, i]
        sum_of_column = sum(column)
        max_of_column = max(column)
        if float(sum_of_column) == float(max_of_column):
            loc = np.where(column == max_of_column)[0][0]
            val[gen_var(table)[i]] = table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1, -1]
    for k, v in val.items():
        val[k] = round(v, 6)
    if output == 'table':
        return table
    else:
        return val


if __name__ == "__main__":
    m = gen_matrix(2, 2)
    print(m)
    add_constraint(m, '2,-1,G,10')
    add_constraint(m, '1,1,L,20')
    add_obj(m, '5,10,0')
    print(m)
    print(simplex_method(m))

    m = gen_matrix(2, 4)
    add_constraint(m, '2,5,G,30')
    add_constraint(m, '-3,5,G,5')
    add_constraint(m, '8,3,L,85')
    add_constraint(m, '-9,7,L,42')
    add_obj(m, '2,7,0')
    print(simplex_method(m))
