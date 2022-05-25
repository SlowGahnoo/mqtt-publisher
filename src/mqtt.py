from paho.mqtt import client as mqtt_client
import random
import time
import logging

class Client:
    def __init__(self, id):
        self.id = f"python-mqtt-{id}"

    def connect(self, broker, port = 1883, topic = "/python/mqtt/"):
        """ Connect to MQTT broker """
        self.topic = topic
        logging.info("Connecting to MQTT Broker")
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker")
            else:
                logging.error("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(self.id)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)

    def disconnect(self):
        """ Disconnect from MQTT broker """
        self.client.disconnect()

        
class Publisher(Client):
    def __init__(self, id):
        super().__init__(id)
        self.message = ""

    def create_message(self, message):
        """ Prepare a message to publish """
        self.message = message

    def publish(self):
        """ Publish the prepared message """
        result = self.client.publish(self.topic, self.message)
        status = result[0]
        if status == 0:
            logging.info(f"Sent: {self.message}")
        else:
            logging.error(f"Failed to send message to topic {self.topic}")
        self.message = ""

class Subscriber(Client):
    def __init__(self, id):
        super().__init__(id)

    def subscribe(self):
        """ Start receiving messages from publisher of topic """
        def on_message(client, userdata, msg):
            logging.info(f"Received: {msg.payload.decode()}")
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        self.client.loop_forever()

# broker, topic = 'broker.emqx.io', '/python/mqtt/'
default_broker, default_topic = 'test.mosquitto.org', '/python/mqtt/'

def run1():
    p = Publisher(random.randint(0, 1000))
    p.connect(broker = default_broker, topic = default_topic)
    try:
        while True:
            p.create_message(input(">> "))
            p.publish()
    except EOFError:
        return

def run2():
    c = Subscriber(random.randint(0, 1000))
    c.connect(broker = default_broker, topic = default_topic)
    try:
        c.subscribe()
    except KeyboardInterrupt:
        return

import sys
if __name__ == "__main__":
    logging.basicConfig(
            level = logging.DEBUG, 
            format = '[%(levelname)s] %(asctime)s - %(message)s'
            )
    if len(sys.argv) > 1:
        if sys.argv[1] == "p":
            run1()
        elif sys.argv[1] == "s":
            run2()
        else:
            exit(0)
