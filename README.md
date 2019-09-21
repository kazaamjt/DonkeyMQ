# DonkeyMQ

DonkeyMQ is my attempt at making an AMQP client and server.  

Follow my journey [here](https://kazaamjt.github.io/DonkeyMQ/).  

## The server in docker

Building the container image:  

`docker build -t donkey-server .`

Running the container:  

`docker run -p 5672:5672 --name donkey_server_instance -i -t donkey-server`

Or:  

`docker run -d -p 5672:5672 donkey-server`
