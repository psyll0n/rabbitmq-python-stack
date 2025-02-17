## `rabbitmq-python-stack`

Example RabbitMQ docker-compose stacks for testing and learning 🚀🐇

This repository was created by using the YouTube playlist linked below.

Reference: [RabbitMQ Tutorials Playlist](https://youtube.com/playlist?list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO&si=Wknp4RcnAcUmM2HZ)

Also see, [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials).


## Getting Started 🚀

To bring up the stack execute the command:

`docker-compose up --build`

Verify that all Docker containers are running:

`docker ps`

## Access RabbitMQ Management UI

RabbitMQ provides a management UI at:

`http://localhost:15672`

Username: `user`
Password: `password`
 

## Stopping the Stack 🛑 

`docker-compose down`

`docker-compose down --volumes`
