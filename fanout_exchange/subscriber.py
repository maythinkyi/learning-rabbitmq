import pika
import json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

# Declare exchange with fanout type, all queues attached to that exchange will consumer the message

channel.exchange_declare(exchange='device_events_exchange', exchange_type=ExchangeType.fanout,durable=True)

channel.queue_declare(queue='notification',durable=True)
channel.queue_bind(queue='notification',exchange='device_events_exchange',routing_key='')

channel.queue_declare(queue='audit_log',durable=True)
channel.queue_bind(queue='audit_log',exchange='device_events_exchange',routing_key='')

channel.queue_declare(queue='monitoring',durable=True)
channel.queue_bind(queue='monitoring',exchange='device_events_exchange',routing_key='')

def on_notification_callback(ch,method,properties,body):
    print(f'[x] Notitification received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_audit_log_callback(ch,method,properties,body):
    print(f'[x] Audit_log received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_monitoring_callback(ch,method,properties,body):
    print(f'[x] Monitoring received: {json.loads(body)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='notification',on_message_callback=on_notification_callback)
channel.basic_consume(queue='audit_log',on_message_callback=on_audit_log_callback)
channel.basic_consume(queue='monitoring',on_message_callback=on_monitoring_callback)

channel.start_consuming()