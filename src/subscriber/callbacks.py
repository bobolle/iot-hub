import json
from cloud.sender import send_to_cloud

def on_connect(client, userdata, flags, result_code, properties):
    client.subscribe("edge/+/sensors/distance")

def on_message(client, userdata, msg):
    topics = msg.topic.split('/')

    device_type = topics[0]
    device_id = topics[1]

    #create funciton for sending data to db

    #try:
    #    //cursor = conn.cursor()
    #    //cursor.execute()
    #    //conn.commit()
    #except Exception as e:
    #    print(f"error: on_message, {e}")

    #payload = json.loads(msg.payload.decode())
    send_to_cloud('/data', msg.payload)
