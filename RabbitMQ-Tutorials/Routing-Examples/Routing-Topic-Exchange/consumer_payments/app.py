import pika

RABBITMQ_HOST = "rabbitmq"
EXCHANGE_NAME = "topic_logs"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"

# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Declare Topic Exchange
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")

# Declare Queue
queue_name = "payments"
channel.queue_declare(queue=queue_name)

# Bind to topic "user.europe.payments"
channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key="user.europe.payments")

print(" [*] Waiting for payments messages.")

def callback(ch, method, properties, body):
    print(f" [x] Payments Consumer received: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()