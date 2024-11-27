from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QMessageBox

from ui.dialogs.create_meeting_wizard import CreateMeetingWizard
from ui.widgets.event_list_widget import EventListWidget


class MainPageWidget(QWidget):
    def __init__(self, meetings, status_bar, parent=None):
        super(MainPageWidget, self).__init__(parent)

        self.meetings = meetings
        self.status_bar = status_bar
        self.calendar_widget = None  # Ссылка на виджет календаря будет передана из MainWindow

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
            self.meetings.append(meeting)

            # Обновить виджет расписания с новыми данными
            self.events_widget.populate_events()

            # Обновить календарь
            if self.calendar_widget:
                self.calendar_widget.update_meetings(self.meetings)

            QMessageBox.information(self, "Успех", "Совещание успешно создано!")
