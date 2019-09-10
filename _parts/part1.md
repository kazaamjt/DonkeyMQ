---
title: Part 1 - Introduction and setup
date: 2019-08-20
---

## Setup

Let's dig right in.  

What will we be using?  
I'll be using Python 3.7 on Windows. (Although I will test everything on linux/Debian 10 as well)  
I will also build an AMQP client from scratch along with the server, for testing purposes.  

I chose python because it's easy to use async networking, making it quite ideal for AMQP, which is also aimed at being async.  

I''ll be implementing the [AMQP V1.0](http://www.amqp.org/sites/amqp.org/files/amqp.pdf) version of the AMQP protocol.  
It is a quite different protocol from the more widely implemented 0.9.1 version but it promises significant improvements over the older versions.  

## Networking

The basis of AMQP is networking.  
According to the spec we should support TCP and SCTP.  
However SCTP, while in theory very usefull for us, is much newer and support for it is not as widespread, so I'll start with TCP.  
TLS is also supposed to be supported, but again, later.  

First I'll start with an async tcp server and client.  

To use async networking, I'll use the standard library asyncio library.  
It requires us using an async event loop, and this is our first cross platform problem.  

The default eventloop on windows is currently not interuptable.  
While in python 3.8 this is supposedly fixed, it is not in my 3.7.4 version.  
So I set up a litle function that hands the right type of event loop:  

file: *src/shared/__init__.py*

```python
import sys
import asyncio
from typing import Any

def get_event_loop() -> Any:
    if sys.platform.startswith("win"):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    return loop
```

Next we set up our client to sent a simple test message, then for a response.  
Once the response has been received, we send a close message, signaling that we want to close the connection.  
We then expect an "ok" reply and close the connection either way.  

This emulates the setting up and tearing down connections a litle bit like AMQP does.  

file: *src/client.py*

```python
import asyncio

from shared import get_event_loop

class Client:
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
        self.writer.write("test".encode())
        data = await self.reader.read(100)
        if data.decode() == "message received":
            self.writer.write("close".encode())

            data = await self.reader.read(100)
            if data.decode() == "ok":
                print("success")
            else:
                print("failed")
        else:
            print("failed")

        self.disconnect()

def main() -> None:
    client = Client('127.0.0.1')
    client.loop.run_until_complete(client.test())
    client.loop.close()

if __name__ == "__main__":
    main()
```

Now that we have our client set up we get our server set up.  
Our server is going to accept incomming connections and handle according to the messages it received.  

After writing make sure to call writer.drain().  
It's a flow control method that pauses our coroutine from writing more data to the buffer until the client is all caught up.  
More on the drain method [here](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamWriter.drain).  

The `loop.add_signal_handler` method makes it so that our service can be interupted by `ctrl+c` or the posix TERM signal.  
We need this methed instead of the clasic way fo doing this, because normal signal handeling doesn't actually interupt the loop.  
To make things worse, the `loop.add_signal_handler` hasn't been implemented on windows at the time of writing.  
As a workaround, we'll write a docker file and run our server app in a container.  
Running python apps as a service on windows is a pain. (windows services are a pain in the ass in general)  
A somewhat simple module allowing python scripts to run as a service can be found [here](https://github.com/kazaamjt/WinPyService).  
But I digress, back to programming:  

file: *src/server.py*

```python
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
```

The while loop is more for show than actually doing anything, but it will be usefull later.  
besides that it's important to note that `self.loop.stop()` gets called in `self.stop`, while everything else stays in start.  
This is because otherwise python tries to start a new loop to close the server while the current loop still exists.  

Now about running this in a container, on a linux machine this is not needed, but you have litle choice on windows.  
Luckely docker is quick to get going, a very simple `Dockerfile` will get us going:

```Dockerfile
FROM python:3.7.4-slim-buster

COPY src/server.py .
COPY src/shared ./shared

EXPOSE 5672

CMD ["python", "server.py"]
```

Now all we need to do is build this image and then run it:

`docker build -t donkey-server .`
`docker run -p 5672:5672 --name donkey_server_instance -i -t donkey-server`

I am not going to go any deeper in to the usage of docker, as I consider it out of scope for this guide.  

And with that, the groundwork for both our client library and server have been laid.  
In part 2 we will get in to the actual AMQP spec itself, discussing frames and frame-headers and how to handle those.  
