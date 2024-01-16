#!/usr//bin/env python3
'''Async Generator that takes no arguments'''
import asyncio
import random
import typing


async def async_generator() -> typing.Generator[float, None, None]:
    '''Define async_generator'''
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
