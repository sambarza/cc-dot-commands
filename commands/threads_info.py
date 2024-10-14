import threading
import anyio

from cat.looking_glass.stray_cat import StrayCat

def get_limiter():

    return anyio.to_thread.current_default_thread_limiter()

def threads_info(cat: StrayCat):

    thread_list = threading.enumerate()

    # Using directly anyio.to_thread.current_default_thread_limiter we get the thread capacity
    # limiter of the event loop running in the current thread, 
    # we need the thread capacity limiter of the event loop running in the main event loop
    main_thread_anyio_threads_limiter = anyio.from_thread.run_sync(get_limiter)

    limiter_statistics = main_thread_anyio_threads_limiter.statistics()

    output = f"""
**`Threads info`**
```text
Total running threads {len(thread_list)}

Max worker threads      - {limiter_statistics.total_tokens}
Borrowed worker threads - {limiter_statistics.borrowed_tokens}
Waiting worker threads  - {limiter_statistics.tasks_waiting}
```

**`Threads list`**

||||
|-|-|-|
|Name|Idle Since|Root Event Loop ID
"""

    for thread in thread_list:
        if type(thread) == anyio._backends._asyncio.WorkerThread:
            output += f"{thread.name}|{thread.idle_since}|{id(thread.loop)}\n"
        else:
            output += f"{thread.name}||\n"

    return {"output": output}
