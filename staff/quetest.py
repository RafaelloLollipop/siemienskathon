from amqplib import client_0_8 as amqp


queue_name = "Game1"
queue_exchange = "Game1"
queue_rooting_key = "Game1"
consumer_tag = "Game1"


# connect to server
lConnection = amqp.Connection(host="localhost:5672", userid="guest", password="guest", virtual_host="/", insist=False)
lChannel = lConnection.channel()

lChannel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)
lChannel.exchange_declare(exchange=queue_exchange, type="direct", durable=True, auto_delete=False)
lChannel.queue_bind(queue=queue_name, exchange=queue_exchange, routing_key=queue_rooting_key)

def data_receieved(msg):
     print('Received: ' + msg.body)
lChannel.basic_consume(queue=queue_name, no_ack=True, callback=data_receieved, consumer_tag=consumer_tag)

while True:
     lChannel.wait()

lChannel.basic_cancel(consumer_tag)

lChannel.close()
lConnection.close()
