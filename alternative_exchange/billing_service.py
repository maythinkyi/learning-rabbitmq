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

channel.queue_declare(queue='billing_queue',durable=True)
channel.queue_bind(queue='billing_queue',exchange='isp.topic',routing_key='billing.*.*')

def callback(ch,method,properties,body):
    print(f'[x] Billing Received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='billing_queue',on_message_callback=callback)

channel.start_consuming()