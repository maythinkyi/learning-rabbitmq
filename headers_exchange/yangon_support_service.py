import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='isp.headers',durable=True,exchange_type=ExchangeType.headers)

channel.queue_declare(queue='yangon_support_queue',durable=True)
channel.queue_bind(exchange='isp.headers',queue='yangon_support_queue',arguments={
    'x-match': 'any',
    'region': 'yangon'
})

def callback(ch,method,properties,body):
    print(f'[x] YGN Support Received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='yangon_support_queue',on_message_callback=callback)

channel.start_consuming()