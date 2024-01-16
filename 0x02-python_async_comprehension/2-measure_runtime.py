#!/usr/bin/env python3
"""
Write a measure_runtime coroutine that will execute
async_comprehension four times in parallel using asyncio.gather
"""
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    start_time = time.time()
    await asyncio.gather(*[async_comprehension() for i in range(4)])
    total = time.time() - start_time
    return total
