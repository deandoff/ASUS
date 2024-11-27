from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


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


class CalendarWidget(QWidget):
    def __init__(self, meetings):
        super().__init__()

        self.meetings = meetings

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
        self.populate_calendar()  # Очищаем таблицу

        for i in range(7):
            current_date = self.current_week_start.addDays(i).toString("dd.MM.yyyy")
            for meeting in self.meetings:
                if meeting["date"] == current_date:
                    self.add_meeting_to_table(meeting, i)

    def add_meeting_to_table(self, meeting, day_column):
        """Добавить одно совещание в таблицу."""
        # Время начала
        start_hour, start_minute = map(int, meeting["time"].split(":"))
        start_row = start_hour * 4 + (start_minute // 15)

        # Длительность в часах
        duration_str = meeting["duration"]  # Ожидается строка в формате "часы:минуты"
        duration_hours, duration_minutes = map(int, duration_str.split(":"))

        # Переводим длительность в строки таблицы
        duration_rows = (duration_hours * 60 + duration_minutes) // 15  # Округляем в 15-минутные интервалы

        # Создаем объединение ячеек для совещания
        self.table.setSpan(start_row, day_column, duration_rows, 1)
        cell = self.table.item(start_row, day_column)
        cell.setText(meeting["title"])
        cell.setBackground(QBrush(QColor("lightblue")))
        cell.setForeground(QBrush(QColor("black")))

    def update_meetings(self, meetings):
        """Обновить список совещаний и перерисовать календарь."""
        self.meetings = meetings
        self.display_meetings()

    def next_week(self):
        """Показать следующую неделю."""
        self.current_week_start = self.current_week_start.addDays(7)
        self.update_headers()
        self.display_meetings()

    def previous_week(self):
        """Показать предыдущую неделю."""
        self.current_week_start = self.current_week_start.addDays(-7)
        self.update_headers()
        self.display_meetings()
