# main_app_window.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QDialogButtonBox, \
    QWidget, QDialog
from PySide6.QtCore import Qt
from create_meeting_wizard import CreateMeetingWizard
from meeting_calendar_window import MeetingCalendarWindow
from ui.event_list_widget import EventListWidget


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно приложения")
        self.setGeometry(200, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Список совещаний
        self.meetings = []

        # Центральный виджет
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Виджет с кнопками
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)

        self.create_meeting_button = QPushButton("Создать совещание")
        self.create_meeting_button.clicked.connect(self.create_meeting)
        button_layout.addWidget(self.create_meeting_button)

        self.meeting_calendar_button = QPushButton("Календарь совещаний")
        self.meeting_calendar_button.clicked.connect(self.open_calendar)
        button_layout.addWidget(self.meeting_calendar_button)

        button_layout.addStretch()

        main_layout.addLayout(button_layout, 1)

        # Виджет с расписанием
        schedule_layout = QVBoxLayout()
        self.events_widget = EventListWidget(self.meetings)  # Создаем виджет с событиями
        schedule_layout.addWidget(self.events_widget)

        main_layout.addLayout(schedule_layout, 2)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Статусная строка
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Приложение запущено.")

    def create_meeting(self):
        """Открыть окно для создания совещания."""
        dialog = CreateMeetingWizard()
        if dialog.exec() == QDialog.Accepted:
            meeting = dialog.meeting_data
            self.meetings.append(meeting)

            # Обновить виджет расписания с новыми данными
            self.events_widget.populate_events()

            QMessageBox.information(self, "Успех", "Совещание успешно создано!")

    def open_calendar(self):
        """Открыть окно с календарем совещаний."""
        calendar_window = MeetingCalendarWindow(self.meetings)
        calendar_window.exec()