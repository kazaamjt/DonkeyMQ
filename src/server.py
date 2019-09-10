"""
An AMQP 1.0.0 server implementation.
Specifically aimed to be AMQP 1.0.0 compliant.
"""
import signal
import asyncio

from shared import get_event_loop

class Server:
    def __init__(self, ip_address: str = "0.0.0.0", port: int = 5672) -> None:
        self.ip_address = ip_address
        self.port = port
        self.loop = get_event_loop()

        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        self.loop.add_signal_handler(signal.SIGINT, self.stop)

        self.server: asyncio.base_events.Server

    async def handle_msg(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
        while True:
            data = await reader.read(100)
            message = data.decode()
            addr = writer.get_extra_info('peername')

            print(f"[{addr[0]}:{addr[1]}] {message}")
            if message == "test":
                writer.write(b"message received")
                await writer.drain()

            elif message == "close":
                writer.write(b"ok")
                await writer.drain()
                break

            else:
                writer.write(b"nok")
                await writer.drain()
                break

        print("Closed the client socket")
        writer.close()

    def start(self) -> None:
        coro = asyncio.start_server(self.handle_msg, self.ip_address, self.port, loop=self.loop)
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
