import pika
import uuid
import time

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"
QUEUE_NAME = "rpc_queue"

class RPCClient:
    def __init__(self):
        """Initialize the connection and create a temporary reply queue"""
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.channel = self.connection.channel()

        # Create a reply queue for receiving responses
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        # Start listening for responses
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        """Callback to handle response messages"""
        if self.corr_id == properties.correlation_id:
            self.response = body.decode()

    def call(self, message):
        """Send request and wait for response"""
        self.response = None
        self.corr_id = str(uuid.uuid4())  # Generate a unique correlation ID

        self.channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=message
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        
        return self.response

# Run the client continuously every 3 seconds
rpc_client = RPCClient()

counter = 1
while True:
    request_message = f"Request {counter}"
    print(f" [x] Sending request: {request_message}")
    response = rpc_client.call(request_message)
    print(f" [.] Got response: {response}")
    
    counter += 1
    time.sleep(3)  # Wait for 3 seconds before sending the next request