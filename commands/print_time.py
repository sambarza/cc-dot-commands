import asyncio
import anyio

from datetime import datetime

from cat.looking_glass.stray_cat import StrayCat

async def log_time_async():

    while True:
        print("Current time is", datetime.now())
        await asyncio.sleep(0.5)

def get_limiter():

    asyncio.create_task(log_time_async())

def start_print_time(cat: StrayCat):

    # Using directly anyio.to_thread.current_default_thread_limiter we get the thread capacity
    # limiter of the event loop running in the current thread, 
    # we need the thread capacity limiter of the event loop running in the main event loop
    anyio.from_thread.run_sync(get_limiter)

    return {"output": f"Now the current time will be print in the log each second (using the main event loop)"}