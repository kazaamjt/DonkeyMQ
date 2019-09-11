# Writing an AMQP server from scratch

Through this series I will be attempting to write an AMQP server from scratch.  

For my day job I have used RabbitMQ in combination with multiple plugins and client libraries.  
I recently had to dig deep in to the [RabbitMQ-C Library](https://github.com/alanxz/rabbitmq-c) and making RabbitMQ scale horizontaly.  
This sparked my interests and I wanted to know more about how AMQP works, what it defines and what it leaves up to implementers.  

Specifically I want to dig in to the following topics:  

- How does AMQP work at a base level?
- How does distribution of a cluster work?
- How are messages stored?
- Uncover The inner workings of queues, exchanges and routing?
- Maybe tackle some of the horizontal scaling problems RMQ has?

To do all this, I will be working off the [AMQP](https://www.amqp.org/) official [version 1.0 spec](http://www.amqp.org/sites/amqp.org/files/amqp.pdf).  

This project was inspired by such projects as [CStack's awesome DB-Tutorial](https://github.com/cstack/db_tutorial) and [Handmade Hero](https://handmadehero.org/).  

## Table of contents

[Part 1 - Introduction and setup](part1.md)
