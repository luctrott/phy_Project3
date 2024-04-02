from TBS1_LM75 import LM75
from TBS1_VL53 import VL53
import config
from mqtt import MqttPublisher
import time
import json

class Sensor_mqtt:
    def __init__(self):
        
        self.vl53 = VL53()
        self.lm75 = LM75(0x48)
        self.mqtt = MqttPublisher(config.BROKER,config.BROKER_PORT)
    
    def get_data(self):
        return self.vl53.distance_mm(), self.lm75.temperature_c()

    def send_data(self):
        data = {
            "distance": self.vl53.distance_mm(),
            "temperature": self.lm75.temperature_c()
        }
        data = json.dumps(data)
        
        self.mqtt.publish(config.TOPIC_ROBO_SENSORS,data)
        print(str(data))
    
    def run(self):
        while True:
            self.send_data()
            #print("Data sent")
            time.sleep(1)
        
        
if __name__ == "__main__":
    sm=Sensor_mqtt()
    sm.run()