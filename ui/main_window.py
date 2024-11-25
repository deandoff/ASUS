from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLineEdit, QDateEdit,
    QTimeEdit, QFormLayout, QDialogButtonBox, QStackedWidget,
    QCheckBox, QPushButton, QLabel, QComboBox, QTextEdit, QHBoxLayout, QFileDialog, QWidget, QMainWindow, QTableWidget,
    QHeaderView, QTableWidgetItem, QGridLayout, QMenuBar, QMenu, QWidgetAction, QMessageBox
)


class CreateMeetingWizard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создание нового совещания")
        self.setGeometry(300, 200, 600, 500)

        self.current_page = 0
        self.meeting_data = {}

        # Основной виджет с несколькими страницами
        self.stacked_widget = QStackedWidget()
        self.create_main_page()
        self.create_additional_participants_page()
        self.create_topics_page()
        self.create_summary_page()  # Создаём последнюю страницу сразу

        # Кнопки навигации
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.previous_page)
        self.back_button.setEnabled(False)

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_page)

        # Общий макет
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

    def create_main_page(self):
        """Создание основной страницы ввода данных."""
        self.main_page = QWidget()
        layout = QFormLayout(self.main_page)

        self.topic_input = QLineEdit()
        layout.addRow("Тема совещания:", self.topic_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())  # Установить текущую дату
        layout.addRow("Дата:", self.date_input)

        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())  # Установить текущее время
        layout.addRow("Время:", self.time_input)

        self.duration_input = QLineEdit()
        layout.addRow("Длительность (ч):", self.duration_input)

        self.participants_input = QComboBox()
        self.participants_input.setEditable(True)  # Для поиска
        self.participants_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])  # Пример данных
        layout.addRow("Участники:", self.participants_input)

        self.additional_participants_checkbox = QCheckBox("Дополнительные участники")
        layout.addRow(self.additional_participants_checkbox)

        self.stacked_widget.addWidget(self.main_page)

    def create_additional_participants_page(self):
        """Создание страницы с дополнительными участниками."""
        self.additional_page = QWidget()
        layout = QFormLayout(self.additional_page)

        self.chairperson_input = QComboBox()
        self.chairperson_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])
        layout.addRow("Председатель:", self.chairperson_input)

        self.secretary_input = QComboBox()
        self.secretary_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])
        layout.addRow("Секретарь:", self.secretary_input)

        self.controller_input = QComboBox()
        self.controller_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])
        layout.addRow("Контролёр:", self.controller_input)

        self.external_participants_input = QTextEdit()
        layout.addRow("Внешние участники:", self.external_participants_input)

        self.stacked_widget.addWidget(self.additional_page)

    def create_topics_page(self):
        """Создание страницы с вопросами совещания."""
        self.topics_page = QWidget()
        layout = QVBoxLayout(self.topics_page)

        self.topics_input = QTextEdit()
        layout.addWidget(QLabel("Вопросы совещания:"))
        layout.addWidget(self.topics_input)

        self.stacked_widget.addWidget(self.topics_page)

    def create_summary_page(self):
        """Создание страницы с информацией о совещании."""
        self.summary_page = QWidget()
        layout = QVBoxLayout(self.summary_page)

        # Заголовок
        layout.addWidget(QLabel("Подтверждение информации о совещании:"))

        # Виджет для отображения информации
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)

        self.stacked_widget.addWidget(self.summary_page)

    def next_page(self):
        """Перейти на следующую страницу."""
        if self.current_page < self.stacked_widget.count() - 1:
            self.current_page += 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.back_button.setEnabled(True)

            if self.current_page == self.stacked_widget.count() - 1:
                self.next_button.setText("Готово")
                self.next_button.clicked.disconnect()  # Отключить старый слот
                self.next_button.clicked.connect(self.accept)
                self.populate_summary_page()  # Заполнить страницу информации
            else:
                self.next_button.setText("Далее")

    def populate_summary_page(self):
        """Заполнить страницу информации данными о совещании."""
        summary = f"""
        Тема: {self.topic_input.text()}
        Дата: {self.date_input.date().toString("dd.MM.yyyy")}
        Время: {self.time_input.time().toString("HH:mm")}
        Длительность: {self.duration_input.text()} ч.
        Участники: {self.participants_input.currentText()}
        Дополнительные участники: {"Да" if self.additional_participants_checkbox.isChecked() else "Нет"}
        """
        if self.additional_participants_checkbox.isChecked():
            summary += f"""
            Председатель: {self.chairperson_input.currentText()}
            Секретарь: {self.secretary_input.currentText()}
            Контролёр: {self.controller_input.currentText()}
            Внешние участники: {self.external_participants_input.toPlainText()}
            """

        summary += f"""
        Вопросы совещания: {self.topics_input.toPlainText()}
        """

        self.summary_text.setText(summary)

    def previous_page(self):
        """Перейти на предыдущую страницу."""
        if self.current_page > 0:
            self.current_page -= 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.back_button.setEnabled(self.current_page > 0)

            if self.current_page < self.stacked_widget.count() - 1:
                self.next_button.setText("Далее")
                self.next_button.clicked.disconnect()
                self.next_button.clicked.connect(self.next_page)

    def accept(self):
        """Сохранение данных совещания и завершение мастера."""
        self.meeting_data = {
            "title": self.topic_input.text(),
            "date": self.date_input.date(),
            "time": self.time_input.time().hour(),
            "duration": int(self.duration_input.text()) if self.duration_input.text().isdigit() else 1,
            "description": self.topics_input.toPlainText(),
            "participants": self.participants_input.currentText(),
            "additional": {
                "chairperson": self.chairperson_input.currentText(),
                "secretary": self.secretary_input.currentText(),
                "controller": self.controller_input.currentText(),
                "external_participants": self.external_participants_input.toPlainText(),
            } if self.additional_participants_checkbox.isChecked() else None
        }
        super().accept()


