import pika

parameters = pika.ConnectionParameters(host='localhost', port=5672)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    print("Connection to RabbitMQ successful!")

    connection.close()

except pika.exceptions.AMQPConnectionError:
    print("Failed to connect to RabbitMQ. Please check your connection parameters.")

except Exception as e:
    print("An error occurred:", str(e))