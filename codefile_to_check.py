# this file contains some wannabe-python code
# it serves as testcase for the guideline-checker

import numpy as np
from typing import Tuple

# a few signatures to read parameter-names from
def pi():
    """The mathematical constant 3.1415..."""
    return 3.1415926535

def abs(x):
    """the absolute value of a number"""
    if x >= 0:
        return x
    else:
        return -x

def clamp(a, b, c):
    """a restricted to [b,c] (ends included)"""
    if b > c:
        raise ValueError("cannot clamp to emtpy range")
    return np.max([b, np.min([a, c])])

def foo(a: int, b, c: float):
    """whatever..."""
    return

def long_name(a,
              b: float,
              c: float):
    """this docstring contains a and c,
    but not the middle parameter"""
    pass

def very_long_name_that_requires_an_immediate_linebreak(
        a, b,
        c: str
) -> bool:
    """the docstring is fine, has a,b,c"""
    return True

def complicated_types(a: int, b: Tuple[float, float]
) -> Tuple[int,
           Tuple[int, int]]:
    """the docstring does not contain the second parameter"""
    return True
