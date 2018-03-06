#input is termMatrix from parser.py
#output is another termMatrix with terms collected

#termMatrix = [[" ", variable1, variable2...], [coefficient, exponent1, exponent2...],...]

def collectLikeTerms(termMatrix):
    t = termMatrix
    for i in range(1, len(t)):
        if i < len(t) - 1:
            for j in range(i+1, len(t)):
                if t[i][1:] == t[j][1:]:
                    t[i] = [t[i][0]+t[j][0]]+t[i][1:]
                    t[j][0] = 0
    #get rid of 0 terms
    t = [u for u in t if u[0] != 0]
    return t

if __name__ == '__main__':
    print('x^2y+4x^2y+8+16+2x+y = 5x^2y+2x+y+24')
    termMatrix = [[' ', 'y', 'x'], [1.0, 1, 2], [4.0, 1, 2], [8.0, 0, 0], [16.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
    print(collectLikeTerms(termMatrix))