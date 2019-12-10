"""
Simplex method/ Linear Programming for optimizing an objective function with a set of linear constraints
https://youtu.be/E94xNYyjTmg
"""

import numpy as np
from scipy import optimize

def simplex_method(table, dictionary_output=False, unrestricted=False):
    """
    Optimizes linear objective function with linear constraints.
    Returns minimum with respect to objective function.
    To return maximum, change sign of objective function.
    Set unrestricted=True if variables can be negative.
    """
    assert type(table).__name__ == 'ndarray'  # "table[:, -1]" column selection is specific to np.ndarray
    if unrestricted and dictionary_output:
        # preserve objective function to recreate optimum value
        objective_function = table[-1][:-1]

    if unrestricted:
        table = make_unrestricted_variables(table)

    table = add_slack_variables(table)
    last_row = table[-1][:-1]
    while has_a_negative(last_row):
        table = simplex_row_operation(table)
        last_row = table[-1][:-1]

    number_of_variables = len(table[0]) - len(table) - 1
    optimum = np.zeros(number_of_variables + 1)
    for i in range(number_of_variables):
        basic, index = is_column_basic(table[:, i])
        if basic:
            optimum[i] = table[index][-1]
    optimum[-1] = table[-1][-1]

    if unrestricted:
        optimum = reduce_variables(optimum, number_of_variables)

    if dictionary_output:
        variable_dict = {}
        for i, value in enumerate(optimum[:-1]):
            variable_dict['x' + str(i)] = value
        if unrestricted:
            variable_dict['optimum'] = np.array(optimum[:-1]).dot(np.array(objective_function))
        else:
            variable_dict['optimum'] = optimum[-1]
        return variable_dict

    return optimum


def simplex_method_scipy(table, unrestricted=False):
    assert type(table).__name__ == 'ndarray'  # "table[:, -1]" column selection is specific to np.ndarray

    if unrestricted:
        table = make_unrestricted_variables(table)
        number_of_variables = len(table[0]) - 1

    A = table[:-1, :-1]
    b = table[:, -1][:-1]
    c = table[-1][:-1]
    optimum = optimize.linprog(c, A_ub=A, b_ub=b).get('x')

    if unrestricted:
        np.append(optimum, 0)  # reduce requires a dummy at the end
        optimum = reduce_variables(optimum, number_of_variables)[:-1]
    return optimum



def make_unrestricted_variables(table):
    """
    The simplex method minimizes cx subject to Ax=b and x >= 0.
    But here we can have negative x's, so we must modify so that our variables are unrestricted
    To do this we define x_i := x_2i - x_(2i+1).
    We also add constraints that all variables be positive, i.e.
    -x_2i <=0, -x_(2i+1) <= 0
    Later we reconstruct original x_i after simplex
    """
    assert type(table).__name__ == 'ndarray'
    number_of_variables = 2 * (len(table[0]) - 1)
    unresticted = np.zeros((len(table) + number_of_variables, number_of_variables + 1))
    for i in range(len(table) - 1):
        for j in range(len(table[0]) - 1):
            unresticted[i][2 * j] = table[i][j]
            unresticted[i][2 * j + 1] = -table[i][j]
    # now add the last column to unrestricted
    for i in range(len(table) - 1):
        unresticted[i][2 * (len(table[0]) - 1)] = table[i][(len(table[0]) - 1)]
    # Add the objective function to bottom of unrestricted table
    for j in range(len(table[0]) - 1):
        unresticted[-1][2 * j] = table[-1][j]
        unresticted[-1][2 * j + 1] = -table[-1][j]
    # Add -x <= 0 constraint for each variable x
    for i in range(number_of_variables):
        unresticted[len(table) - 1 + i][i] = -1
        unresticted[len(table) - 1 + i][-1] = 0
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


def has_a_negative(vector):
    """
    Returns True if the vector has a value < 0, otherwise returns False
    """
    for i in range(len(vector)):
        if vector[i] < 0:
            return True
    return False


def simplex_row_operation(matrix):
    """
    row operation on matrix to remove negative from last row
    """
    last_row = matrix[-1][:-1]
    pivot_column_index = find_pivot_column(last_row)
    pivot_column = get_column(matrix, pivot_column_index)
    last_column = get_column(matrix, -1)
    pivot_row_index = find_pivot_row(pivot_column[:-1], last_column)
    matrix = pivot(pivot_row_index, pivot_column_index, matrix)
    return matrix


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


def get_column(matrix, index):
    """
    returns the column of matrix at index
    """
    if type(matrix).__name__ == 'ndarray':
        return matrix[:, index]
    if type(matrix).__name__ in {'list', 'Matrix'}:
        raise NotImplemented


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
            if entry > 0:
                ratio = constants[i] / entry
                if ratio < m:
                    m = ratio
                    row_index = i
    return row_index


def pivot(row_index, column_index, table):
    """
    Make a unit column at column index by 'pivoting' around table[row_index][column_index].
    R is row at row index (R = R[row_index])
    R = R / R[column_index]
    Now R has 1 at column index position
    Make all other entries in column 0 by subtracting multiples of R to them.
    """
    assert type(table).__name__ == 'ndarray'  # row multiplication/ division specific to numpy arrays
    result = table.copy()
    result[row_index] /= table[row_index, column_index]
    for i in range(len(result)):
        if i != row_index:
            result[i] = result[i] - result[row_index] * result[i][column_index]
    return result


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


def reduce_variables(optimum, number_of_variables):
    """
    removes the extra variables that were added in make_unrestriced_variables
    x_i := x_2i - x_(2i+1)
    """
    reduced_optimum = []
    for i in range(number_of_variables):
        if i % 2 == 0:
            reduced_optimum.append(optimum[i])
        else:
            reduced_optimum[i // 2] -= optimum[i]
    reduced_optimum.append(optimum[-1])
    return reduced_optimum


if __name__ == "__main__":
    pass
