import time
import paho.mqtt.client as paho
from paho import mqtt
from logic.mqtt.MqttConfig import MqttConfig

class MqttHandler:

    def __init__(self, config: MqttConfig):
        self.config = config

        self.topic = config.topic

        self.__retainedMessages = []

        self.client = paho.Client(client_id=config.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.__on_connect

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(config.username, config.password)

        self.client.on_subscribe = self.__on_subscribe
        self.client.on_message = self.__on_message
        self.client.on_publish = self.__on_publish

        self.client.subscribe(self.topic, qos=config.qos)

    def __on_connect(self, client, userdata, flags, rc, properties=None):
        pass

    def __on_publish(self, client, userdata, mid, properties=None):
        pass

    def __on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        pass

    def __on_message(self, client, userdata, msg):
        self.__retainedMessages.append(msg.payload.decode("utf-8"))

    def publish_message(self, message, retain=False, qos=1):
        self.__delete_old_retained_messages()
        time.sleep(1)
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload=str(message), qos=qos, retain=retain)
        self.client.disconnect()

    def get_retained_message(self):

        self.client.connect(self.config.broker_adress, self.config.port)
        self.client.subscribe(self.config.topic, self.config.qos)
        time.sleep(0.5)
        self.client.loop_start()

        time.sleep(0.5)

        self.client.loop_stop()

        self.client.disconnect()

        retained_messages = self.__retainedMessages.copy()
        self.__retainedMessages.clear()

        return retained_messages[0]

    def __delete_old_retained_messages(self):
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload=None, qos=0, retain=True)
