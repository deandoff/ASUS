from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QMessageBox

from ui.dialogs.create_meeting_wizard import CreateMeetingWizard
from ui.widgets.event_list_widget import EventListWidget


class MainPageWidget(QWidget):
    def __init__(self, meetings, status_bar, parent=None):
        super(MainPageWidget, self).__init__(parent)

        self.meetings = meetings
        self.status_bar = status_bar

        self.layout = QHBoxLayout()

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)

        self.create_meeting_button = QPushButton("Создать совещание")
        self.create_meeting_button.clicked.connect(self.create_meeting)
        self.button_layout.addWidget(self.create_meeting_button)

        self.layout.addLayout(self.button_layout, 1)

        self.events_widget = EventListWidget(self.meetings)
        self.layout.addWidget(self.events_widget, 2)

        self.setLayout(self.layout)



    def create_meeting(self):
        """Открыть окно для создания совещания."""
        dialog = CreateMeetingWizard()
        if dialog.exec() == QDialog.Accepted:
            meeting = dialog.meeting_data
            print(meeting)
            self.meetings.append(meeting)
            print(self.meetings)

            # Обновить виджет расписания с новыми данными
            self.events_widget.populate_events()

            QMessageBox.information(self, "Успех", "Совещание успешно создано!")

    def show_all_meetings(self):
        """Обработчик для отображения всех совещаний."""
        pass
