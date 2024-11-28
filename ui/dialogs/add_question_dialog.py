from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QHBoxLayout, QFileDialog
import psycopg2

db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"


def get_responders_from_db():
    """Получить список ответчиков из базы данных."""
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT id, login FROM Users WHERE role IN ('USER', 'CREATOR', 'GUEST')")
        responders = cursor.fetchall()
        return {responder[1]: responder[0] for responder in responders}  # Возвращаем словарь с логинами и ID
    except Exception as e:
        print(f"Ошибка при загрузке ответчиков: {e}")
        return {}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


class AddQuestionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить вопрос")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout(self)

        # Вопрос
        self.question_input = QLineEdit(self)
        self.question_input.setPlaceholderText("Введите вопрос")
        layout.addWidget(QLabel("Вопрос:"))
        layout.addWidget(self.question_input)

        # Ответчик
        self.responder_input = QComboBox(self)
        self.load_responders()  # Загружаем ответчиков из базы данных
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
        self.setStyleSheet(""" QPushButton{font-family: Roboto Slab; 
                                                     font-size: 17px; 
                                                     color: white; 
                                                     background-color: black; 
                                                     border: 2px solid black; 
                                                     border-radius: 10px; 
                                                     padding: 5px;}
                        QLineEdit {background-color: #E0FFFF;
                        border-style: solid; 
                        border-width: 2px; 
                        border-color: #808080; 
                        padding: 8px;
                        margin: 5px;
                        border-radius: 4px;}

                        QComboBox{background-color: #E0FFFF;
                        border-style: solid; 
                        border-width: 2px; 
                        border-color: #808080; 
                        padding: 8px;
                        margin: 5px;
                        border-radius: 4px;}""")

        self.selected_files = []  # Список выбранных файлов
        self.responder_id_dict = get_responders_from_db()  # Словарь с ID ответчиков

    def load_responders(self):
        """Загружает ответчиков из базы данных в выпадающий список."""
        responders = get_responders_from_db()
        self.responder_input.addItems(responders.keys())  # Добавляем логины ответчиков в выпадающий список

    def attach_files(self):
        """Открыть диалоговое окно для выбора файлов."""
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы")
        if files:
            self.selected_files.extend(files)

    def get_question_data(self):
        """Получить введенные данные о вопросе."""
        responder_name = self.responder_input.currentText()
        responder_id = self.responder_id_dict.get(responder_name)  # Получаем ID ответчика
        return {
            "text": self.question_input.text(),
            "responder": responder_name,
            "responder_id": responder_id,  # Добавляем ID ответчика
            "files": ", ".join(self.selected_files),
        }