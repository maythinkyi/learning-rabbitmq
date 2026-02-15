import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='logs_direct_exchange',durable=True,exchange_type=ExchangeType.direct)

channel.queue_declare(queue='dashboard_queue',durable=True)

channel.queue_bind(exchange='logs_direct_exchange',queue='dashboard_queue',routing_key='WARNING')
channel.queue_bind(exchange='logs_direct_exchange',queue='dashboard_queue',routing_key='ERROR')

def callback(ch,method,properties,body):
    print(f'[x] Dashboard Recevied: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='dashboard_queue',on_message_callback=callback)

channel.start_consuming()