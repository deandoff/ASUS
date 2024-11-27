from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar,
    QMenu, QMessageBox, QPushButton, QWidgetAction, QDialog, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHeaderView, QDialogButtonBox, QLineEdit,
    QDateEdit, QTimeEdit, QTextEdit, QFormLayout
)
from PySide6.QtCore import QDate, QTime

class CreateMeetingWizard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создание нового совещания")
        self.setGeometry(300, 200, 500, 400)

        self.meeting_data = {}

        self.important_fields = []

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


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно приложения")
        self.setGeometry(200, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Список совещаний
        self.meetings = []

        # Меню
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Добавление пунктов меню
        file_menu = QMenu("Файл", self)
        self.menu_bar.addMenu(file_menu)

        help_menu = QMenu("Справка", self)
        self.menu_bar.addMenu(help_menu)

        # Действия в меню
        exit_action = QWidgetAction(self)
        exit_action.setDefaultWidget(QPushButton("Выход", self))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QWidgetAction(self)
        about_action.setDefaultWidget(QPushButton("О программе", self))
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Центральный виджет
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Метка
        label = QLabel("Добро пожаловать в приложение!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Кнопки
        self.create_meeting_button = QPushButton("Создать совещание")
        self.create_meeting_button.clicked.connect(self.create_meeting)
        layout.addWidget(self.create_meeting_button)

        self.meeting_calendar_button = QPushButton("Календарь совещаний")
        self.meeting_calendar_button.clicked.connect(self.open_calendar)
        layout.addWidget(self.meeting_calendar_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Статусная строка
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Приложение запущено.")

    def show_about(self):
        """Показать информацию о приложении."""
        QMessageBox.about(self, "О программе", "Это главное окно приложения.")

    def create_meeting(self):
        """Открыть окно для создания совещания."""
        dialog = CreateMeetingWizard()
        if dialog.exec() == QDialog.Accepted:
            meeting = dialog.meeting_data
            self.meetings.append(meeting)
            QMessageBox.information(self, "Успех", "Совещание успешно создано!")

    def open_calendar(self):
        """Открыть окно с календарем совещаний."""
        calendar_window = MeetingCalendarWindow(self.meetings)
        calendar_window.exec()


if __name__ == "__main__":
    app = QApplication([])

    window = MainAppWindow()
    window.show()

    app.exec()
