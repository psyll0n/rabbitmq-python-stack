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
        break
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready, retrying in 5 seconds...")
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()