# create_meeting_wizard.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDateEdit, QTimeEdit, QTextEdit, QDialogButtonBox, QMessageBox
from PySide6.QtCore import QDate, QTime

class CreateMeetingWizard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создание нового совещания")
        self.setGeometry(300, 200, 500, 400)

        self.meeting_data = {}

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # Поля для ввода данных
        self.topic_input = QLineEdit()
        form_layout.addRow("Тема совещания:", self.topic_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)

        # Установка текущей даты по умолчанию
        current_date = QDate.currentDate()
        self.date_input.setDate(current_date)

        # Запрет выбора прошлых дат
        self.date_input.setMinimumDate(current_date)

        form_layout.addRow("Дата:", self.date_input)

        self.time_input = QTimeEdit()

        # Установка текущего времени по умолчанию
        current_time = QTime.currentTime()
        self.time_input.setTime(current_time)

        form_layout.addRow("Время:", self.time_input)

        self.duration_input = QLineEdit()
        form_layout.addRow("Длительность (ч):", self.duration_input)

        self.participants_input = QTextEdit()
        form_layout.addRow("Участники:", self.participants_input)

        self.location_input = QLineEdit()
        form_layout.addRow("Место проведения:", self.location_input)

        layout.addLayout(form_layout)

        # Кнопки OK и Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        """Собрать данные и завершить диалог."""
        meeting_date = self.date_input.date()
        meeting_time = self.time_input.time()
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()

        # Если выбранная дата - сегодняшняя
        if meeting_date == current_date:
            # Проверка времени, чтобы оно не было раньше текущего времени
            if meeting_time < current_time:
                QMessageBox.warning(self, "Ошибка", "Вы не можете выбрать время раньше текущего времени.")
                return

        if self.topic_input.text() == "":
            QMessageBox.warning(self, "Ошибка", "Укажите тему совещания.")
            return

        # Сбор данных
        self.meeting_data = {
            "Тема": self.topic_input.text(),
            "Дата": meeting_date.toString("dd.MM.yyyy"),
            "Время": meeting_time.toString("HH:mm"),
            "Длительность": self.duration_input.text(),
            "Участники": self.participants_input.toPlainText(),
            "Место": self.location_input.text(),
        }
        super().accept()
