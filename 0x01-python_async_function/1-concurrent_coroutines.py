#!/usr/bin/env python3
'''Execute multiple coroutines at the same time with async'''
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''Define wait_n'''
    random_del: List[float] = []
    Delays: List[float] = []
    Delays = [await wait_random(max_delay) for i in range(n)]
    return sorted(Delays)
