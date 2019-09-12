---
title: Part 2 - version negotiation
---

## Version negotiation

Now that we have functional, albeit basic, network stack, we can get in to our first AMQP things.  
From here we could implement many things, but after having read the spec a litle bit, I feel that the version handshake is a good place to go next.  

For the whole explenation, you can read the [AMQP spec](http://www.amqp.org/sites/amqp.org/files/amqp.pdf) Chapter 2.2.  
I will briefly try to explain though.  

The spec says that before any frames can be sent (more on frames later), the protocol version must be negotiated.  
This is done by both peers sending a `Protocol Header`.  
This `Protocol Header` consists of the following 8 octets:

- Upper case ASCII letters `AMQP` (4 octets)
- A protocol ID (1 octet)
- Version number: major, minor, revision (3 Octets, 1 octet each)

That doesn't look very complicated, right?  
Ok so first we need to convert everything to bytes and simply send them over the wire.  
Since both our client and server will be using the same header, I'll make a constructor and put in our shared module.  

file: *src/shared/\_\_init\_\_.py*

```Python
def protocol_header_bytes() -> bytes:
    header = b"AMQP"
    header += (0).to_bytes(1, byteorder="big", signed=False)
    version = (1, 0, 0)
    for number in version:
        header += number.to_bytes(1, byteorder="big", signed=False)

    return header
```

Due to python 3 using utf-8 by default, all we have to do is the following:

[<< Part 1 - Introduction and setup](part1.md)  
[Back to index](index.md)  
