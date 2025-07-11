import firebase_admin
from firebase_admin import credentials, firestore
import random
import time
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_sensor_data():
    # Day/night cycle
    hour = datetime.now().hour
    is_day = 6 <= hour < 18
    light = random.uniform(50000, 100000) if is_day else random.uniform(0, 1000)
    
    # Weather simulation
    is_raining = random.random() < 0.2  # 20% chance of rain
    rain = random.uniform(5, 15) if is_raining else 0
    
    # Soil moisture dynamics
    moisture = max(10, random.uniform(30, 80) - (0 if is_raining else random.uniform(1, 3)))
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": round(moisture, 2),
        "soil_temperature": round(random.uniform(15, 30), 2),
        "air_temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 90), 2),
        "light_intensity": round(light, 2),
        "rainfall": round(rain, 2)
    }

# Send data every 5 seconds
while True:
    data = generate_sensor_data()
    db.collection("sensor_data").add(data)
    print("Data sent:", data)
    time.sleep(5)