import pika
import time

RABBITMQ_HOST = "rabbitmq"
EXCHANGE_NAME = "logs"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"

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

# Declare a fanout exchange (Pub/Sub)
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

count = 1
while True:
    message = f"Log Message {count}"
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="", body=message)
    print(f" [x] Sent '{message}'")
    count += 1
    time.sleep(2)  # Send a message every 2 seconds