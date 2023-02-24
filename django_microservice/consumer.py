import pika

URL = "amqps://onemgswk:bHqVQSi4BV0pgJ1mRjkOX2fxMFUu7-f_@woodpecker.rmq.cloudamqp.com/onemgswk"
params = pika.URLParameters(URL)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print(f"Received\n{body}")


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')
channel.start_consuming()
channel.close()
