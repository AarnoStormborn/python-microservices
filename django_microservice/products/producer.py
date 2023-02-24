import pika
import json

URL = "amqps://onemgswk:bHqVQSi4BV0pgJ1mRjkOX2fxMFUu7-f_@woodpecker.rmq.cloudamqp.com/onemgswk"
params = pika.URLParameters(URL)

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
