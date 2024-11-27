from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtCore import QSize, Qt, QTimer, QTime, QDate
from plyer import notification


class EventListWidget(QWidget):
    event_selected = Signal(dict)  # Сигнал, передающий данные выбранного события

    def __init__(self, events, parent=None):
        super().__init__(parent)

        self.events = events
        self.upcoming_event_timer = QTimer(self)  # Таймер для уведомлений
        self.upcoming_event_timer.timeout.connect(self.check_upcoming_events)
        self.upcoming_event_timer.start(10000)  # Проверяем каждые 60 секунд

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
                background-color: #ffffff;
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

        self.btn_all_events = QPushButton("Все мероприятия")
        self.btn_all_events.clicked.connect(self.show_all_events)
        self.layout.addWidget(self.btn_all_events)

    def check_upcoming_events(self):
        """Проверяет и уведомляет о ближайших событиях."""
        today = QDate.currentDate()
        now = QTime.currentTime()
        print(self.events)
        for event in self.events:
            event_time = QTime.fromString(event["time"], "HH:mm")
            event_date = QDate.fromString(event["date"], "dd.MM.yyyy")
            print(event_date)
            time_difference = now.secsTo(event_time) // 60  # Разница в минутах
            print(time_difference)

            # Уведомляем, если событие начинается через 15 минут
            if event_date == today and 0 <= time_difference <= 15:
                self.send_notification(event)

    def send_notification(self, event):
        """Отправляет уведомление через plyer."""
        notification.notify(
            title=f"Напоминание: {event['title']}",
            message=f"Событие начнётся в {event['time']}.",
            timeout=10  # Уведомление исчезнет через 10 секунд
        )

    def populate_events(self):
        self.events_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.events_list.clear()

        window_height = self.height()
        item_height = 140
        visible_items_count = int(window_height // item_height)

        events_to_display = self.events[:visible_items_count]

        for event in events_to_display:
            item_widget = QWidget()
            item_layout = QVBoxLayout()
            item_layout.setContentsMargins(10, 10, 10, 10)

            date_label = QLabel(f"<b>{event['date']}</b>")
            date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Выравнивание по левому краю
            date_label.setStyleSheet("color: #6c757d; font-size: 14px;")
            item_layout.addWidget(date_label)

            title_label = QLabel(event["title"])
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Выравнивание по левому краю
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
            item_layout.addWidget(title_label)

            time_label = QLabel(f"<b>{event['time']}</b>")
            time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Выравнивание по левому краю
            time_label.setStyleSheet("color: #495057; font-size: 14px;")
            item_layout.addWidget(time_label)

            item_widget.setLayout(item_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint() + QSize(0, 35))

            self.events_list.addItem(list_item)
            self.events_list.setItemWidget(list_item, item_widget)

    def show_event_details(self, item):
        """Вызывается при выборе элемента списка и передает его данные в сигнал."""
        row = self.events_list.row(item)
        if row >= 0 and row < len(self.events):
            event = self.events[row]
            self.event_selected.emit(event)
