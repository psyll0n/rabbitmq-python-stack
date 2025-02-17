import time
import pika


RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"


# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

channel.exchange_declare("simplehashing", "x-consistent-hash")
routing_key = "Hash Me!"
message = "This is a hashed message..."


try:
    while True:
        channel.basic_publish(
            exchange="simplehashing", 
            routing_key=routing_key,
            body=message)
        print(f"Sent message: '{message}'")
        time.sleep(5)
except Exception as e:
    print(f"An error occurred while publishing message: {e}")

try:
    connection.close()
except Exception as e:
    print(f"An error occurred while closing the connection: {e}")