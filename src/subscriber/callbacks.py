import json
import datetime
from cloud.sender import send_to_cloud

def on_connect(client, userdata, flags, result_code, properties):
    client.subscribe("edge/+/sensors/distance")

def on_message(client, userdata, msg):
    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    topics = msg.topic.split('/')

    device_type = topics[0]
    device_id = topics[1]
    
    json_object = json.loads(msg.payload.decode('utf-8'))



    payload = {
            'device_id': device_id,
            'data': json_object['value'],
            'timestamp': timestamp
    }
    
    #create funciton for sending data to db

    #try:
    #    //cursor = conn.cursor()
    #    //cursor.execute()
    #    //conn.commit()
    #except Exception as e:
    #    print(f"error: on_message, {e}")

    send_to_cloud('/data', json.dumps(payload))
