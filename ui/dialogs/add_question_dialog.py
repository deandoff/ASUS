from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QHBoxLayout, QFileDialog


class AddQuestionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить вопрос")

        layout = QVBoxLayout(self)

        # Вопрос
        self.question_input = QLineEdit(self)
        self.question_input.setPlaceholderText("Введите вопрос")
        layout.addWidget(QLabel("Вопрос:"))
        layout.addWidget(self.question_input)

        # Ответчик
        self.responder_input = QComboBox(self)
        self.responder_input.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])
        layout.addWidget(QLabel("Ответчик:"))
        layout.addWidget(self.responder_input)

        # Прикрепление файлов
        self.files_input = QPushButton("Прикрепить файлы")
        self.files_input.clicked.connect(self.attach_files)
        layout.addWidget(self.files_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Добавить")
        self.accept_button.clicked.connect(self.accept)
        button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.selected_files = []  # Список выбранных файлов

    def attach_files(self):
        """Открыть диалоговое окно для выбора файлов."""
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы")
        if files:
            self.selected_files.extend(files)

    def get_question_data(self):
        """Получить введенные данные о вопросе."""
        return {
            "text": self.question_input.text(),
            "responder": self.responder_input.currentText(),
            "files": ", ".join(self.selected_files),
        }