class CalendarWindow(QMainWindow):
    def __init__(self, meetings):
        super().__init__()
        self.setWindowTitle("Календарь совещаний")
        self.setGeometry(100, 100, 900, 600)

        # Устанавливаем текущую неделю
        self.current_week_start = QDate.currentDate().addDays(-(QDate.currentDate().dayOfWeek() - 1))

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        self.layout = QVBoxLayout(self.central_widget)

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
        self.table.setRowCount(24)  # 24 часа
        self.table.setColumnCount(7)  # 7 дней (неделя)
        self.update_headers()

        self.table.setVerticalHeaderLabels([f"{hour:02}:00" for hour in range(24)])

        # Растяжение заголовков
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Заполнение таблицы
        self.populate_calendar()

        # Событие клика
        self.table.cellClicked.connect(self.show_meeting_info)

        # Добавляем таблицу в макет
        self.layout.addWidget(self.table)

        # Список совещаний
        self.meetings = {}
        for meeting in meetings:
            self.add_meeting(meeting)

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
        for row in range(24):
            for col in range(7):
                self.table.setItem(row, col, QTableWidgetItem(""))

    def display_meetings(self):
        """Добавить данные о совещаниях в календарь."""
        self.populate_calendar()  # Очищаем таблицу

        for i in range(7):
            current_date = self.current_week_start.addDays(i)
            if current_date in self.meetings:
                for meeting in self.meetings[current_date]:
                    hour = meeting["time"]
                    cell = self.table.item(hour, i)
                    cell.setText(meeting["title"])
                    cell.setBackground(Qt.lightGray)
                    print(
                        f"Отображаем совещание {meeting} на {current_date.toString('dd.MM.yyyy')} в {hour}:00")  # Отладка

    def show_meeting_info(self, row, col):
        """Отобразить информацию о совещании при клике."""
        current_date = self.current_week_start.addDays(col)  # Получаем дату по текущему столбцу
        if current_date in self.meetings:
            for meeting in self.meetings[current_date]:
                if meeting["time"] == row:  # Если время совпадает
                    dialog = MeetingInfoDialog(meeting)
                    dialog.exec()

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

    def add_meeting(self, meeting):
        """Добавить новое совещание в календарь."""
        meeting_date = meeting["date"]
        print(f"Добавляем совещание в календарь: {meeting}")  # Отладочное сообщение

        if meeting_date not in self.meetings:
            self.meetings[meeting_date] = []

        self.meetings[meeting_date].append({
            "time": meeting["time"],
            "title": meeting["title"],
            "duration": meeting["duration"],
            "description": meeting["description"]
        })

        print(f"Текущее состояние списка совещаний: {self.meetings}")  # Отладка
        self.display_meetings()

    def update_meetings(self, meetings):
        """Обновить список совещаний и перерисовать календарь."""
        self.meetings = {}
        for meeting in meetings:
            self.add_meeting(meeting)  # Перезаполняем данные
        self.display_meetings()

class MeetingInfoDialog(QDialog):
    def __init__(self, meeting):
        super().__init__()
        self.setWindowTitle(meeting["title"])
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Время: {meeting['time']}:00"))
        layout.addWidget(QLabel(f"Длительность: {meeting['duration']} ч"))
        layout.addWidget(QLabel(f"Описание: {meeting['description']}"))
        self.setLayout(layout)


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
            print(f"Новое совещание создано: {meeting}")  # Отладочное сообщение
            self.meetings.append(meeting)  # Сохраняем совещание
            QMessageBox.information(self, "Успех", "Совещание успешно создано!")

            # Обновляем календарь, если он открыт
            if hasattr(self, "calendar_window") and self.calendar_window.isVisible():
                print("Обновляем календарь...")  # Отладочное сообщение
                self.calendar_window.add_meeting(meeting)

    def open_calendar(self):
        """Открыть окно с календарем совещаний."""
        if not hasattr(self, "calendar_window"):
            print("Создаём окно календаря...")  # Отладочное сообщение
            self.calendar_window = CalendarWindow(self.meetings)  # Передаём ссылку на список
        else:
            print("Обновляем данные календаря...")  # Отладочное сообщение
            self.calendar_window.update_meetings(self.meetings)  # Обновляем данные
        self.calendar_window.show()


if __name__ == "__main__":
    app = QApplication([])

    window = MainAppWindow()
    window.show()

    app.exec()
