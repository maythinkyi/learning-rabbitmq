import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='isp.topic',durable=True,exchange_type=ExchangeType.topic,arguments={'alternate-exchange': 'alt_exchange'})

channel.exchange_declare(exchange='alt_exchange',durable=True,exchange_type=ExchangeType.fanout)
channel.queue_declare(queue='alt_queue',durable=True)
channel.queue_bind(exchange='alt_exchange',queue='alt_queue',routing_key='alt')

channel.queue_declare(queue='device_queue',durable=True)
channel.queue_bind(queue='device_queue',exchange='isp.topic',routing_key='device.*.*')

def callback(ch,method,properties,body):
    print(f'[x] Device Received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='device_queue',on_message_callback=callback)

channel.start_consuming()