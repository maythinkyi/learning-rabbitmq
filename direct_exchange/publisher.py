import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='logs_direct_exchange',durable=True,exchange_type=ExchangeType.direct)

message = {
    'key':'value'
}

channel.basic_publish(
    exchange='logs_direct_exchange',
    body=json.dumps(message),
    routing_key='ERROR',
    properties=pika.BasicProperties(delivery_mode=2)
)

connection.close()