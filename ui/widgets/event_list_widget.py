from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtCore import QSize, Qt, QTimer, QTime, QDate
from plyer import notification

import psycopg2
db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"


class EventListWidget(QWidget):
    event_selected = Signal(dict)  # Сигнал, передающий данные выбранного события

    def __init__(self, events, parent=None):
        super().__init__(parent)

        self.events = events
        self.upcoming_event_timer = QTimer(self)  # Таймер для уведомлений
        self.upcoming_event_timer.timeout.connect(self.check_upcoming_events)
        self.upcoming_event_timer.start(60000)  # Проверяем каждые 60 секунд

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Ближайшие совещания")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont('Roboto Slab', 14))
        self.layout.addWidget(self.title_label)

        self.events_list = QListWidget()
        self.events_list.itemClicked.connect(self.show_event_details)
        self.events_list.setStyleSheet("""
            QListWidget {
                background-color: #F0FFFF;
                border-radius: 4px;
                padding: 8px;
                border-style: solid;
                border-width: 2px;
                border-color: #000000;
                font-family: Roboto Slab;
                font-size: 16px;
            }
            QListWidget::item {
                background-color: #E0FFFF;
                border: 1px solid #e0e0e0;
                margin: 5px;
                padding: 10px;
                border-radius: 8px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e0f7fa;
                border: 1px solid #4fc3f7;
            }
        """)

        self.populate_events()
        self.layout.addWidget(self.events_list)

    def check_upcoming_events(self):
        """Проверяет и уведомляет о ближайших событиях."""
        today = QDate.currentDate()
        now = QTime.currentTime()
        for event in self.events:
            event_time = QTime.fromString(event["time"], "HH:mm")
            event_date = QDate.fromString(event["date"], "dd.MM.yyyy")
            time_difference = now.secsTo(event_time) // 60  # Разница в минутах
            # Уведомляем, если событие начинается через 15 минут
            if event_date == today and 14 <= time_difference <= 15:
                self.send_notification(event)

    def send_notification(self, event):
        """Отправляет уведомление через plyer."""
        notification.notify(
            title=f"Напоминание: {event['title']}",
            message=f"Событие начнётся в {event['time']}.",
            timeout=10  # Уведомление исчезнет через 10 секунд
        )

    def populate_events(self):
        self.events_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.events_list.clear()
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    m.id AS meeting_id,
                    m.theme,
                    c.date,
                    c.time
                FROM 
                    Meetings m
                JOIN 
                    Calendar c ON m.id = c.meeting_id
                Order by c.date asc, c.time asc;
            """)
            events = cursor.fetchall()
        except Exception as e:
            print(e)
            return

        for event in events:
            meeting_id, theme, date, time = event  # Extract the description

            item_widget = QWidget()
            item_layout = QVBoxLayout()
            item_layout.setContentsMargins(10, 10, 10, 10)

            date_label = QLabel(f"<b>{date}</b>")
            date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            date_label.setStyleSheet("color: #6c757d; font-size: 14px;")
            item_layout.addWidget(date_label)

            title_label = QLabel(theme)
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
            item_layout.addWidget(title_label)

            time_label = QLabel(f"<b>{time}</b>")
            time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            time_label.setStyleSheet("color: #495057; font-size: 14px;")
            item_layout.addWidget(time_label)

            item_widget.setLayout(item_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint() + QSize(0, 35))

            self.events_list.addItem(list_item)
            self.events_list.setItemWidget(list_item, item_widget)

            # Create a dictionary with event details
            event_details = {
                "title": theme,
                "date": date,
                "time": time
            }

            # Connect the item clicked signal with the correct event data
            self.events_list.itemClicked.connect(lambda item, event=event_details: self.show_event_details(item, event))

    def show_event_details(self, item, event):
        """Emit event details when an item is clicked."""
        self.event_selected.emit(event)

