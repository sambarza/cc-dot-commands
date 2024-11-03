from fastapi import Depends
from typing import Dict

import os
import anyio.to_thread
import psutil

from cat.auth.permissions import AuthPermission, AuthResource
from cat.auth.connection import HTTPAuth
from cat.mad_hatter.decorators import endpoint

# server introspection
@endpoint.get("/introspection", prefix="/dot-commands", tags=["Dot Commands"])
async def introspection(
    stray=Depends(HTTPAuth(AuthResource.STATUS, AuthPermission.READ)),
) -> Dict:
    """Server internal status"""

    anyio_threads_limiter = anyio.to_thread.current_default_thread_limiter()

    limiter_statistics = anyio_threads_limiter.statistics()

    process = psutil.Process(os.getpid())

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)

    memory_info = process.memory_info()
    virtual_memory = psutil.virtual_memory()

    memory_rss = memory_info.rss
    memory_vms = memory_info.vms
    memory_percent = process.memory_percent()

    disk_usage = psutil.disk_usage("/")

    net_io = psutil.net_io_counters()

    return {
        "CPU Utilization %": cpu_usage,
        "CPU Logical Cores": cpu_count,
        "Physical Memory Usage (RSS) MB": f"{memory_rss / (1024 ** 2):.2f}",
        "Virtual Memory Usage (VMS) MB": f"{memory_vms / (1024 ** 2):.2f}",
        "Memory Usage %": f"{memory_percent:.2f}",
        "Total System Memory MB": f"{virtual_memory.total / (1024 ** 2):.2f}",
        "Disk Usage %": disk_usage.percent,
        "Send Network Packets": net_io.packets_sent,
        "Received Network Packets": net_io.packets_recv,
        "max_thread": limiter_statistics.total_tokens,
        "running_threads": limiter_statistics.borrowed_tokens,
        "tasks_waiting": limiter_statistics.tasks_waiting,
    }
