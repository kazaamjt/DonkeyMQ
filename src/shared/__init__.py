"""Various miscellaneous things that are shared amongst the client and server"""

import sys
import asyncio
from typing import Any
from shared import consts
from shared import amqp

# obsolete with python 3.8+, hopefully
def get_event_loop() -> Any:
    """Returns an event loop based on platform"""
    if sys.platform.startswith("win"):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    return loop

def get_protocol_header_bytes() -> bytes:
    """Constructs a protocol header represented in bytes"""
    header = amqp.str_to_bytes("AMQP")
    header += amqp.int_to_bytes(0)
    for number in consts.VERSION:
        header += amqp.int_to_bytes(number)

    return header
