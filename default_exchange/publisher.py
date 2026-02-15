import pika
import json

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq')

connection = pika.BlockingConnection(parameters=connection_parameters)

channel = connection.channel()

# Default exchange -> get the message + RK

register_message = {
    "device_id": "DEV001",
    "mac": "AA:BB:CC:DD:EE:FF",
    "serial": "SN123456"
}

channel.basic_publish(exchange='',routing_key='device_registration',body=json.dumps(register_message),properties=pika.BasicProperties(delivery_mode=2))

log_message = {
    "device_id": "DEV001",
    "status": "ONLINE"
}
channel.basic_publish(exchange='',routing_key='device_log',body=json.dumps(log_message),properties=pika.BasicProperties(delivery_mode=2))

print('[x]: Message sent to both Device Registration and Device Log System.')

connection.close()