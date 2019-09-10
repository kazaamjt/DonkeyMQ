"""
An AMQP 1.0.0 client implementation.
Specifically aimed at working with DonkeyMQ.
"""
import asyncio

from shared import get_event_loop

class Client:
    """
    An AMQP 1.0.0 client implementation.
    Specifically aimed at working with DonkeyMQ.
    """
    def __init__(self, ip_address: str, port: int = 5672, loop: asyncio.AbstractEventLoop = get_event_loop()) -> None:
        self.ip_address = ip_address
        self.port = port
        self.loop = loop

        self.reader: asyncio.streams.StreamReader
        self.writer: asyncio.streams.StreamWriter

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.ip_address, self.port, loop=self.loop)

    def disconnect(self) -> None:
        self.writer.close()

    async def test(self) -> None:
        await self.connect()
        self.writer.write(b"test")
        data = await self.reader.read(100)
        if data.decode() == "message received":
            self.writer.write(b"close")

        data = await self.reader.read(100)
        if data.decode() == "ok":
            print("success")
        else:
            print("failed")

        self.disconnect()

def main() -> None:
    client = Client('127.0.0.1')
    client.loop.run_until_complete(client.test())
    client.loop.close()

if __name__ == "__main__":
    main()
