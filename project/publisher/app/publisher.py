import paho.mqtt.client as mqtt
import time
import random
import json

# Configurazione del broker MQTT
BROKER = "mqtt_broker"  # Nome del servizio nel docker-compose.yml
PORT = 1883
TOPIC_STRUCTURE = "/farm_{farm_id}/plant_{plant_id}/{sensor_type}"  # Struttura del topic



# Lista di piante monitorate

def config_sensors():
    with open('/app/sensors-config/sensors-config.json', 'r') as file:
        return json.load(file)["sensors"]

def config_plants():
    with open('/app/sensors-config/plants-config.json', 'r') as file:
        farms = json.load(file)["farms"]
        plants = [{"farm_id": farm["farm_id"], "plant_id": plant["plant_id"]} for farm in farms for plant in farm["plants"]]
        return plants

# Funzione per generare dati casuali per i sensori
def generate_sensor_data(sensors):
    
    sensor_values = {sensor["name"]: round(random.uniform(sensor["min"], sensor["max"]), 2) for sensor in sensors}
    
    return sensor_values

# Connessione al broker
client = mqtt.Client("Publisher")
client.connect(BROKER, PORT)

# Funzione per pubblicare dati su MQTT
def publish_data(sensors, plants):

    while True:
        for plant in plants:
            values = generate_sensor_data(sensors)
            for sensor_type in values.keys():
                value = values.get(sensor_type)  # Genera il valore per il sensore
                payload = json.dumps({"value": value})  # Serializza solo il valore in JSON
                topic = TOPIC_STRUCTURE.format(farm_id=plant["farm_id"], plant_id=plant["plant_id"], sensor_type=sensor_type)
                client.publish(topic, payload)
        print(f"Published! {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}", flush=True)
        time.sleep(5)  # Attendi 5 secondi prima di inviare nuovi dati

if __name__ == "__main__":
    plants = config_plants()
    print(plants)
    sensors = config_sensors()
    publish_data(sensors, plants)
