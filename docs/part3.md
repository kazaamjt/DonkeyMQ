---
title: Part 3 - AMQP Frames
---

## On Frames

Part 3 of this code-along, or whatever this is, is all about Frames.  
Buckle up, this part is going to be quite heavy on theory.  
We're going to have to some constraints and knowledge before getting in to the practical side further.  
That being said, let's get in ot it.  

Frames are a very essential part of AMQP.  
They are pretty much the basis of AMQP communication and are used for almost every action.  

Frames can be made up of 3 parts:  

        required        optional        optional
    +--------------+-----------------+------------+
    | frame header | extended header | frame body |
    +--------------+-----------------+------------+
        8 bytes        *variable*      *variable*

The `Frame header` is a fixed 8 bytes long and is the first part of every frame transmitted.
It tells more about how to parse the extended header and body.  

The `Extended Header` is the second part of a frame (if it exists), and is variable length.  
What to do with it depends on the frame type.  

The `Frame Body` holds the actual information and is also variable in length.  
It is currently not clear to me in what scenarios the frame body could be optional, but the spec notes that is optional.  

While the body and the extended header are very dependant on the frame type, the header is pretty much constant,
so we'll only get in to how the header is formed here.  

The `Frame Header` is, as mentioned earlier, a fixed 8 bytes long.  
The first 4 bytes (byte index 0 to 3) define the total `frame size`.  
It's an unsigned 32-bit integer expressing the combined size of the header, extended header and the body.  

The next byte (byte index 4) is the `Data Offset`, also refered to als DOFF in the spec.  
It tells us at what byte offset the body starts at.  
It is a unsigned 8-bit integer expressing the offset in 4 byte "words".  
As the header is 8 bytes long, the minumum offset is 2, and anything lower would be a `malformed frame` according to the spec.  
(Even if there is no body, as the body is optional, the offset is 2.)  

Then comes a single byte to denote the `Frame Type` (byte index 5).  
It is expressed in `AMQP Type codes` and indicates the format and purpose of the frame.  
For example, `0x00` indicates a standard AMQP frame and `0x01` indicates a SASL frame.  

The last 2 bytes (byte index 6 and 7) are noted to be type specific.  
The next chapter opens by stating they contain the channel number, so we'll assume they will unless noted otherwise.  

All together this gives us the following:

        +0       +1       +2       +3
      +-----------------------------------+
    0 |                SIZE               |
      +-----------------------------------+
    4 |  DOFF  |  TYPE  |     CHANNEL     |
      +-----------------------------------+

Now that we got through the header part of the Frames, let's make a class to represent our frame header.  

## Nodes, Containers, Links, Sessions, etc
