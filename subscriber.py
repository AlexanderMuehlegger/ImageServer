import paho.mqtt.client as mqtt
import time
from datetime import date, datetime

import keys

def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def on_message(client, userdata, message):
    print(f"[{date.today()} {get_time()}] Message received: ", str(message.payload.decode("utf-8")))

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("CONNECTION established")
    else:
        print("authentication error!")

def on_log(client, userdata, level, buf):
    print("log: ", buf)

if __name__ == '__main__':
    client = mqtt.Client('sub')
    client.on_connect = on_connect
    client.username_pw_set(keys.username, keys.pw)
    client.connect(keys.ip, port=keys.port)
    client.subscribe("foto/taken/dev0")

    client.loop_start()
    client.on_message = on_message
    client.on_log = on_log

    time.sleep(100000)
    client.loop_stop()
    print("EXIT")