import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='isp.topic',durable=True,exchange_type=ExchangeType.topic)

channel.queue_declare(queue='noc_queue',durable=True)

channel.queue_bind(exchange='isp.topic', queue='noc_queue',routing_key='device.*.*')
channel.queue_bind(exchange='isp.topic', queue='noc_queue',routing_key='fiber.#')


def callback(ch,method,properties,body):
    print(f'[x] NOC Received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='noc_queue',on_message_callback=callback)

channel.start_consuming()