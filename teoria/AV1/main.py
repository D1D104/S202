import random
import threading
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

db = client['bancoiot']
sensores = db['sensores']

sensores.update_many({}, {"$set": {"valorSensor": 0, "sensorAlarmado": False}})

def tempAleatoria(sensor):
    while True:
        temperatura = random.randint(30,40)
        print(f"Sensor {sensor}: {temperatura} °C")

        sensores.update_one(
            {'nomeSensor': sensor},
            {'$set': {'valorSensor': temperatura}}
        )

        if temperatura > 38:
            sensores.update_one({"nomeSensor": sensor}, {"$set": {"sensorAlarmado": True}})
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {sensor}!")
            break

        time.sleep(1)

sens = ["Temp1", "Temp2", "Temp3"]
threads = []

for sensor in sens:
    thread = threading.Thread(target=tempAleatoria, args=(sensor,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()