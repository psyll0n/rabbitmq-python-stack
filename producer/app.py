import pika
import time

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"
QUEUE_NAME = "task_queue"

# Retry logic for connection
while True:
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        break  # Connection successful, exit loop
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready, retrying in 5 seconds...")
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

count = 1
while True:
    message = f"Message {count}"
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f" [x] Sent '{message}'")
    count += 1
    time.sleep(2)