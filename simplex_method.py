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


def pivot(row_index, column_index, table):
    result = table.copy()
    result[row_index] /= table[row_index, column_index]
    for i in range(len(result)):
        if i != row_index:
            result[i] = result[i] - result[row_index] * result[i][column_index]
    return result


def simplex_method(table, output='variable_names', unrestricted=False):
    """
    Optimizes linear objective function with linear constraints
    """
    assert type(table) == np.ndarray  # "table[:, -1]" column selection is specific to np.ndarray

    if unrestricted:
        table = make_unrestricted_variables(table)

    table = add_slack_variables(table)

    while has_a_negative(table[-1][:-1]):
        pivot_column_index = find_pivot_column(table[-1][:-1])
        pivot_row_index = find_pivot_row(table[:, pivot_column_index], table[:, -1])
        table = pivot(pivot_row_index, pivot_column_index, table)

    if output == 'table':
        return table

    number_of_columns = len(table[0])
    number_of_rows = len(table)
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
                    epsilon[(i - 1) // 2 % n][-1] += -1 * table[index, -1]
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


def make_unrestricted_variables(table):
    """
    The simplex method minimizes cx subject to Ax=b and x >= 0.
    But here we can have negative x's, so we must modify so that our variables are unrestricted
    To do this we define x_i := x_2i - x_(2i+1). Then we reconstruct original x_i after simplex
    """
    unresticted = np.zeros((len(table), 2 * (len(table[0]) - 1) + 1))
    for i in range(len(table)):
        for j in range(len(table[0]) - 1):
            unresticted[i][2 * j] = table[i][j]
            unresticted[i][2 * j + 1] = -1 * table[i][j]
    # now add the last column to unrestricted
    for i in range(len(table)):
        unresticted[i][2 * (len(table[0]) - 1)] = table[i][(len(table[0]) - 1)]
    return unresticted


def add_slack_variables(table):
    """
    insert the identity matrix before the constants
    the size of the identity is the number of constraints plus 1 for the objective function
    """
    assert type(table) == np.ndarray
    id = np.identity(len(table))
    table_with_id_inserted = np.concatenate((table[:, 0:-1], id), axis=1)
    last_column = table[:, -1]
    table_with_id_inserted = np.column_stack((table_with_id_inserted, last_column))
    return table_with_id_inserted


def is_column_basic(col):
    """
    returns True, index if column is all zero's except one 1 at index,
    otherwise returns False, -1
    Basic column is also knows as "unit column"
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
    pass
