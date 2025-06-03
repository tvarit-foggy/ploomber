"""
Extensions for the inspect module
"""

import inspect


def getfile(fn):
    """
    Returns the file where the function is defined. Works even in wrapped
    functions
    """
    if hasattr(fn, "__wrapped__"):
        return getfile(fn.__wrapped__)
    else:
        # Handle Cython functions
        if hasattr(fn, '__code__') and hasattr(fn.__code__, 'co_filename'):
            return fn.__code__.co_filename
        else:
            return inspect.getfile(fn)
