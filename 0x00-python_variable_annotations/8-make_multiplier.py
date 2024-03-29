#!/usr/bin/env python3
"""
Write a type-annotated function make_multiplier
that takes a float multiplier as argument
and returns a function that multiplies a float by multiplier
"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''Defining the function make_multiplier'''
    def multiplies(n: float):
        '''Define the function multiplier'''
        return n * multiplier
    return multiplies
