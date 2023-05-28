
import paho.mqtt.client as mqtt 

class Communication:
    def __init__(self,message=None):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('127.0.0.1',1883, keepalive=60)
        self.mqtt_client.loop_start()
        self.mqtt_client.on_connect = self.on_connect

        self.mqtt_client.message_callback_add('service/topic', self.on_message_topic)
        self.mqtt_client.subscribe('service/#')
        self.msg_topic=''
        self.update_topic= False


    def on_message_topic(self, client, userdata, message):
        self.msg_topic = message.payload
        self.update_topic = True

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed")
