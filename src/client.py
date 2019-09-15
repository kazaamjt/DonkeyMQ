"""
An AMQP 1.0.0 client implementation.
Specifically aimed at working with DonkeyMQ.
"""
import asyncio

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

        self.reader: asyncio.streams.StreamReader
        self.writer: asyncio.streams.StreamWriter

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.ip_address, self.port, loop=self.loop)
        version_match = await self._negotiate_version()
        if version_match:
            pass

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
