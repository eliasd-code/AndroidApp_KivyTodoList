from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from logic.storage.TaskStorageHandler import TaskStorageHandler
from logic.mqtt.MqttHandler import MqttHandler
from logic.mqtt.MqttConfig import MqttConfig

from ui.screens.MainScreen import MainScreen
from ui.screens.SettingScreen import SettingScreen

# Die zwei Statements müssen drin bleiben, das sonst
from ui.components.TodolistItem import ToDoListItem


class ToDoApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = MqttConfig.load_from_resource()
        self.mqtt_client = MqttHandler(self.config)

    def build(self):
        Builder.load_file('resources/layout.kv')
        self.icon = 'resources/app_icon.png'
        sm = ScreenManager()

        main_screen = MainScreen(name='main', mqtt_client=self.mqtt_client)
        setting_screen = SettingScreen(name='login', mqtt_client=self.mqtt_client)

        sm.add_widget(main_screen)
        sm.add_widget(setting_screen)

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]
        main_screen.load_tasks_in_local_list(tasks)
        return sm


if __name__ == '__main__':
    ToDoApp().run()
