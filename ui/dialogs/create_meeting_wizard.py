from PySide6.QtCore import QDate, QTime
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QWidget, QLineEdit, QDateEdit,
    QTimeEdit, QCheckBox, QComboBox, QListWidget, QTextEdit, QLabel, QMessageBox,
)

from ui.support.searchable_multi_select import SearchableMultiSelect
from ui.dialogs.add_question_dialog import AddQuestionDialog


class CreateMeetingWizard(QDialog):
    def __init__(self, user_data):
        super().__init__()

        self.setWindowTitle('Новое совещание')
        self.setGeometry(300, 200, 700, 600)
        self.setFixedSize(700, 600)

        self.current_page = 0
        self.meeting_data = {}

        self.page_was_created = False
        self.additional_page_index = None

        self.stacked_widget = QStackedWidget()
        self.create_main_page()
        self.create_topic_page()
        self.create_summary_page()

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.previous_page)
        self.back_button.setStyleSheet("""font-family: Roboto Slab; 
                        font-size: 17px; 
                        color: white; 
                        background-color: black; 
                        border: 2px solid black; 
                        border-radius: 10px; 
                        padding: 5px;""")
        self.back_button.setEnabled(False)

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setStyleSheet("""font-family: Roboto Slab; 
                                font-size: 17px; 
                                color: white; 
                                background-color: black; 
                                border: 2px solid black; 
                                border-radius: 10px; 
                                padding: 5px;""")

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

        self.setStyleSheet("""font-family: Roboto Slab; 
                                      font-size: 14px;
                                      background-color: #F0FFFF;""")
        self.stacked_widget.setStyleSheet("""QLineEdit {background-color: #E0FFFF;
                        border-style: solid; /* Устанавливает стиль границы */
                        border-width: 2px; /* Толщина границы */
                        border-color: #808080; /* Цвет границы */
                        padding: 8px;
                        margin: 5px;
                        border-radius: 4px;}
                        
                        QDateEdit {background-color: #E0FFFF;
                        border-style: solid; /* Устанавливает стиль границы */
                        border-width: 2px; /* Толщина границы */
                        border-color: #808080; /* Цвет границы */
                        padding: 8px;
                        margin: 5px;
                        border-radius: 4px;}
                        
                        QTimeEdit {background-color: #E0FFFF;
                        border-style: solid; /* Устанавливает стиль границы */
                        border-width: 2px; /* Толщина границы */
                        border-color: #808080; /* Цвет границы */
                        padding: 8px;
                        margin: 5px;
                        border-radius: 4px;} """)

    def on_time_changed(self, time):
        """Автоматическая корректировка времени на ближайшее кратное 15 минутам (в меньшую сторону)."""
        if time.minute() % 15 != 0:
            # Округляем вниз к ближайшему кратному 15 минутам
            minutes = (time.minute() // 15) * 15  # Округляем в меньшую сторону
            corrected_time = QTime(time.hour(), minutes)
            self.time_input.setTime(corrected_time)  # Устанавливаем откорректированное время

    def create_main_page(self):
        self.main_page = QWidget()
        layout = QFormLayout(self.main_page)

        self.topic_input = QLineEdit()
        layout.addRow("Тема совещания:", self.topic_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDate(QDate.currentDate())
        layout.addRow("Дата:", self.date_input)

        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.time_input.timeChanged.connect(self.on_time_changed)

        layout.addRow("Время:", self.time_input)

        # Выпадающий список для выбора длительности
        self.duration_input = QTimeEdit()
        self.duration_input.timeChanged.connect(self.on_duration_changed)
        layout.addRow("Длительность (ч):", self.duration_input)

        self.participants_input = SearchableMultiSelect(
            items=["Иванов И.И.", "Петров П.П.", "Сидоров С.С.", "Александров А.А.", "Викторов В.В."]
        )
        layout.addRow("Участники:", self.participants_input)

        self.additional_participants_checkbox = QCheckBox("Дополнительные участники")
        self.additional_participants_checkbox.stateChanged.connect(self.on_additional_participants_toggled)
        layout.addRow(self.additional_participants_checkbox)

        self.stacked_widget.addWidget(self.main_page)

    def on_duration_changed(self, time):
        """Автоматическая корректировка длительности на ближайшее кратное 15 минутам."""
        # Получаем текущие минуты
        minutes = time.minute()

        # Вычисляем кратное 15 минутам
        corrected_minutes = (minutes // 15) * 15  # Округляем в меньшую сторону

        # Если минуты не равны текущим, обновляем время
        if corrected_minutes != minutes:
            corrected_time = QTime(time.hour(), corrected_minutes)
            self.duration_input.setTime(corrected_time)  # Устанавливаем исправленное время

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.stacked_widget.setCurrentIndex(self.current_page)

            if self.current_page < self.stacked_widget.count() - 1:
                self.next_button.setText("Далее")
                self.next_button.clicked.disconnect()
                self.next_button.clicked.connect(self.next_page)

            if self.current_page == 0:
                self.back_button.setEnabled(False)

    def on_additional_participants_toggled(self, state):
        if state:
            if not self.page_was_created:
                self.create_additional_participants_page()
        else:
            if self.page_was_created and self.additional_page_index is not None:
                self.stacked_widget.removeWidget(self.additional_page)
                self.additional_page.deleteLater()
                self.additional_page_index = None
                self.page_was_created = False

    def create_additional_participants_page(self):
        if self.page_was_created and self.additional_page_index is None:
            self.stacked_widget.removeWidget(self.summary_page)

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

        self.external_participants_input = QListWidget()
        self.external_participants_input.setSelectionMode(QListWidget.MultiSelection)
        self.external_participants_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])
        layout.addRow("Внешние участники:", self.external_participants_input)

        self.stacked_widget.addWidget(self.additional_page)
        self.additional_page_index = self.stacked_widget.indexOf(self.additional_page)
        self.page_was_created = True

        self.stacked_widget.addWidget(self.summary_page)

    def create_topic_page(self):
        """Создание страницы с вопросами совещания."""
        self.topics_page = QWidget()
        layout = QVBoxLayout(self.topics_page)

        self.topics_input = QTextEdit()
        layout.addWidget(QLabel("Вопросы совещания:"))
        layout.addWidget(self.topics_input)

        # Кнопка для добавления вопроса
        self.add_question_button = QPushButton("Добавить вопрос")
        self.add_question_button.clicked.connect(self.add_question)
        self.add_question_button.setStyleSheet("""font-family: Roboto Slab; 
                                        font-size: 17px; 
                                        color: white; 
                                        background-color: black; 
                                        border: 2px solid black; 
                                        border-radius: 10px; 
                                        padding: 5px;""")
        layout.addWidget(self.add_question_button)

        self.stacked_widget.addWidget(self.topics_page)

    def create_summary_page(self):
        self.summary_page = QWidget()
        layout = QVBoxLayout(self.summary_page)

        layout.addWidget(QLabel("Подтверждение информации о совещании:"))
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)

        self.stacked_widget.addWidget(self.summary_page)

    def next_page(self):

        if not self.topic_input.text():
            error_window = QMessageBox()
            error_window.setWindowTitle("Ошибка")
            error_window.setText("Введите тему совещания")
            error_window.setStandardButtons(QMessageBox.Ok)
            error_window.setStyleSheet("""QMessageBox {
                font-family: Roboto Slab; 
                font-size: 18px;
                background-color: #F0FFFF;
                } 
                
                QPushButton {font-family: Roboto Slab; 
                                        font-size: 17px; 
                                        color: white; 
                                        background-color: black; 
                                        border: 2px solid black; 
                                        border-radius: 10px; 
                                        padding: 5px;}""")
            error_window.exec_()
            return

        if self.time_input.time() < QTime.currentTime() and self.date_input.date() == QDate.currentDate():
            error_window = QMessageBox()
            error_window.setWindowTitle("Ошибка")
            error_window.setText("Ввыберите корректное время")
            error_window.setStandardButtons(QMessageBox.Ok)
            error_window.setStyleSheet("""QMessageBox {
                            font-family: Roboto Slab; 
                            font-size: 18px;
                            background-color: #F0FFFF;
                            } 

                            QPushButton {font-family: Roboto Slab; 
                                                    font-size: 17px; 
                                                    color: white; 
                                                    background-color: black; 
                                                    border: 2px solid black; 
                                                    border-radius: 10px; 
                                                    padding: 5px;}""")
            error_window.exec_()
            return


        if self.current_page < self.stacked_widget.count() - 1:
            self.current_page += 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.back_button.setEnabled(True)

            if self.current_page == self.stacked_widget.count() - 1:
                self.next_button.setText("Готово")
                self.next_button.clicked.disconnect()
                self.next_button.clicked.connect(self.accept)
                self.populate_summary_page()
            else:
                self.next_button.setText("Далее")

    def accept(self):
        duration = self.duration_input.time().toString("HH:mm")
        self.meeting_data = {
            "title": self.topic_input.text(),
            "date": self.date_input.date().toString("dd.MM.yyyy"),
            "time": self.time_input.time().toString("HH:mm"),
            "duration": duration,  # Сохраняем длительность в формате числа
            "description": self.topics_input.toPlainText(),
            "participants": self.participants_input.get_selected_items(),
        }
        super().accept()

    def populate_summary_page(self):
        """Заполнить страницу информации данными о совещании."""
        participants = ", ".join(self.participants_input.get_selected_items())  # Множественный выбор участников

        # Создаем строку с основной информацией о совещании
        summary = f"""
            Тема: {self.topic_input.text()}
            Дата: {self.date_input.date().toString("dd.MM.yyyy")}
            Время: {self.time_input.time().toString("HH:mm")}
            Длительность: {self.duration_input.time().toString("HH:mm")} ч.
            Участники: {participants}
            Повестка совещания:
            {self.topics_input.toPlainText()}
            Дополнительные участники: {"Да" if self.additional_participants_checkbox.isChecked() else "Нет"}
        """

        # Если выбраны дополнительные участники, добавим их информацию
        if self.additional_participants_checkbox.isChecked() and self.external_participants_input:
            external_participants = ", ".join(
                [item.text() for item in self.external_participants_input.selectedItems()])
            summary += f"""
                Председатель: {self.chairperson_input.currentText()}
                Секретарь: {self.secretary_input.currentText()}
                Контролёр: {self.controller_input.currentText()}
                Внешние участники: {external_participants}
            """

        # Устанавливаем итоговый текст в виджет
        self.summary_text.setText(summary)

    def add_question(self):
        dialog = AddQuestionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            question = dialog.get_question_data()
            self.topics_input.append(
                f"\tВопрос: {question['text']}\n\tОтветчик: {question['responder']}\n\tПрикреплённые файлы: {question['files']}\n"
            )
