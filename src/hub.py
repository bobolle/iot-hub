from subscriber.client import MQTTClient
import psycopg2
import time
import argparse

# too lazy to store these in a better way right now

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883

DB_NAME = "db"
DB_USER = "db_admin"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = 5432

def debug_print(msg):
    if args.debug:
        print(f"DEBUG: {msg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    try:
        conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}")
        print("init connection to db established")
    except Exception as e:
        print(f"init connection to db failed: {e}")

    client = MQTTClient(BROKER_ADDRESS, BROKER_PORT)
    client.connect()
    client.start_loop()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.stop_loop()
        client.disconnect()
