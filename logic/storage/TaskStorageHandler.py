import json
import uuid

from logic.mqtt.MqttConfig import MqttConfig
from logic.mqtt.MqttHandler import MqttHandler

tasks_data_path = "resources/tasks.json"

mqtt_config = MqttConfig.load_from_resource()
mqtt_client = MqttHandler(mqtt_config)


class TaskStorageHandler:
    """
                Klasse zur Verwaltung von Aufgaben in einer JSON-Datei.
    """

    @staticmethod
    def _add_task(client_id, message):
        """
                    Fügt eine neue Aufgabe zur Aufgabenliste hinzu.

                    client_id: Die ID des Clients, der die Aufgabe erstellt.
                    message: Die Nachricht oder Beschreibung der Aufgabe.
        """
        try:

            with open(tasks_data_path, "r") as file:
                data = json.load(file)

                task: dict = {
                    "uuid": str(uuid.uuid4()),
                    "client-id": str(client_id),
                    "message": message,
                    "state": False
                }

                data["tasks"].append(task)

                TaskStorageHandler._write_data(data)

        except Exception as e:
            print("Es ist ein Fehler beim hinzufügen des Tasks aufgetreten:", message, e)

    @staticmethod
    def _set_task_state(uuid, state: bool):
        """
                    Aktualisiert den Status einer Aufgabe.

                    uuid: Die eindeutige ID der Aufgabe, deren Status aktualisiert werden soll.
                    state: Der neue Status der Aufgabe (True oder False).
                    Exception: Wirft eine Ausnahme, wenn der Status der Aufgabe nicht aktualisiert werden kann.
        """
        try:
            with open(tasks_data_path, "r") as read_file:
                data = json.load(read_file)

                tasks = data["tasks"]

                for index, task in enumerate(tasks):

                    if task.get('uuid') == uuid:
                        task['state'] = state
                        with open(tasks_data_path, "w") as write_file:
                            json.dump(data, write_file, indent=4)
                            write_file.close()
                read_file.close()

                mqtt_client.publish_message(data, True)

        except Exception as e:
            print(f"Status des Task konnte nicht aktuallisert werden:", uuid, state, e)

    @staticmethod
    def _read_data():
        """
                    Liest die Daten aus der JSON-Datei.

                    return: Die geladenen Daten als Dictionary.
        """
        try:
            with open(tasks_data_path, "r") as file:
                file.seek(0)
                return json.load(file)
        except Exception as e:
            print("Es ist ein Fehler beim Lesen der Datei aufgetreten:", e)

    @staticmethod
    def _write_data(data):
        """
                    Schreibt Daten in die JSON-Datei.

                    data: Die zu schreibenden Daten.
        """
        try:
            with open(tasks_data_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print("Es ist ein Fehler beim Schreiben der Datei aufgetreten:", e)

    @staticmethod
    def _delete_task(task_uuid):
        """
                    Löscht eine Aufgabe anhand ihrer UUID.

                    task_uuid: Die UUID der zu löschenden Aufgabe.
        """
        try:
            with open(tasks_data_path, "r") as read_file:
                data = json.load(read_file)

                tasks = data["tasks"]

                for index, task in enumerate(tasks):

                    if task.get('uuid') == task_uuid:
                        del tasks[index]
                        data["tasks"] = tasks
                        with open(tasks_data_path, "w") as write_file:
                            json.dump(data, write_file, indent=4)
                            write_file.close()
                read_file.close()
        except Exception as e:
            print("Es ist ein Fehler beim Löschen des Tasks aufgetreten:", e)

    @staticmethod
    def _set_task_text(task_uuid, text):
        """
                    Aktualisiert den Text einer Aufgabe.

                    task_uuid: Die UUID der zu aktualisierenden Aufgabe.
                    text: Der neue Text der Aufgabe
        """
        try:
            with open(tasks_data_path, "r") as read_file:
                data = json.load(read_file)
                tasks = data.get("tasks", [])
                for task in tasks:
                    if task.get('uuid') == task_uuid:
                        task['message'] = text
                        break
                with open(tasks_data_path, "w") as write_file:
                    json.dump(data, write_file, indent=4)
        except Exception as e:
            print("Fehler beim Bearbeiten der Task Message:", e)
