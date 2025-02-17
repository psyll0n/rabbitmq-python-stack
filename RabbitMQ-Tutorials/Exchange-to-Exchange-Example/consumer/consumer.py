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

channel.exchange_declare(exchange="secondexchange", exchange_type=ExchangeType.fanout)
channel.queue_declare(queue="letterbox")
channel.queue_bind(exchange="secondexchange", queue="letterbox")

channel.basic_consume(queue="letterbox", on_message_callback=on_message_recieved, auto_ack=True)

print("Started consuming messages...")
channel.start_consuming()