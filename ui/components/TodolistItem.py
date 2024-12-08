from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import ObjectProperty

from logic.storage.TaskStorageHandler import TaskStorageHandler


class ToDoListItem(BoxLayout):
    checkbox = ObjectProperty(None)
    id = StringProperty('')
    text = StringProperty('')
    state = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ToDoListItem, self).__init__(**kwargs)
        self.press_event = None

    def refresh_view_attrs(self, rv, index, data):
        """
                        Aktualisiert die Todo-Liste mit den gegebenen Informationen aus der tasks.json.

                        Args:
                            rv: Die RecycleView Instanz die, die Task beinhaltet.
                            index: Der Index der Task in der RecycleView Daten Liste.
                            data: Ein Dictionary welches die Datenattribute für die Task beinhalten.
        """
        self.ids.edit_button.opacity = 0
        self.ids.edit_button.disabled = True
        self.ids.delete_button.opacity = 0
        self.ids.delete_button.disabled = True

        self.ids.checkbox.active = data.get('state', False)
        return super(ToDoListItem, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """
                        Kümmert sich um das Event sobald eine Berührung gehalten wird. Wenn die Berührung auf einem Item stattfindet, werden die Buttons der Task angezeigt.

                        Args:
                            touch: Berührungs-Event.
        """
        if self.collide_point(*touch.pos):

            self.hide_buttons_other_items()

            self.press_event = Clock.schedule_once(lambda dt: self.show_buttons(), 0.5)
        return super(ToDoListItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        """
                        Wird die Berührung vor einer Sekunde losgelassen, wird das Event abgebrochen.
        """
        if self.press_event:

            Clock.unschedule(self.press_event)
            self.press_event = None
        return super(ToDoListItem, self).on_touch_up(touch)

    def show_buttons(self, *args):
        """
                        Macht den edit und delete button sichtbar für das Item.
        """
        self.ids.edit_button.opacity = 1
        self.ids.edit_button.disabled = False
        self.ids.delete_button.opacity = 1
        self.ids.delete_button.disabled = False

    def hide_buttons(self):
        """
                        Versteckt den edit und delete button für das Item.
        """
        self.ids.edit_button.opacity = 0
        self.ids.edit_button.disabled = True
        self.ids.delete_button.opacity = 0
        self.ids.delete_button.disabled = True

    def hide_buttons_other_items(self):
        """
                        Versteckt den edit und delete button des Items, für alle Items außer dem berührten.
        """
        current_screen = App.get_running_app().root.current_screen
        if hasattr(current_screen, 'ids') and 'rv' in current_screen.ids:
            for item in current_screen.ids.rv.children[0].children:
                if item != self:
                    item.hide_buttons()

    def on_checkbox_change(self, checkbox, value):
        """
                        Aktualisiert das Item mit dem neuen Status, wenn die checkbox betätigt wird.

                        Args:
                            checkbox: Die checkbox Instanz.
                            value: Der neue Boolean Wert der checkbox.
        """
        item_uuid = None
        for item in App.get_running_app().root.get_screen('main').ids.rv.data:
            task_uuid = item['id']
            if task_uuid == self.id:
                item_uuid = item['id']

        if item_uuid:
            TaskStorageHandler._set_task_state(item_uuid, bool(checkbox.active))
        else:
            print("Ein Fehler ist aufgetreten. Der Checkbox Status konnte nicht aktualisiert werden.")

    def on_data(self, *args):
        """
                        Sorgt dafür das die checkbox den korekten Zustand anzeigt, wenn sich die Daten des Items ändern.
        """
        self.ids.checkbox.active = self.state