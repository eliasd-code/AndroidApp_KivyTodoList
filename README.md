**Projektname: ToDoApp**

Dieses Projekt ist eine ToDo-Listen-App, die mit KivyMD erstellt wurde und auf verschiedenen Plattformen wie Android, Windows und Linux ausgeführt werden kann.

**Voraussetzungen:**
- Python 3.x
- KivyMD

**Installation:**
1. Stellen Sie sicher, dass Python 3.x auf Ihrem System installiert ist.
2. Installieren Sie KivyMD, indem Sie den Befehl `pip install kivymd` ausführen.

**Ausführung:**
1. Navigieren Sie zum Projektverzeichnis.
2. Führen Sie die Datei `main.py` aus, indem Sie den Befehl `python main.py` in der Befehlszeile eingeben.

**Beschreibung:**
- Die `ToDoApp` ist eine KivyMD-Anwendung, die eine intuitive Benutzeroberfläche für die Verwaltung von ToDo-Listen bietet.
- Sie können neue Aufgaben erstellen, bestehende bearbeiten und löschen sowie Ihre Einstellungen anpassen.
- Die App verwendet MQTT für die Synchronisierung von Aufgaben zwischen verschiedenen Geräten.

**Struktur des Projekts:**
- `main.py`: Hauptdatei der Anwendung, die die App initialisiert und ausführt.
- `resources/layout.kv`: Datei zur Definition des Layouts der Benutzeroberfläche.
- `logic/storage/TaskStorageHandler.py`: Klasse zur Handhabung der Speicherung von Aufgaben.
- `logic/mqtt/MqttHandler.py`: Klasse zur Handhabung der MQTT-Kommunikation.
- `logic/mqtt/MqttConfig.py`: Klasse zur Konfiguration von MQTT.
- `ui/screens/MainScreen.py`: Klasse für den Hauptbildschirm der App.
- `ui/screens/SettingScreen.py`: Klasse für den Einstellungs-/Konfigurationsbildschirm der App.
- `ui/components/TodolistItem.py`: Klasse für die Anzeige von ToDo-Listenelementen in der Benutzeroberfläche.

**Weitere Informationen:**
Weitere Informationen zur Verwendung der App finden Sie in der jeweiligen Dokumentation der KivyMD-Bibliothek.

**Autor:**
Maximilian Meier, Elias Dafkov, Eric Kaiser

**Kontakt:** Gibts keinen