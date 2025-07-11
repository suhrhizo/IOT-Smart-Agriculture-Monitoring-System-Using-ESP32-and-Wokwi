import paho.mqtt.client as mqtt
import time
import random
import json

client = mqtt.Client()
client.connect("localhost", 1883)  # Replace with your broker address

while True:
    data = {
        "soil_moisture": random.randint(20, 80),
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": random.randint(40, 90),
        "rainfall": random.choice([0, 1])
    }
    client.publish("smartfarm/data", json.dumps(data))
    print("Published:", data)
    time.sleep(2)
