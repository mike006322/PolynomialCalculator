#input a string that represents a polynomial equal to 0
#output coded polynomial as [[" ", variable1, variable2...], [coefficient, exponent1, exponent2...],...]
#Matrix will be as follows:
#
#(blank)    , varable1 label, variable2 label,...
#coefficient, exponent1     , exponent2
#coefficient, exponent1     , exponent2
#  .
#  .
#  .

def parse_poly(s_input):
    s = s_input.replace(" ", "").replace("-","+-").replace("*", "").lower().split("+")
    termMatrix = [[" "]]
    num_terms = len(s)
    for _ in range(num_terms):
        termMatrix.append([])
        
    num_var = 0
    
    def addVar(var):
        #if var is present, adds var to the list of variables and incriments num_var
        for term in s:
            if var in term:
                if var not in termMatrix[0]:
                    termMatrix[0].append(var)
                    nonlocal num_var
                    num_var += 1
    
    def addExp(k):
        #replaces 0 in kth entry of term in termMatrix with exponent
        var = termMatrix[0][k]
        for j in range(len(s)):
            term = s[j]
            if var in term:
                i = term.index(var)
                var_len = len(var)
                if i < len(term) - var_len:
                    if term[i+var_len] == '^':
                        termMatrix[j+1][k] = int(term[i+1+var_len])
                    else:
                        termMatrix[j+1][k] = 1 
                else:
                    termMatrix[j+1][k] = 1 
    
    def addCoeff():
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
            termMatrix[j+1][0] = float(coeff)
    
    def findVars():
        variables = set()
        possibleVariables = {'x', 'y', 'z', 't', 'u', 'v', 'r'}
        for term in s:
            for t in range(len(term)):
                if term[t] in possibleVariables:
                    if t < len(term) - 1:
                        if term[t+1].isnumeric():
                            variables.add(term[t]+term[t+1])
                        else:
                            variables.add(term[t])
                    else:
                        variables.add(term[t])
        return variables
                    
    def fill():
        variables = findVars()
        for v in variables:
            addVar(v)
        for i in range(1, len(termMatrix)):
            termMatrix[i].append('coeff')
        addCoeff()
        for i in range(1, len(termMatrix)):
            for _ in range(num_var):
                termMatrix[i].append(0)
        for i in range(1, num_var+1):
            addExp(i)

    fill()
    return termMatrix
    
if __name__ == "__main__":
    #poly = 'z^3*4x^2+8+y*z^4'
    #poly = '2*X^2y-x-2'
    poly = 'x1^2*x2^3 - 9Z^4T^2 + 7x^2x2^6'
    print(poly)
    print(parse_poly(poly))
