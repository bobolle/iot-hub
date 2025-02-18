import paho.mqtt.client as mqtt
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

mqttc.connect("iot-hub-mosquitto-1", 1883, 60)
mqttc.subscribe("pico/sensor/distance")

mqttc.loop_forever()
