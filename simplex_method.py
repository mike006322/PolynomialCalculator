"""
Simplex method/ Linear Programming for optimizing an objective function with a set of linear constraints
https://youtu.be/E94xNYyjTmg
"""

import numpy as np


def has_a_negative(vector):
    for i in range(len(vector)):
        if vector[i] < 0:
            return True
    return False


def find_pivot_column(last_row):
    """
    locate the most negative entry in the last row excluding the last column
    """
    m = 0
    column_index = -1
    for i, entry in enumerate(last_row):
        if entry < 0:
            if entry < m:
                m = entry
                column_index = i
    return column_index


def find_pivot_row(pivot_column, constants):
    """
    divide each constant by it's corresponding positive entry in the pivot column
    if the ratio is negative, skip it
    The pivot row has the smallest ratio
    """
    m = np.inf
    row_index = -1
    for i, entry in enumerate(pivot_column):
        if entry == 0:
            continue
        else:
            ratio = constants[i] / entry
            if ratio > 0:
                if ratio < m:
                    m = ratio
                    row_index = i
    return row_index


def pivot_new(row_index, column_index, table):
    result = table.copy()
    result[row_index] /= table[row_index, column_index]
    for i in range(len(result)):
        if i != row_index:
            result[i] = result[i] - result[row_index] * result[i][column_index]
    return result


def simplex_method(table, output='variable_names'):
    """
    solves maximization problem for optimal solution, returns dictionary w/ keys x1,x2...xn and max.
    """
    while has_a_negative(table[-1, :][:-1]):
        pivot_column_index = find_pivot_column(table[-1, :][:-1])
        pivot_row_index = find_pivot_row(table[:, pivot_column_index], table[:, -1])
        table = pivot_new(pivot_row_index, pivot_column_index, table)

    if output == 'table':
        return table

    number_of_columns = len(table[0, :])
    number_of_rows = len(table[:, 0])
    number_of_variables = number_of_columns - number_of_rows - 1

    if output == 'epsilon':
        epsilon = []
        # epsilon is n by n
        n = int(np.sqrt(number_of_variables // 2))
        # we divide number of variables by 2 because we are reducing them
        # we added variables to unrestrict them
        for i in range(n):
            epsilon.append([])
        for i in range(number_of_variables):
            basic, index = is_column_basic(table[:, i])
            if basic:
                # %2 because we are also reducing the variables
                # this accounts for the modification for unrestricted variables, i.e. not always >=0
                if i % 2 == 0:
                    epsilon[i // 2 % n].append(table[index, -1])
                else:
                    epsilon[(i - 1) // 2 % n][-1] += -1*table[index, -1]
            else:
                if i % 2 == 0:
                    epsilon[i // 2 % n].append(0)
        return epsilon

    val = {}
    for i in range(number_of_variables):
        basic, index = is_column_basic(table[:, i])
        if basic:
            val['x' + str(i)] = table[index, -1]
        else:
            val['x' + str(i)] = 0
    val['optimum'] = table[-1, -1]
    for k, v in val.items():
        val[k] = round(v, 6)
    return val


def is_column_basic(col):
    """
    returns True, index if column is all zero's except one 1 at index,
    otherwise returns False, -1
    """
    found_one = False
    index = -1
    for i, entry in enumerate(col):
        if entry != 0:
            if entry != 1 or found_one:
                return False, -1
            else:
                found_one, index = True, i
    return found_one, index


if __name__ == "__main__":
    def gen_matrix(var, cons):
        """
        generates an empty matrix with adequate size for variables and constraints.
        """
        tab = np.zeros((cons + 1, var + cons + 2))
        return tab


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
