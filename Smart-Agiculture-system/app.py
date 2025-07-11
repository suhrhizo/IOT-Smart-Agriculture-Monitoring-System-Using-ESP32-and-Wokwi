from flask import Flask, jsonify
from flask_cors import CORS
import paho.mqtt.client as mqtt
import threading
import json

app = Flask(__name__)
CORS(app)

latest_data = {
    "soil_moisture": 0,
    "temperature": 0,
    "humidity": 0,
    "rainfall": 0,
    "pump": "OFF",
    "growth_stage": 1
}

def on_connect(client, userdata, flags, rc):
    client.subscribe("smartfarm/data")

def on_message(client, userdata, msg):
    global latest_data
    data = json.loads(msg.payload)
    latest_data.update(data)

    # Auto-irrigation logic
    if data["soil_moisture"] < 30 and data["rainfall"] == 0:
        latest_data["pump"] = "ON"
        latest_data["growth_stage"] = min(latest_data["growth_stage"] + 1, 5)
    else:
        latest_data["pump"] = "OFF"

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)

threading.Thread(target=mqtt_client.loop_forever).start()

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(debug=True)