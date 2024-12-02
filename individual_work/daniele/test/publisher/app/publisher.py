import paho.mqtt.client as mqtt
import time
import random
import json

# Configurazione del broker MQTT
BROKER = "mqtt_broker"  # Nome del servizio nel docker-compose.yml
PORT = 1883
TOPIC_STRUCTURE = "/farm_{farm_id}/plant_{plant_id}/{sensor_type}"  # Struttura del topic

# Lista di piante monitorate
PLANTS = [
    {"farm_id": "1", "plant_id": "001"},
    {"farm_id": "1", "plant_id": "002"},
    {"farm_id": "2", "plant_id": "003"},
]

# Funzione per generare dati casuali per i sensori
def generate_sensor_data(sensor_type):
    sensor_values = {
        "temperature": round(random.uniform(15.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "chlorophyll_content": round(random.uniform(40.0, 70.0), 2),
        "ph_level": round(random.uniform(5.5, 7.0), 2),
        "height": round(random.uniform(50.0, 150.0), 2),  # Altezza in cm
        "canopy_density": round(random.uniform(0.5, 1.0), 2),  # Percentuale
    }
    return sensor_values.get(sensor_type)

# Connessione al broker
client = mqtt.Client("Publisher")
client.connect(BROKER, PORT)

# Funzione per pubblicare dati su MQTT
def publish_data():
    sensor_types = ["temperature", "humidity", "chlorophyll_content", "ph_level", "height", "canopy_density"]
    while True:
        for plant in PLANTS:
            for sensor_type in sensor_types:
                value = generate_sensor_data(sensor_type)  # Genera il valore per il sensore
                payload = json.dumps({"value": value})  # Serializza solo il valore in JSON
                topic = TOPIC_STRUCTURE.format(farm_id=plant["farm_id"], plant_id=plant["plant_id"], sensor_type=sensor_type)
                client.publish(topic, payload)
        print(f"Published! {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}", flush=True)
        time.sleep(5)  # Attendi 5 secondi prima di inviare nuovi dati

if __name__ == "__main__":
    publish_data()
