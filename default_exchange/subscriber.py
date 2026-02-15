import pika
import json

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='device_registration',durable=True)
channel.queue_declare(queue='device_log',durable=True)

def callback_1(ch,method,properties,body):
    print('[x]: device_registration Received > ', json.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_2(ch,method,properties,body):
    print('[x]: device_log Received > ',json.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='device_registration',on_message_callback=callback_1)
channel.basic_consume(queue='device_log',on_message_callback=callback_2)

channel.start_consuming()