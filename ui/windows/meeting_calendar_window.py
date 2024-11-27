# meeting_calendar_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialogButtonBox, QHeaderView
from PySide6.QtCore import Qt

class MeetingCalendarWindow(QDialog):
    def __init__(self, meetings):
        super().__init__()

        self.setWindowTitle("Календарь совещаний")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout(self)

        # Таблица для отображения совещаний
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Тема", "Дата", "Время", "Участники", "Место"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Заполнение таблицы данными
        self.load_meetings(meetings)

        # Кнопки закрытия
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def load_meetings(self, meetings):
        """Заполнить таблицу данными о совещаниях."""
        self.table.setRowCount(len(meetings))
        for row, meeting in enumerate(meetings):
            self.table.setItem(row, 0, QTableWidgetItem(meeting["Тема"]))
            self.table.setItem(row, 1, QTableWidgetItem(meeting["Дата"]))
            self.table.setItem(row, 2, QTableWidgetItem(meeting["Время"]))
            self.table.setItem(row, 3, QTableWidgetItem(meeting["Участники"]))
            self.table.setItem(row, 4, QTableWidgetItem(meeting["Место"]))
