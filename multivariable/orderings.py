#For each ordering, input is in form termMatrix from parser.py
#output is another termMatrix sorted according to the ordering


from CollectLikeTerms import collectLikeTerms

########## Lexicographic Ordering #############
def order_lex(termMatrix):
    t = termMatrix
    #first move around variables within terms
    #then move terms around
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    print(res)
    res= [res[0]] + sorted(res[1:], key = lambda x: x[1:], reverse = True)
    return res
    

########## Graded Lexicographic Ordering #############

########## Reverse Graded Lexicographic Ordering #############

if __name__ == '__main__':
    print('x^2y+y^3x+x+y')
    termMatrix = [[' ', 'x', 'y'], [1.0, 2, 1], [1.0, 1, 3], [1.0, 1, 0], [1.0, 0, 1]]
    print(termMatrix)
    print(order_lex(termMatrix))