import time
import json
from kivy.uix.screenmanager import Screen
from logic.storage.TaskStorageHandler import TaskStorageHandler
import uuid as UUID


class MainScreen(Screen):

    def __init__(self, mqtt_client, **kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client

    def load_tasks_in_local_list(self, tasks):
        """
                        Lädt Items in die local list view.

                        Args:
                            tasks: Eine Liste von Item dictionaries, um sie in der Liste darzustellen.
        """
        data = []
        for task in tasks:
            item = {'id': str(task["uuid"]), 'text': task["message"], 'state': task["state"]}
            data.append(item)
        self.ids.rv.data = data

    def add_item(self, uuid=""):
        """
                        Fügt ein neues Item zur Liste hinzu. Generiert eine neue UUID falls noch keine mitgebeben wurde.

                        Args:
                            uuid: Ein optionaler UUID string für das neue Item. Generiert einen neuen wenn dieser leer ist.
        """
        if uuid == "":
            uuid = str(UUID.uuid4())

        text = 'New Task'
        new_item = {'id': uuid, 'text': text, 'state': False}
        self.ids.rv.data.append(new_item)
        self.ids.rv.refresh_from_data()
        TaskStorageHandler._add_task(str(self.mqtt_client.config.client_id), text)
        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(data, True)

    def sync_items(self):
        data = self.mqtt_client.get_retained_message()
        if data[0]:
            try:
                data = json.loads(data.replace("'", "\"").replace("True", "true").replace("False", "false"))
                TaskStorageHandler._write_data(data)
                self.load_tasks_in_local_list(data["tasks"])

            except json.JSONDecodeError as e:
                print("Fehler beim Decodieren der empfangenen Daten:", e)
        else:
            print("Fehler, das hat nicht funktioniert", data)

    def delete_item(self, task_uuid):
        """
                        Löscht ein Item aus der Liste.

                        Args:
                            task_uuid: Der UUID string des Item, das gelöscht werden soll.
        """

        TaskStorageHandler._delete_task(task_uuid)

        self.ids.rv.data = [item for item in self.ids.rv.data if item['id'] != task_uuid]

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]
        self.load_tasks_in_local_list(tasks)

        self.mqtt_client.publish_message(data, True)

    def edit_item(self, item_widget):
        """
                        Initiiert den Bearbeitungsprozess für ein Item.

                        Args:
                            item_widget: Die Widget Instanz des Items das bearbeitet werden soll.
        """
        self.selected_item_id = item_widget.id
        self.ids.global_edit_text.text = item_widget.text
        self.ids.global_edit_text.disabled = False
        self.ids.global_edit_text.opacity = 1
        self.ids.global_edit_text.focus = True


    def apply_global_edit(self):
        """
                        Wendet die in dem Textinput vorgenommenen Änderungen auf das ausgewählte item an.
        """
        new_text = self.ids.global_edit_text.text

        for item in self.ids.rv.data:
            if item['id'] == self.selected_item_id:
                item['text'] = new_text
                break

        self.ids.rv.refresh_from_data()

        TaskStorageHandler._set_task_text(self.selected_item_id, text=self.ids.global_edit_text.text)
        time.sleep(1)
        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(data, True)

        self.ids.global_edit_text.text = ''
        self.ids.global_edit_text.opacity = 0
        self.ids.global_edit_text.disabled = True
        self.selected_item_id = None
