import pika

# RabbitMQ connection parameters
parameters = pika.ConnectionParameters(host='localhost', port=5672)

try:
    # Establish a connection
    connection = pika.BlockingConnection(parameters)

    # Create a channel
    channel = connection.channel()

    # Connection successful
    print("Connection to RabbitMQ successful!")

    # Close the connection
    connection.close()

except pika.exceptions.AMQPConnectionError:
    # Connection failed
    print("Failed to connect to RabbitMQ. Please check your connection parameters.")

except Exception as e:
    # Other exceptions
    print("An error occurred:", str(e))