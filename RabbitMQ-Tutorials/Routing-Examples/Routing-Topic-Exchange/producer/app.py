import pika
import time

RABBITMQ_HOST = "rabbitmq"
EXCHANGE_NAME = "topic_logs"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"

messages = [
    ("business.europe.purchases", "Business purchase in Europe"),
    ("user.europe.purchases", "User purchase in Europe"),
    ("user.europe.payments", "User payment in Europe"),
]

# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        break
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready, retrying in 5 seconds...")
        time.sleep(5)

channel = connection.channel()

# Declare Topic Exchange
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")

while True:
    for routing_key, message in messages:
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=routing_key, body=message)
        print(f" [x] Sent '{message}' with routing key '{routing_key}'")
    time.sleep(5)