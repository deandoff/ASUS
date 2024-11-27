# main_app_window.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QWidget, QDialog, QMenuBar, QMenu
from PySide6.QtCore import Qt
from ui.dialogs.create_meeting_wizard import CreateMeetingWizard
from meeting_calendar_window import MeetingCalendarWindow
from ui.widgets.event_list_widget import EventListWidget


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно приложения")
        self.setGeometry(200, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Список совещаний
        self.meetings = []

        # Центральный виджет
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)

        # Меню
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Добавление пунктов меню
        file_menu = QMenu("Совещания", self)
        self.menu_bar.addMenu(file_menu)

        # Новый пункт меню для отображения всех совещаний
        view_all_meetings_action = file_menu.addAction("Показать все совещания")
        view_all_meetings_action.triggered.connect(lambda: self.show_all_meetings())

        help_menu = QMenu("Справка", self)
        self.menu_bar.addMenu(help_menu)

        # Виджет с кнопками
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)

        self.create_meeting_button = QPushButton("Создать совещание")
        self.create_meeting_button.clicked.connect(self.create_meeting)
        self.button_layout.addWidget(self.create_meeting_button)

        self.meeting_calendar_button = QPushButton("Календарь совещаний")
        self.meeting_calendar_button.clicked.connect(self.open_calendar)
        self.button_layout.addWidget(self.meeting_calendar_button)

        self.button_layout.addStretch()

        self.main_layout.addLayout(self.button_layout, 1)

        # Виджет с расписанием
        self.events_widget = EventListWidget(self.meetings)  # Создаем виджет с событиями
        self.main_layout.addWidget(self.events_widget, 2)

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

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

    def show_all_meetings(self):
        """Обработчик для отображения всех совещаний."""
        # Скрываем все виджеты в основном макете
        for i in range(self.main_layout.count()):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(False)

        # Создаем новый виджет с расписанием и показываем его
        self.events_widget = EventListWidget(self.meetings)  # Создаем новый виджет с событиями
        self.main_layout.addWidget(self.events_widget)

        # Обновить виджет расписания с новыми данными
        self.events_widget.populate_events()
        self.status_bar.showMessage("Показаны все совещания.")