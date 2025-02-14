import pika
import time
import uuid

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

# Declare exchange (same as producer)
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

# Each consumer gets a unique queue (auto-delete when disconnected)
queue_name = f"consumer-{uuid.uuid4()}"
result = channel.queue_declare(queue=queue_name, exclusive=True)
queue_name = result.method.queue

# Bind queue to exchange
channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

print(f" [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C")

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()