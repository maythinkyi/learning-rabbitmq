import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

# Declare exchange with fanout type, in subscriber side all queues attached to that exchange will consume the message

exchange = channel.exchange_declare(exchange='device_events_exchange',exchange_type=ExchangeType.fanout, durable=True)

event = {
    "device_id": "DEV001",
    "status": "OFFLINE"
}

channel.basic_publish(exchange='device_events_exchange',body=json.dumps(event),properties=pika.BasicProperties(delivery_mode=2),routing_key='')

connection.close()