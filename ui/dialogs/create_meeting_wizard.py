from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QDialog, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QWidget, \
    QLineEdit, QDateEdit, QTimeEdit, QListWidget, QCheckBox, QComboBox, QTextEdit, QLabel, QFileDialog

from ui.support.searchable_multi_select import SearchableMultiSelect
from ui.dialogs.add_question_dialog import AddQuestionDialog

class CreateMeetingWizard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Новое совещание')
        self.setGeometry(300, 200, 600, 500)
        self.setFixedSize(600, 500)

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
        self.back_button.setEnabled(False)

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_page)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

    def create_main_page(self):
        self.main_page = QWidget()
        layout = QFormLayout(self.main_page)

        self.topic_input = QLineEdit()
        layout.addRow("Тема совещания:", self.topic_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addRow("Дата:", self.date_input)

        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        layout.addRow("Время:", self.time_input)

        self.duration_input = QLineEdit()
        layout.addRow("Длительность (ч):", self.duration_input)

        self.participants_input = QListWidget()
        self.participants_input = SearchableMultiSelect(
            items=["Иванов И.И.", "Петров П.П.", "Сидоров С.С.", "Александров А.А.", "Викторов В.В."]
        )
        layout.addRow("Участники:", self.participants_input)

        self.additional_participants_checkbox = QCheckBox("Дополнительные участники")
        self.additional_participants_checkbox.stateChanged.connect(self.on_additional_participants_toggled)
        layout.addRow(self.additional_participants_checkbox)

        self.stacked_widget.addWidget(self.main_page)

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
        self.chairperson_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров S.S."])
        layout.addRow("Председатель:", self.chairperson_input)

        self.secretary_input = QComboBox()
        self.secretary_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров S.S."])
        layout.addRow("Секретарь:", self.secretary_input)

        self.controller_input = QComboBox()
        self.controller_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров S.S."])
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

    def next_page(self):
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
        self.meeting_data = {
            "title": self.topic_input.text(),
            "date": self.date_input.date().toString("dd.MM.yyyy"),
            "time": self.time_input.time().toString("HH:mm"),
            "duration": int(self.duration_input.text()) if self.duration_input.text().isdigit() else 1,
            "description": self.topics_input.toPlainText(),
            "participants": self.participants_input.get_selected_items(),  # Используем метод get_selected_items
            "additional": {
                "chairperson": self.chairperson_input.currentText() if self.page_was_created else None,
                "secretary": self.secretary_input.currentText() if self.page_was_created else None,
                "controller": self.controller_input.currentText() if self.page_was_created else None,
                "external_participants": [
                    item.text() for item in self.external_participants_input.selectedItems()
                ] if self.page_was_created else None
            } if self.additional_participants_checkbox.isChecked() else None
        }
        super().accept()

    def populate_summary_page(self):
        participants = ", ".join(
            [item for item in self.participants_input.get_selected_items()])

        summary = f"""
                        Тема: {self.topic_input.text()}
                        Дата: {self.date_input.date().toString("dd.MM.yyyy")}
                        Время: {self.time_input.time().toString("HH:mm")}
                        Длительность: {self.duration_input.text()} ч.
                        Участники: {participants}
                        Повестки совещания:\n {self.topics_input.toPlainText()}
                        Дополнительные участники: {"Да" if self.additional_participants_checkbox.isChecked() else "Нет"}
                        """
        if self.additional_participants_checkbox.isChecked() and self.external_participants_input:
            summary += f"""
                            Председатель: {self.chairperson_input.currentText()}
                            Секретарь: {self.secretary_input.currentText()}
                            Контролёр: {self.controller_input.currentText()}
                            Внешние участники: {', '.join([item.text() for item in self.external_participants_input.selectedItems()])}
                            """

        self.summary_text.setText(summary)

    def add_question(self):
        dialog = AddQuestionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            question = dialog.get_question_data()
            self.topics_input.append(
                f"\tВопрос: {question['text']}\n\tОтветчик: {question['responder']}\n\tПрикреплённые файлы: {question['files']}\n")