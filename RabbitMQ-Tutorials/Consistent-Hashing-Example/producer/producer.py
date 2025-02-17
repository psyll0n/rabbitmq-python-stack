import pika
import time
from pika.exchange_type import ExchangeType

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"


# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="headersexchange", exchange_type=ExchangeType.headers)
message = "This message will be sent with headers..."

try:
    while True:
        channel.basic_publish(
            exchange="headersexchange", 
            routing_key="",
            properties=pika.BasicProperties(headers={"name": "John Doe", "age": 30}), 
            body=message)
        print(f"Sent message: '{message}'")
        time.sleep(5)
except Exception as e:
    print(f"An error occurred while publishing message: {e}")

try:
    connection.close()
except Exception as e:
    print(f"An error occurred while closing the connection: {e}")