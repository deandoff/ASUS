from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QMessageBox, QLabel
from ui.dialogs.create_meeting_wizard import CreateMeetingWizard
from ui.widgets.brief_info_widget import BriefInfoWidget
from ui.widgets.event_list_widget import EventListWidget


class MainPageWidget(QWidget):
    def __init__(self, meetings, status_bar, user_data, parent=None):
        super(MainPageWidget, self).__init__(parent)

        self.user_data = user_data

        self.meetings = meetings
        self.status_bar = status_bar
        self.calendar_widget = None

        self.layout = QHBoxLayout()

        # Создание и добавление виджета с событиями
        self.events_widget = EventListWidget(self.meetings)
        self.layout.addWidget(self.events_widget, 3)

        # Подключение сигнала выбора события к методу обновления BriefInfoWidget
        self.events_widget.event_selected.connect(self.update_brief_info)

        # Создание контейнера для BriefInfoWidget и кнопок
        self.main_info_layout = QVBoxLayout()

        # Создание виджета краткой информации
        self.brief_info = BriefInfoWidget(None)
        self.main_info_layout.addWidget(self.brief_info)

        # Кнопки для создания и изменения совещания

        self.create_meeting_button = QPushButton("Создать совещание")
        self.create_meeting_button.clicked.connect(self.create_meeting)
        self.create_meeting_button.setStyleSheet("""font-family: Roboto Slab; 
                                                 font-size: 17px; 
                                                 color: white; 
                                                 background-color: black; 
                                                 border: 2px solid black; 
                                                 border-radius: 10px; 
                                                 padding: 5px; 
            """)
        self.main_info_layout.addWidget(self.create_meeting_button)

        self.update_meeting_button = QPushButton("Изменить совещание")
        self.update_meeting_button.clicked.connect(self.update_meeting)
        self.update_meeting_button.setStyleSheet("""font-family: Roboto Slab; 
                                                         font-size: 17px; 
                                                         color: white; 
                                                         background-color: black; 
                                                         border: 2px solid black; 
                                                         border-radius: 10px; 
                                                         padding: 5px; 
                    """)
        self.main_info_layout.addWidget(self.update_meeting_button)

        # Добавление основного контейнера с BriefInfo и кнопками в основное окно
        self.layout.addLayout(self.main_info_layout, 2)

        self.setLayout(self.layout)


    def create_meeting(self):
        """Открыть окно для создания совещания."""
        dialog = CreateMeetingWizard(self.user_data)
        if dialog.exec() == QDialog.Accepted:
            meeting = dialog.meeting_data
            self.meetings.append(meeting)
            # Обновить виджет расписания с новыми данными
            self.events_widget.populate_events()

            # Обновить календарь
            if self.calendar_widget:
                self.calendar_widget.update_meetings(self.meetings)

            QMessageBox.information(self, "Успех", "Совещание успешно создано!")

    def update_meeting(self):
        pass

    def update_brief_info(self, event):
        """Обновляет краткую информацию при выборе события."""
        self.brief_info.update_info(event)

