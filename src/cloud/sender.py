import requests

def send_to_cloud(path, data):
    url = 'http://192.168.1.13/9090/api' + path
    headers = {'Content-Type': 'application/json'}

    try:
        requests.post(url, headers=headers, data=data)
    except Exception as e:
        print(f"sending to cloud failed: {e}")
