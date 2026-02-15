#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials(username='guest',password='guest'),virtual_host='mtk_rbmq'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def calculate_billing(customer_id):
   return json.dumps({
    "status": "success",
    "credit_score": 700,
    "eligible": True
    })

def on_request(ch, method, props, body):
    customer_id = int(body)

    print(f" [.] Customer_id({customer_id})")
    response = calculate_billing(customer_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()