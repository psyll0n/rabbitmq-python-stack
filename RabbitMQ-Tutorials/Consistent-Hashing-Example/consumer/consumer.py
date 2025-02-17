import pika
from pika.exchange_type import ExchangeType


RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"


def on_message_recieved(channel, method_frame, header_frame, body):
    print(f"Received new message: '{body}'")
    

# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="headersexchange", exchange_type=ExchangeType.headers)
channel.queue_declare(queue="letterbox")
bind_args = {
    'x-match': 'all',
    'name': 'John Doe',
    'age': 30
} 

channel.queue_bind(queue="letterbox", exchange="headersexchange", arguments=bind_args)
channel.basic_consume(queue="letterbox", on_message_callback=on_message_recieved, auto_ack=True)

print("Started consuming messages...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    connection.close()