"""
For each ordering, input is in form term_matrix from poly_parser.py
output is another term_matrix sorted according to the ordering
"""

# ----- Lexicographic Ordering -----


def order_lex(term_matrix):
    """
    orders lexicographically
    """
    t = term_matrix
    # first move around variables within terms
    # then move terms around
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    res = [res[0]] + sorted(res[1:], key=lambda x: x[1:], reverse=True)
    return res

# Monomial ordering specified by matrix u:
# An n by m sized matrix, u, defines a monomial ordering on N^n by
# for a, b in N^n, a >= b if u*(a-b) doesn't have a negative as it's highest non-zero term.
# Matrix u must have rank >= n and cannot have both negatives and positives in the first non-zero row.
# Example: lexicographical ordering for x, y, z:
# [[1,0,0],[0,1,0],[0,0,1]]

# def monomoial_geq(a, b, u):
#     """
#     input monomials a and b, matrix u which describes a monomial ordering
#     returns boolean whether a >= b based on u
#     """
#     v = u(a-b)
#
# def order_specified(term_matrix, u):
# # Sort: sort the terms based on the ordering specified by matrix u



# ----- Graded Lexicographic Ordering -----

def graded_lex(term_matrix):
    """
    orders by degree first, then breaks ties with lexicographical ordering
    """
    t = term_matrix
    # first move terms around
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    # sort terms based on the sum of their variable orders
    # append a sum of powers to each term, then sort by that sum, then remove sum
    for i in range(1, len(res)):
        res[i].append(sum(res[i][1:]))
    res = [res[0]] + sorted(res[1:], key=lambda x: x[-1], reverse=True)
    # res = [res[0]] + [x[:-1] for x in res[1:]]
    # print(order_lex([res[0]]+res[3:5+1])[1:])
    # if the sum is the same then break the tie with lex ordering
    j = 1
    while j < len(res) - 2:
        if res[j][-1] == res[j+1][-1]:
            start = j
            j += 1
            while res[j][-1] == res[j+1][-1]:
                if j + 1 == len(res) - 1:
                    j += 1
                    break
                j += 1
            end = j
            if j+1 < len(res):
                res = res[0:start] + order_lex([res[0]]+res[start:end+1])[1:] + res[end+1:]
            else:
                
                res = res[0:start] + order_lex([res[0]]+res[start:j+1])[1:]
        else:
            j += 1
    # remove the sum appendage if the terms still has it
    for i in range(len(res)):
        if len(res[i]) > len(res[0]):
            res[i] = res[i][:-1]
    return res
        

# ----- Reverse Graded Lexicographic Ordering -----

def reverse_lex(term_matrix):
    t = term_matrix
    # first move around variables within terms
    # then move terms around
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    res = [res[0]] + sorted(res[1:], key=lambda x: x[-1], reverse=True)
    return res

    
def grev_lex(term_matrix):
    t = term_matrix
    # first move terms around
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    # sort terms based on the sum of their variable orders
    # append a sum of powers to each term, then sort by that sum, then remove sum
    for i in range(1, len(res)):
        res[i].append(sum(res[i][1:]))
    res = [res[0]] + sorted(res[1:], key=lambda x: x[-1], reverse=True)
    # res = [res[0]] + [x[:-1] for x in res[1:]]
    # print(order_lex([res[0]]+res[3:5+1])[1:])
    # if the sum is the same then break the tie with lex ordering
    j = 1
    while j < len(res) - 2:
        if res[j][-1] == res[j+1][-1]:
            start = j
            j += 1
            while res[j][-1] == res[j+1][-1]:
                if j + 1 == len(res) - 1:
                    j += 1
                    break
                j += 1
            end = j
            if j+1 < len(res):
                res = res[0:start] + reverse_lex([res[0]]+res[start:end+1])[1:] + res[end+1:]
            else:
                
                res = res[0:start] + reverse_lex([res[0]]+res[start:j+1])[1:]
        else:
            j += 1
    # remove the sum appendage if the terms still has it
    for i in range(len(res)):
        if len(res[i]) > len(res[0]):
            res[i] = res[i][:-1]
    return res
