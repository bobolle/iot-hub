import paho.mqtt.client as mqtt
from subscriber.callbacks import *

class MQTTClient:
    def __init__(self, broker, port):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.broker = broker
        self.port = port

        self.set_callbacks()

    def set_callbacks(self):
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            print(f"init connection to broker established")
        except Exception as e:
            print(f"init connection to broker failed: {e}")
    
    def start_loop(self):
        self.client.loop_start()

    def stop_loop(self):
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
