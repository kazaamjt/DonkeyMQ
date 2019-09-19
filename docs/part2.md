---
title: Part 2 - version negotiation
---

## Version negotiation

Now that we have functional, albeit basic, network stack, we can get in to our first AMQP things.  
From here we could implement many things, but after having read the spec a litle bit, I feel that the version handshake is a good place to go next.  

For the whole explenation, you can read the [AMQP spec](http://www.amqp.org/sites/amqp.org/files/amqp.pdf) Chapter 2.2.  
I will briefly try to explain though.  

As mentioned before, for now, DonkeyMQ will only support the 1.0.0 version.  
So lets's store that in a shared const module:

file: *src/shared/consts.py*

```Python
"""
A module holding constants shared by the server and client.
"""
VERSION = (1, 0, 0)
```

The spec states that before any frames can be sent (more on frames later), the protocol version must be negotiated.  
This is done by both peers sending a `Protocol Header`.  
This `Protocol Header` consists of the following 8 octets:

- Upper case ASCII letters `AMQP` (4 octets)
- A protocol ID (1 octet)
- Version number: major, minor, revision (3 Octets, 1 octet each)

That shouldn't be too complicated, right?  
Ok so first we need to convert everything to bytes and simply send them over the wire.  
Since both our client and server will be using the same protocol header, I'll make a constructor and put in the shared module.  

Now the AMQP spec has type definitions we'll have to adhere to.  
Luckily in the case of strings, it's just utf-8, which python uses by default.  
The integers on the other hand have to be converted specifically to big endian unsigned values, and may not be larger than 1 byte in this case.  
Luckely python integers have a `.to_bytes()` that allows us to set the endianness and maximum byte size.  

Let's make convience `to_bytes` functions that encode and decode various types to and from bytes.  
For now, we'll add a function to convert integers and strings to amqp network bytes:  

file: *src/shared/amqp.py*  

```Python
def str_to_bytes(string: str) -> bytes:
    return string.encode("utf-8")

def int_to_bytes(integer: int) -> bytes:
    return integer.to_bytes(1, byteorder="big", signed=False)

def bytes_to_str(str_bytes: bytes) -> str:
    return str_bytes.decode("utf-8")

def bytes_to_int(int_bytes: bytes) -> int:
    return int.from_bytes(int_bytes, byteorder="big", signed=False)
```

(We'll come back and )
Next, let's add a header constructor to our shared module:  

file: *src/shared/\_\_init\_\_.py*  

```Python
from shared import consts
from shared import amqp

def get_protocol_header_bytes() -> bytes:
    header = amqp.str_to_bytes("AMQP")
    header += amqp.int_to_bytes(0)
    for number in consts.VERSION:
        header += amqp.int_to_bytes(number)

    return header
```

Next let's add it to our client and sent it as our first message.  

file: *src/client.py*

```Python
class Client:
    def __init__(self, ip_address: str, port: int = 5672, loop: asyncio.AbstractEventLoop = get_event_loop()) -> None:
        self.ip_address = ip_address
        self.port = port
        self.loop = loop
        self.protocol_header = get_protocol_header_bytes()

        self.reader: asyncio.streams.StreamReader
        self.writer: asyncio.streams.StreamWriter
```


[<< Part 1 - Introduction and setup](part1.md)  
[Back to index](index.md)  
