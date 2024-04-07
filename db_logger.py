from mqtt import MqttSubscriber
import config
import sqlite3
import time
import json

class SensorSub:
    def __init__(self, broker:str, topic:str, db:str)->None:
        self.client = MqttSubscriber(broker)
        self.db = db
        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.client.change_callback(self.on_message)
        self.client.subscribe(topic)

    def on_message(self, client, userdata, message):
        data = message.payload.decode()
        print(f"received message {data}")
        self.add_to_db(data)
        for i in self.get():
            print(i)

    def add_to_db(self, data):
        data=json.loads(data)
        distance= data["distance"]
        temperature= data["temperature"] 
        self.cur.execute("INSERT INTO sensor_data (tstamp, distance,temperature) VALUES (?,?,?)", (time.time(), distance,temperature))
        self.conn.commit()

    def get(self):
        self.conn.commit()
        self.cur.execute("SELECT * FROM sensor_data")
        return self.cur.fetchall()
        
if __name__ == "__main__":
    sensor = SensorSub(config.BROKER, config.TOPIC_ROBO_SENSORS, config.DB_NAME)
    input("Press Enter to continue...")
    for i in sensor.get():
        print(i)