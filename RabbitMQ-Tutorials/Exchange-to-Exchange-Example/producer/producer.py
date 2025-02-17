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

channel.exchange_declare(exchange="firstexchange", exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange="secondexchange", exchange_type=ExchangeType.fanout)
# Bind the first exchange to the second exchange
channel.exchange_bind("secondexchange", "firstexchange", routing_key="")


message = "This message has gone through to multiple exchanges..."

try:
    while True:
        message = "This message has gone through to multiple exchanges..."
        channel.basic_publish(exchange="firstexchange", routing_key="", body=message)
        print(f"Sent message: '{message}'")
        time.sleep(5)
except Exception as e:
    print(f"An error occurred while publishing message: {e}")

try:
    connection.close()
except Exception as e:
    print(f"An error occurred while closing the connection: {e}")