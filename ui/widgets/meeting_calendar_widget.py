from PySide6.QtCore import Qt
from PySide6.QtCore import QDate
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
import psycopg2

db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"

class CalendarWidget(QWidget):
    def __init__(self, user_data):
        super().__init__()

        self.user_data = user_data
        self.user_id = user_data["id"]
        self.role = user_data["role"]  # Получаем роль пользователя
        self.meetings = []

        # Устанавливаем текущую неделю
        self.current_week_start = QDate.currentDate().addDays(-(QDate.currentDate().dayOfWeek() - 1))

        # Основной макет
        self.layout = QVBoxLayout(self)

        # Кнопки управления неделями
        nav_layout = QHBoxLayout()
        self.prev_week_button = QPushButton("Предыдущая неделя")
        self.prev_week_button.clicked.connect(self.previous_week)
        nav_layout.addWidget(self.prev_week_button)

        self.next_week_button = QPushButton("Следующая неделя")
        self.next_week_button.clicked.connect(self.next_week)
        nav_layout.addWidget(self.next_week_button)

        self.layout.addLayout(nav_layout)

        # Таблица календаря
        self.table = QTableWidget()
        self.table.setRowCount(96)  # 24 часа * 4 (15-минутные слоты)
        self.table.setColumnCount(7)  # 7 дней (неделя)
        self.update_headers()

        self.table.setVerticalHeaderLabels(
            [f"{hour:02}:00" if minute == 0 else "" for hour in range(24) for minute in (0, 15, 30, 45)]
        )

        # Растяжение заголовков
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Заполнение таблицы
        self.populate_calendar()

        # Добавляем таблицу в макет
        self.layout.addWidget(self.table)

        # Отображение совещаний в таблице
        self.display_meetings()

        self.setStyleSheet("""
            /* Общий стиль для фона виджета */
            QWidget {
                background-color: #F0FFFF;
                font-family: "Roboto Slab";
                font-size: 14px;
            }

            /* Кнопки навигации */
            QPushButton {
                font-family: Roboto Slab; 
                font-size: 17px; 
                color: white; 
                background-color: black; 
                border: 2px solid black; 
                border-radius: 10px; 
                padding: 5px;
            }
        """)

    def update_headers(self):
        """Обновить заголовки таблицы с датами."""
        headers = []
        for i in range(7):
            date = self.current_week_start.addDays(i)
            headers.append(f"{date.toString('ddd')}\n{date.toString('dd.MM')}")
        self.table.setHorizontalHeaderLabels(headers)

    def populate_calendar(self):
        """Инициализация пустых ячеек."""
        for row in range(96):  # Каждая строка — это 15 минут
            for col in range(7):
                item = QTableWidgetItem("")
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Запрещаем редактирование
                self.table.setItem(row, col, item)

    def display_meetings(self):
        """Добавить данные о совещаниях в календарь."""
        self.meetings = self.fetch_meetings()  # Загружаем совещания из базы данных
        self.populate_calendar()  # Очищаем таблицу

        for i in range(7):
            current_date = self.current_week_start.addDays(i).toString("dd.MM.yyyy")
            for meeting in self.meetings:
                if meeting["date"] == current_date:
                    self.add_meeting_to_table(meeting, i)

    def fetch_meetings(self):
        """Получить совещания из базы данных, в которых пользователь является участником или администратор."""
        meetings = []
        try:
            connection = psycopg2.connect(db_url)
            cursor = connection.cursor()
            if self.role == 'ADMIN':
                query = """
                    SELECT c.date, c.time, m.theme, c.duration
                    FROM Calendar c
                    JOIN Meetings m ON c.meeting_id = m.id
                """
                cursor.execute(query)
            else:
                query = """
                    SELECT c.date, c.time, m.theme, c.duration
                    FROM Calendar c
                    JOIN Meetings m ON c.meeting_id = m.id
                    JOIN Participant p ON m.id = p.meeting_id
                    WHERE p.id_from_users = %s
                """
                cursor.execute(query, (self.user_id,))
            rows = cursor.fetchall()
            for row in rows:
                meeting = {
                    "date": row[0].strftime("%d.%m.%Y"),
                    "time": row[1],
                    "title": row[2],
                    "duration": row[3]
                }
                meetings.append(meeting)
        except Exception as e:
            print(f"Ошибка при получении совещаний: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()
        return meetings

    def add_meeting_to_table(self, meeting, day_column):
        """Добавить совещание в таблицу по дню."""
        time = meeting["time"]
        start_hour = time.hour
        start_minute = time.minute
        start_row = start_hour * 4 + (start_minute // 15)

        duration = meeting["duration"]
        duration_hours = duration.hour
        duration_minutes = duration.minute

        duration_rows = (duration_hours * 60 + duration_minutes) // 15

        self.table.setSpan(start_row, day_column, duration_rows, 1)
        cell = self.table.item(start_row, day_column)
        cell.setText(meeting["title"])
        cell.setBackground(QColor("lightblue"))
        cell.setForeground(QBrush(QColor("black")))

    def previous_week(self):
        """Перейти к предыдущей неделе."""
        self.current_week_start = self.current_week_start.addDays(-7)
        self.update_headers()
        self.display_meetings()

    def next_week(self):
        """Перейти к следующей неделе."""
        self.current_week_start = self.current_week_start.addDays(7)
        self.update_headers()
        self.display_meetings()