import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='task_exchange',durable=True,exchange_type=ExchangeType.direct)

message = {
    'key': 'val'
}
channel.basic_publish(exchange='task_exchange',routing_key='task',body=json.dumps(message),properties=pika.BasicProperties(delivery_mode=2))