import pika
import json
from pika.exchange_type import ExchangeType
from time import sleep

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

# Create DLX, DLQ and later attach them as arg to the main_queue
channel.exchange_declare(exchange='dlx_exchange',durable=True,exchange_type=ExchangeType.direct)

channel.queue_declare(queue='dlq',durable=True)
channel.queue_bind(exchange='dlx_exchange',queue='dlq',routing_key='dlx')

channel.exchange_declare(exchange='task_exchange',durable=True,exchange_type=ExchangeType.direct)

channel.queue_declare(queue='task_queue',durable=True,
        arguments={
        'x-dead-letter-exchange': 'dlx_exchange',
        'x-dead-letter-routing-key': 'dlx',
        'x-message-ttl': 0  # Message expires after 1s idle
    })
channel.queue_bind(queue='task_queue',exchange='task_exchange',routing_key='task')


def callback(ch,method,properties,body):
    print(f'[x] Task Received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # ch.basic_reject(delivery_tag=method.delivery_tag,requeue=False)

channel.basic_consume(queue='task_queue',on_message_callback=callback)

channel.start_consuming()