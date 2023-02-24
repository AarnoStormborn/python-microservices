import pika
import json
from app import Product
from app import app, db

URL = "amqps://onemgswk:bHqVQSi4BV0pgJ1mRjkOX2fxMFUu7-f_@woodpecker.rmq.cloudamqp.com/onemgswk"
params = pika.URLParameters(URL)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(data)

    if properties.content_type == 'Product Created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print("Created")

    if properties.content_type == 'Product Updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print("Updated")

    if properties.content_type == 'Product Deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("Deleted")


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')
with app.app_context():
    channel.start_consuming()
channel.close()
