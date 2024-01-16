#!/usr//bin/env python3
'''Async Generator that takes no arguments'''
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    '''Define async_generator'''
    for i in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
