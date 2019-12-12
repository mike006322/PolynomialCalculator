import logging
from time import time


def log(f, show_input=True, show_output=True):
    def new_f(*args, **kwargs):
        if show_input:
            logging.info('Beginning function ' + f.__name__ + ', Input: \n' + str([*args]) + str(**kwargs))
        else:
            logging.info('Beginning function ' + f.__name__)
        start = time()
        res = f(*args, **kwargs)
        end = time()
        elapsed = end - start
        if show_output:
            logging.info('Ending function ' + f.__name__ + ' in ' + str(elapsed) + ', Output: \n' + str(res))
        else:
            logging.info('Ending function ' + f.__name__ + ' in ' + str(elapsed))
        return res

    return new_f


if __name__ == '__main__':
    pass
