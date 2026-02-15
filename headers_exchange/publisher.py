import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='isp.headers',durable=True,exchange_type=ExchangeType.headers)

message = {
    'key': 'val'
}
channel.basic_publish(exchange='isp.headers',body=json.dumps(message),properties=pika.BasicProperties(
    headers={'domain':'fiber','region':'yangon','event_type':'cut','priority':'high'},
    delivery_mode=2
    ),routing_key='')

connection.close()