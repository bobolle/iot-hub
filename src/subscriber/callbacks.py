import json
from cloud.sender import send_to_cloud

def on_connect(client, userdata, flags, result_code, properties):
    client.subscribe("edge/+/sensors/+")

def on_message(client, userdata, msg):
    topics = msg.topic.split('/')

    device_type = topics[0]
    device_id = topics[1]
    sensor_type = topics[3]
    
    edge_json_data = json.loads(msg.payload.decode('utf-8'))

    payload = {
            'device_id': device_id,
            'sensor_type': sensor_type,
            'value': json_object['value']
    }

    print(payload)
    
    #create funciton for sending data to db

    #try:
    #    //cursor = conn.cursor()
    #    //cursor.execute()
    #    //conn.commit()
    #except Exception as e:
    #    print(f"error: on_message, {e}")

    send_to_cloud('/data', json.dumps(payload))
