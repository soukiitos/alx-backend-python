#!/usr/bin/env python3
'''Correct duck-typed annotations'''
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''Defining the function safe_first_element'''
    if lst:
        return lst[0]
    else:
        return None
