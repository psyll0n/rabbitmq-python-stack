import pika

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"

def on_message_received_1(channel, method_frame, header_frame, body):
    print(f"Queue 1 received new message: '{body.decode()}'")
    
def on_message_received_2(channel, method_frame, header_frame, body):
    print(f"Queue 2 received new message: '{body.decode()}'")

# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Declare the consistent hashing exchange
channel.exchange_declare(exchange="simplehashing", exchange_type="x-consistent-hash")

# Declare and bind queues using integer routing keys
channel.queue_declare(queue="letterbox1")
channel.queue_bind(queue="letterbox1", exchange="simplehashing", routing_key="1")  # 1 part

channel.queue_declare(queue="letterbox2")
channel.queue_bind(queue="letterbox2", exchange="simplehashing", routing_key="3")  # 3 parts

# Set up consumers
channel.basic_consume(queue="letterbox1", on_message_callback=on_message_received_1, auto_ack=True)
channel.basic_consume(queue="letterbox2", on_message_callback=on_message_received_2, auto_ack=True)

print("Started consuming messages...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    connection.close()