def collect_like_terms(termMatrix):
    """
    input is polynomial in form of termMatrix from poly_parser.py
    output is another termMatrix with terms collected
    termMatrix = [[" ", variable1, variable2...], [coefficient, exponent1, exponent2...],...]
    """
    t = termMatrix
    for i in range(1, len(t)):
        if i < len(t) - 1:
            for j in range(i+1, len(t)):
                if t[i][1:] == t[j][1:]:
                    t[i] = [t[i][0]+t[j][0]]+t[i][1:]
                    t[j][0] = 0
    # get rid of 0 terms
    t = [u for u in t if u[0] != 0]
    # get rid of extra variables
    if len(t[0]) > 0:
        for i in range(len(t[0]) - 1, 0, -1):
            # in reverse so deletion doesn't affect index of subsequent variables
            extra = True
            if len(t) > 0:
                for term in t[1:]:
                    if term[i] != 0:
                        extra = False
            if extra:
                for term in t:
                    del term[i]
    return t

if __name__ == '__main__':
    pass