---
title: Part 1 - Introduction and setup
date: 2019-08-20
---

## Setup

Let's dig right in.  

What will we be using?  
I'll be using Python 3.7 on Windows. (Although I will test everything on linux/Debian 10 as well)  
We will also build an AMQP client from scratch along with the server, for testing purposes.  

I chose python because it's easy to use async networking, making it quite ideal for AMQP, which is also aimed at being async.  

We will be implementing the [AMQP V1.0](http://www.amqp.org/sites/amqp.org/files/amqp.pdf) version of the AMQP protocol.  
It is a quite different protocol from the more widely implemented 0.9.1 version but it should has significant improvements over the older versions.  

## Networking

The basis of AMQP is networking.  
According to the spec we should support TCP and SCTP.  
However SCTP is much newer and support for it is not as widespread, so we'll start with TCP.  
TLS is also supposed to be supported, but again, later.

First we'll start with an async tcp server and client.  
