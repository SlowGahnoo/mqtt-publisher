from paho.mqtt import client as mqtt_client
import random
import time
import logging

class Client:
    def __init__(self, id):
        self.id = f"python-mqtt-{id}"

    def connect(self, broker, port = 1883, topic = "/python/mqtt/"):
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
        self.client.disconnect()

        
class Publisher(Client):
    def __init__(self, id):
        super().__init__(id)

    def create_message(self, message):
        self.message = message 

    def publish(self):
        result = self.client.publish(self.topic, self.message)
        status = result[0]
        if status == 0:
            logging.info(f"Sent: {self.message}")
        else:
            logging.error(f"Failed to send message to topic {self.topic}")

class Subscriber(Client):
    def __init__(self, id):
        super().__init__(id)

    def subscribe(self):
        def on_message(client, userdata, msg):
            logging.info(f"Received: {msg.payload.decode()}")
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        self.client.loop_forever()

def run1():
    p = Publisher(random.randint(0, 1000))
    p.connect(broker = 'broker.emqx.io', topic = '/python/mqtt/')
    try:
        while True:
            p.create_message(input(">> "))
            p.publish()
    except EOFError:
        return

def run2():
    c = Subscriber(random.randint(0, 1000))
    c.connect(broker = 'broker.emqx.io', topic = '/python/mqtt/')
    c.subscribe()

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
