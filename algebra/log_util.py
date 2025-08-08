import logging
from time import time
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T")


def log(f: Callable[..., T], show_input: bool = True, show_output: bool = True) -> Callable[..., T]:
    def new_f(*args: Any, **kwargs: Any) -> T:
        if show_input:
            logging.info('Beginning function ' + f.__name__ + ', Input: \n' + str(args) + str(kwargs))
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
        return cast(T, res)

    return new_f


if __name__ == '__main__':
    pass
