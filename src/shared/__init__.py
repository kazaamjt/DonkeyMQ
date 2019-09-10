"""Various miscellaneous things that are shared amongst the client and server"""

import sys
import asyncio
from typing import Any

# obsolete in 3.8+
def get_event_loop() -> Any:
    """Returns an event loop based on platform"""
    if sys.platform.startswith("win"):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    return loop
