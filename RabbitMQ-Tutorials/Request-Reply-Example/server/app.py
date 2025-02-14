import pika
import time

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"
QUEUE_NAME = "rpc_queue"

# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Declare the RPC Queue
channel.queue_declare(queue=QUEUE_NAME)

print(" [x] Awaiting RPC requests.")

def on_request(ch, method, properties, body):
    """Simulate processing the request"""
    request_data = body.decode()
    print(f" [.] Processing request: {request_data}")
    time.sleep(2)  # Simulate processing time
    response_data = f"Processed: {request_data}"

    # Send response back to the reply queue
    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response_data
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_request)

channel.start_consuming()