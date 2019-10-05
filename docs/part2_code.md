file: *src/shared/consts.py*  

```Python
"""
A module holding constants shared by the server and client.
"""
AMQP_VERSION = (1, 0, 0)
```

file: *src/shared/amqp.py*  

```Python
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
    for number in consts.AMQP_VERSION:
        header += amqp.int_to_bytes(number)

    return header
```

file: *src/shared/\_\_init\_\_.py*  

```Python
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
    for number in consts.AMQP_VERSION:
        header += amqp.int_to_bytes(number)

    return header
```

file: *src/client.py*  

```Python
"""
An AMQP 1.0.0 client implementation.
Specifically aimed at working with DonkeyMQ.
"""
import asyncio
import platform

from shared import get_event_loop, get_protocol_header_bytes

class Client:
    """
    An AMQP 1.0.0 client implementation.
    Specifically aimed at working with DonkeyMQ.
    """
    def __init__(self, ip_address: str, port: int = 5672, loop: asyncio.AbstractEventLoop = get_event_loop()) -> None:
        self.ip_address = ip_address
        self.port = port
        self.loop = loop
        self.protocol_header = get_protocol_header_bytes()

        if platform.system() != "Windows":
            self.reader: asyncio.streams.StreamReader
            self.writer: asyncio.streams.StreamWriter

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.ip_address, self.port, loop=self.loop)
        version_match = await self._negotiate_version()
        if version_match:
            print("Version match")

    async def _negotiate_version(self) -> bool:
        self.writer.write(self.protocol_header)

        data = await self.reader.read(8)
        version_match = False
        if data == self.protocol_header:
            version_match = True

        return version_match

    def disconnect(self) -> None:
        self.writer.close()

    async def test(self) -> None:
        await self.connect()
        self.disconnect()

def main() -> None:
    client = Client('127.0.0.1')
    client.loop.run_until_complete(client.test())
    client.loop.close()

if __name__ == "__main__":
    main()
```

file: *src/server.py*  

```Python
"""
An AMQP 1.0.0 server implementation.
Specifically aimed to be AMQP 1.0.0 compliant.
"""
import signal
import platform
import asyncio
from asyncio.streams import StreamReader, StreamWriter

from shared import get_event_loop, get_protocol_header_bytes

class Server:
    def __init__(self, ip_address: str = "0.0.0.0", port: int = 5672) -> None:
        self.ip_address = ip_address
        self.port = port
        self.loop = get_event_loop()
        self.protocol_header = get_protocol_header_bytes()

        # Win hack
        if platform.system() != "Windows":
            self.loop.add_signal_handler(signal.SIGTERM, self.stop)
            self.loop.add_signal_handler(signal.SIGINT, self.stop)

        self.server: asyncio.base_events.Server
        self.running: bool

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter) -> None:
        addr = writer.get_extra_info("peername")
        print(f"[{addr[0]}:{addr[1]}] Connected")
        version = await self._negotiate_version(reader, writer)
        if version:
            print(f"[{addr[0]}:{addr[1]}] Version match")

    async def _negotiate_version(self, reader: StreamReader, writer: StreamWriter) -> bool:
        data = await reader.read(8)
        version_match = False
        if data == self.protocol_header:
            version_match = True

        writer.write(self.protocol_header)

        return version_match

    async def wakeup(self):
        while self.running:
            await asyncio.sleep(1)

    def start(self) -> None:
        self.running = True
        coro = asyncio.start_server(self.handle_connection, self.ip_address, self.port, loop=self.loop)
        self.server = self.loop.run_until_complete(coro)

        print(f"Serving on {self.server.sockets[0].getsockname()}")

        # Win hack
        if platform.system() == "Windows":
            self.loop.create_task(self.wakeup())
            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                self.loop.run_until_complete(self.wakeup())
        else:
            self.loop.run_forever()

        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

    def stop(self) -> None:
        self.running = False
        self.loop.stop()

def main() -> None:
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
```
