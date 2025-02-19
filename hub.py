import paho.mqtt.client as mqtt
import psycopg2
import time

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"connected with result code {reason_code}")
    else:
        #client.subscribe("$SYS/#")
        print(f"connected")

def on_message(client, userdata, msg):
    print(f"message received: {msg.payload.decode()}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("broker", 1883, 60)
mqttc.subscribe("pico/sensor/distance")

conn = psycopg2.connect("dbname=db user=db_admin password=1234 host=db port=5432")

mqttc.loop_forever()
