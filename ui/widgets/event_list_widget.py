from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtCore import QTimer, QTime, QDate
from plyer import notification
import psycopg2

db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"

class EventListWidget(QWidget):
    event_selected = Signal(dict)  # Сигнал, передающий данные выбранного события

    def __init__(self, events, user_data, parent=None):
        super().__init__(parent)

        self.user_data = user_data
        self.events = events  # Сохраняем события
        self.upcoming_event_timer = QTimer(self)  # Таймер для уведомлений
        self.upcoming_event_timer.timeout.connect(self.check_upcoming_events)
        self.upcoming_event_timer.start(60000)  # Проверяем каждые 60 секунд

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Ближайшие совещания")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont('Roboto Slab', 14))
        self.layout.addWidget(self.title_label)

        self.button = QPushButton("обновить")
        self.button.clicked.connect(self.populate_events)
        self.layout.addWidget(self.button)
        self.button.setStyleSheet("""font-family: Roboto Slab; 
                                                                 font-size: 17px; 
                                                                 color: white; 
                                                                 background-color: black; 
                                                                 border: 2px solid black; 
                                                                 border-radius: 10px; 
                                                                 padding: 5px; 
                            """)

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
        user_id = self.user_data["id"]
        user_role = self.user_data["role"]

        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()

            if user_role == "ADMIN":
                # Администратор видит все совещания
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
                    ORDER BY c.date ASC, c.time ASC;
                """)
            else:
                # Участники видят только свои совещания
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
                    LEFT JOIN 
                        Participant p ON m.id = p.meeting_id AND p.id_from_users = %s AND p.status = 'accepted'
                    WHERE 
                        p.id_from_users IS NOT NULL
                    ORDER BY c.date ASC, c.time ASC;
                """, (user_id,))

            events = cursor.fetchall()

            for event in events:
                meeting_id, theme, date, time = event  # Извлекаем данные о совещании
                event_time = QTime.fromString(time.strftime("%H:%M:%S"), "HH:mm:ss")
                event_date = QDate.fromString(date.strftime("%Y-%m-%d"), "yyyy-MM-dd")  # Преобразуем дату в строку
                time_difference = now.secsTo(event_time) // 60  # Разница в минутах

                # Уведомляем, если событие начинается через 15 минут
                if event_date == today and 14 <= time_difference <= 15:
                    event_data = {
                        "id": meeting_id,
                        "title": theme,
                        "date": date,
                        "time": time
                    }
                    self.send_notification(event_data)

        except Exception as e:
            print(e)

    def populate_events(self):
        """Заполняет список событий для отображения."""
        self.events_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.events_list.clear()
        self.events = []  # Обнуляем список событий
        user_id = self.user_data["id"]
        user_role = self.user_data["role"]

        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()

            if user_role == "ADMIN":
                # Администратор видит все совещания
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
                    ORDER BY c.date ASC, c.time ASC;
                """)
            else:
                # Участники видят только свои совещания
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
                    LEFT JOIN 
                        Participant p ON m.id = p.meeting_id AND p.id_from_users = %s AND p.status = 'accepted'
                    WHERE 
                        p.id_from_users IS NOT NULL
                    ORDER BY c.date ASC, c.time ASC;
                """, (user_id,))

            events = cursor.fetchall()
            for event in events:
                meeting_id, theme, date, time = event
                self.events.append({
                    "id": meeting_id,
                    "theme": theme,
                    "date": date,
                    "time": time
                })

        except Exception as e:
            print(e)
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        for event in events:
            meeting_id, theme, date, time = event  # Извлекаем данные о совещании
            self.events.append({"id": meeting_id, "title": theme, "date": date, "time": time})  # Сохраняем событие

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

    def check_upcoming_events(self):
        """Проверяет и уведомляет о ближайших событиях."""
        today = QDate.currentDate()
        now = QTime.currentTime()
        user_id = self.user_data["id"]
        user_role = self.user_data["role"]

        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()

            if user_role == "ADMIN":
                # Администратор видит все совещания
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
                    ORDER BY c.date ASC, c.time ASC;
                """)
            else:
                # Участники, организаторы, гости и секретари видят только свои совещания
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
                    LEFT JOIN 
                        Participant p ON m.id = p.meeting_id AND p.id_from_users = %s and p.status = 'accepted'
                    LEFT JOIN 
                        Guest g ON m.id = g.meeting_id AND g.id_from_users = %s
                    WHERE 
                        p.id_from_users IS NOT NULL OR 
                        cr.id_from_users IS NOT NULL OR 
                        g.id_from_users IS NOT NULL
                    ORDER BY c.date ASC, c.time ASC;
                """, (user_id, user_id, user_id))

            events = cursor.fetchall()

            for event in events:
                meeting_id, theme, date, time = event  # Извлекаем данные о совещании
                event_time = QTime.fromString(time.strftime("%H:%M:%S"), "HH:mm:ss")
                event_date = QDate.fromString(date.strftime("%d.%m.%Y"), "dd.MM.yyyy")  # Преобразуем дату в строку
                time_difference = now.secsTo(event_time) // 60  # Разница в минутах

                # Уведомляем, если событие начинается через 15 минут
                if event_date == today and 14 <= time_difference <= 15:
                    event_data = {
                        "id": meeting_id,
                        "title": theme,
                        "date": date,
                        "time": time
                    }
                    self.send_notification(event_data)

        except Exception as e:
            print(e)

    def send_notification(self, event):
        """Отправляет уведомление через plyer."""
        notification.notify(
            title=f"Напоминание: {event['title']}",
            message=f"Событие начнётся в {event['time']}.",
            timeout=10  # Уведомление исчезнет через 10 секунд
        )

    def show_event_details(self, item):
        """Вызывается при выборе элемента списка и передает его данные в сигнал."""
        row = self.events_list.row(item)
        if 0 <= row < len(self.events):
            meeting_id = self.events[row]["id"]
            event = self.fetch_event_details(meeting_id)
            if event:
                self.event_selected.emit(event)

    def fetch_event_details(self, meeting_id):
        """Получает полные данные о совещании из базы данных по ID."""
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    m.theme, 
                    c.date, 
                    c.time 
                FROM 
                    Meetings m
                JOIN 
                    Calendar c ON m.id = c.meeting_id
                WHERE 
                    m.id = %s;
            """, (meeting_id,))
            event = cursor.fetchone()
            if event:
                return {
                    "id": meeting_id,
                    "title": event[0],
                    "date": event[1],
                    "time": event[2]
                }
        except Exception as e:
            print(e)
        return None