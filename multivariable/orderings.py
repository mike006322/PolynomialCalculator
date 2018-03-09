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
    res = [res[0]] + sorted(res[1:], key = lambda x: x[1:], reverse = True)
    return res
    

########## Graded Lexicographic Ordering #############

def graded_lex(termMatrix):
    t = termMatrix
    #first move terms aroud
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    #sort terms based on the sum of their variable orders
    #append a sum of powers to each term, then sort by that sum, then remove sum
    for i in range(1, len(res)):
        res[i].append(sum(res[i][1:]))
    res = [res[0]] + sorted(res[1:], key = lambda x: x[-1], reverse = True)
    #res = [res[0]] + [x[:-1] for x in res[1:]]
    #print(order_lex([res[0]]+res[3:5+1])[1:])
    #if the sum is the same then break the tie with lex ordering
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
    #remove the sum appendage if the terms still has it
    for term in res:
        if len(term) > len(res[0]):
            term = term[:-1]
    return res
        

########## Reverse Graded Lexicographic Ordering #############

def reverse_lex(termMatrix):
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
    res = [res[0]] + sorted(res[1:], key = lambda x: x[1:])
    return res
    
def grev_lex(termMatrix):
    t = termMatrix
    #first move terms aroud
    var_order = list(zip(t[0], list(range(len(t[0])))))
    var_order.sort()
    var_order = [u[1] for u in var_order]
    res = [sorted(t[0])]
    for i in range(1, len(t)):
        term = []
        for j in range(len(var_order)):
            term.append(t[i][var_order[j]])
        res.append(term)
    #sort terms based on the sum of their variable orders
    #append a sum of powers to each term, then sort by that sum, then remove sum
    for i in range(1, len(res)):
        res[i].append(sum(res[i][1:]))
    res = [res[0]] + sorted(res[1:], key = lambda x: x[-1], reverse = True)
    #res = [res[0]] + [x[:-1] for x in res[1:]]
    #print(order_lex([res[0]]+res[3:5+1])[1:])
    #if the sum is the same then break the tie with lex ordering
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
    #remove the sum appendage if the terms still has it
    for term in res:
        if len(term) > len(res[0]):
            term = term[:-1]
    return res

if __name__ == '__main__':
    print('x^2y^2z+y^3xz+z+x+y')
    termMatrix = [[' ', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
    #print(termMatrix)
    print(grev_lex(termMatrix))
