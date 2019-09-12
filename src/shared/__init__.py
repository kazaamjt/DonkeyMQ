"""Various miscellaneous things that are shared amongst the client and server"""

import sys
import asyncio
from typing import Any

# obsolete in 3.8+, hopefully
def get_event_loop() -> Any:
    """Returns an event loop based on platform"""
    if sys.platform.startswith("win"):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    return loop

def protocol_header_bytes() -> bytes:
    """Constructs a protocol header represented in bytes"""
    header = b"AMQP"
    header += (0).to_bytes(1, byteorder="big", signed=False)
    version = (1, 0, 0)
    for number in version:
        header += number.to_bytes(1, byteorder="big", signed=False)

    return header
