import paho.mqtt.client as mqtt
import psycopg2
import time
import json
import requests

def on_connect(client, userdata, flags, result_code, properties):
    if result_code.is_failure:
        print(f"connection to mqtt-broker returned with result code {result_code}")
    else:
        print(f"connected to mqtt-broker")
        mqtt_client.subscribe("pico/sensor/distance")
        # send device_id to cloud in order to manage connection

def on_disconnect(client, userdata, result_code):
    print(f"disconnected with result code {result_code}")
    retry_connection()

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"message received: {payload}")

        #cur = conn.cursor()
        #sql = f"INSERT INTO device (name) VALUES ('{payload}')"
        #cur.execute(sql)
        #conn.commit()

        send_to_cloud('/data', payload)

    except Exception as e:
        print(f"error on_message: {e}")
    pass

def calc_avg():
    return avg;

def disconnect_device(client, device_id):
    client.publish(f"edge-device/{device-id}/disconnect", "1")

def send_to_cloud(path, data):
    url = 'http://192.168.1.13:9090/api' + path
    headers = {'Content-Type': 'application/json'}
    json_data = data

    r = requests.post(url, headers=headers, json=json_data)
    return r

def retry_connection():
    while True:
        try:
            mqtt_client.connect("localhost", 1883, 60)
            mqtt_client.loop_forever()
            break
        except Exception as e:
            print(f"reconnection to broker failed")
            time.sleep(5)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    conn = psycopg2.connect("dbname=db user=db_admin password=1234 host=localhost port=5432")
    print("init connection to db established")
except Exception as e:
    print(f"init connection to db failed: {e}")

try:
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_forever()
except Exception as e:
    print(f"init connection to broker failed: {e}")
    retry_connection()

