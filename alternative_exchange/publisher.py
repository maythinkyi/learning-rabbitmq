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

message = {
    'key': 'val'
}

channel.basic_publish(exchange='isp.topic',body=json.dumps(message), routing_key='a.new.ongingin',properties=pika.BasicProperties(delivery_mode=2))

connection.close()