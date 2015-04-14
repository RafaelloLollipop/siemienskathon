from amqplib import client_0_8 as amqp

# connect to server
lConnection = amqp.Connection(host="localhost:5672", userid="guest", password="guest", virtual_host="/", insist=False)
lChannel = lConnection.channel()

# Create a message
lMessage = amqp.Message("Test messsage!")

# Send message as persistant.  This means it will survive a reboot.
lMessage.properties["delivery_mode"] = 2

# publish the message on the exchange
lChannel.basic_publish(lMessage, exchange="Game2", routing_key="Game2")

# Close connection 
lChannel.close()
lConnection.close()

