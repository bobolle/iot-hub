import paho.mqtt.client as mqtt
import psycopg2
import time
import json
import requests
import argparse

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883

DB_NAME = "db"
DB_USER = "db_admin"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = 5432

def on_connect(client, userdata, flags, result_code, properties):
    if result_code.is_failure:
        print(f"connection to mqtt-broker returned with result code {result_code}")
    else:
        print(f"connected to mqtt-broker")
        
        # check if db contains topics to be subscribed to

        client.subscribe("edge/+/sensors/distance")

        # send device_id to cloud in order to manage connection

def on_disconnect(client, userdata, result_code):
    print(f"disconnected with result code {result_code}")
    retry_connection()

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        topic_arr = topic.split('/')
        device_id = topic_arr[1]
        payload = json.loads(msg.payload.decode())

        print(f"message received: {payload}")
        debug_print(device_id)

        send_to_cloud('/data', payload)

    except Exception as e:
        debug_print(f"error on_message: {e}")
    pass

def disconnect_device(client, device_id):
    client.publish(f"edge-device/{device-id}/disconnect", "1")

def send_to_cloud(path, data):
    url = 'http://192.168.1.13:9090/api' + path
    headers = {'Content-Type': 'application/json'}
    json_data = data

    try: 
        r = requests.post(url, headers=headers, json=json_data)
    except Exception as e:
        debug_print(f"sending to cloud failed: {e}")

def retry_connection():
    while True:
        try:
            mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
            mqtt_client.loop_start()
            break
        except Exception as e:
            print(f"reconnection to broker failed")
            time.sleep(5)

def debug_print(msg):
    if args.debug:
        print(f"DEBUG: {msg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try:
        conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}")
        print("init connection to db established")
    except Exception as e:
        print(f"init connection to db failed: {e}")

    try:
        mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"init connection to broker failed: {e}")
        retry_connection()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
