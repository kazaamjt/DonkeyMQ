"""
An AMQP 1.0.0 server implementation.
Specifically aimed to be AMQP 1.0.0 compliant.
"""
import signal
import asyncio
from asyncio.streams import StreamReader, StreamWriter

from shared import get_event_loop, protocol_header_bytes

class Server:
    def __init__(self, ip_address: str = "0.0.0.0", port: int = 5672) -> None:
        self.ip_address = ip_address
        self.port = port
        self.loop = get_event_loop()
        self.protocol_header = protocol_header_bytes()

        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        self.loop.add_signal_handler(signal.SIGINT, self.stop)

        self.server: asyncio.base_events.Server

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter) -> None:
        addr = writer.get_extra_info("peername")
        print(f"[{addr[0]}:{addr[1]}] Connected")
        version = await  self._negotiate_version(reader, writer)
        if version:
            pass

    async def _negotiate_version(self, reader: StreamReader, writer: StreamWriter) -> bool:
        data = await reader.read(8)
        version_match = False
        if data == self.protocol_header:
            version_match = True

        writer.write(self.protocol_header)

        return version_match

    def start(self) -> None:
        coro = asyncio.start_server(self.handle_connection, self.ip_address, self.port, loop=self.loop)
        self.server = self.loop.run_until_complete(coro)

        print(f"Serving on {self.server.sockets[0].getsockname()}")
        self.loop.run_forever()

        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

    def stop(self) -> None:
        self.loop.stop()

def main() -> None:
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
