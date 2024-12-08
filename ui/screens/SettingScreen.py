from kivy.uix.screenmanager import Screen
from logic.mqtt.MqttConfig import MqttConfig
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import re
import sys
class SettingScreen(Screen):

    def __init__(self, mqtt_client,**kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client


    def is_valid(self, username, password, broker_adress, port, topic):
        """
                                Checkt ob MQTT Parameter korrekt sind bevor die config editiert wird.

                                Args:
                                    username: Eingabe des Benutzernamens.
                                    password: Eingabe des Passworts.
                                    broker_address: Die Broker-Adresse des MQTT.
                                    port: Der Port über den eine Verbindung hergestellt werden soll.
                                    topic: Das Topic zu dem subscribed werden soll.
        """

        if not (username and password and broker_adress and port and topic):
            return False

        if not str(port).isdigit():
            return False

        if not re.search(r'[#/]', topic):
            return False

        return True

    def update_config_json(self, username_input, password_input, broker_adress_input, port_input, topic_input):
        """
                        Setzt neue Parameter zur Verbindung mit dem MQTT-Broker.

                        Args:
                            username_input: Eingabe des Benutzernamens.
                            password_input: Eingabe des Passworts.
                            broker_adress_input: Die Broker-Adresse des MQTT.
                            port_input: Der Port über den eine Verbindung hergestellt werden soll.
                            topic_input: Das Topic zu dem subscribed werden soll.
        """
        username_input = username_input.text
        password_input = password_input.text
        broker_adress_input = broker_adress_input.text
        port_input = port_input.text
        topic_input = topic_input.text

        if self.is_valid(username_input, password_input, broker_adress_input, port_input, topic_input):

            mqtt_config = {
                "mqtt": {
                    "client-id": "703601b0-cc92-4826-b06a-2fe3d034b502",
                    "connection": {
                        "broker-adress": broker_adress_input,
                        "port": int(port_input),
                        "qos": 1,
                        "topic": topic_input
                    },
                    "user": {
                        "username": username_input,
                        "password": password_input
                    }
                }
            }

            MqttConfig.write(mqtt_config)
            self.show_shutdown_dialog()
        else:
            print("Es stehen keine Configs bereit")

    def show_shutdown_dialog(self):
        """
                    Zeigt eine Popup mit der Aufforderung die App neu zu starten damit die neue Verbindung hergestellt wird.

        """
        if not hasattr(self, 'shutdown_dialog'):
            self.shutdown_dialog = MDDialog(
                title="Neustart Benachrichtung",
                text="Bitte starten sie die App neu.",
                buttons=[
                    MDFlatButton(
                        text="Okay",
                        on_release=self.shutdown_app
                    ),
                ],
            )
        self.shutdown_dialog.open()

    def shutdown_app(self, *args):
        self.shutdown_dialog.dismiss()
        sys.exit()