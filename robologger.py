from mqtt import MqttSubscriber, MqttPublisher
import config
import json
import time

class RoboLogger:
    def __init__(self):
        self.mqtt_sensor = MqttSubscriber(config.BROKER, config.BROKER_PORT)
        self.mqtt_sensor.change_callback(self.on_sensor_message)
        self.mqtt_sensor.subscribe(config.TOPIC_ROBO_SENSORS)
        self.mqtt_sensor.client.on_connect = self.on_connect
        self.mqtt_sensor.client.on_subscribe = self.on_subscribe
        self.mqtt_publisher = MqttPublisher(config.BROKER, config.BROKER_PORT)
    
    def on_sensor_message(self, client, userdata, msg):
        json_data = json.loads(msg.payload)
        self.log(f"Sensor message: {json_data}")
        distance = json_data['distance']
        if distance < 50:
            self.mqtt_publisher.publish(config.TOPIC_ROBO_MOVEMENT, json.dumps({"motor_left":{"direction":"backward","speed":0},"motor_right":{"direction":"backward","speed":0}}))
            self.log(f"Robo Gestoppt: {distance}")
    def on_connect(self, client, userdata, flags, rc):
        self.log(f"Verbunden: {rc}")
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.log(f"Aboniert: {mid} {granted_qos}")
        

    def close(self):
        self.mqtt_sensor.close()
        self.mqtt_publisher.close()
    
    def log(self,message:str)->None:
        print(f"[{time.time()}]: {message}")
        
    
if __name__ == '__main__':
    robo = RoboLogger()
    input("Press Enter to continue...")
    robo.close()