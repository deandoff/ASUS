import psycopg2
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Qt

from ui.windows.main_window import MainWindow

db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user_data = {}

        self.setWindowTitle("ASUS Authorization")
        self.setFixedSize(500, 300)

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet('''background-color: #F0FFFF;''')

        # Заголовок "Вход"
        self.label_title = QLabel("Вход")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet('''font-family: Roboto Slab; 
                                            font-size: 24px; 
                                            font-weight: bold; 
                                            color: black; 
                                            margin-bottom: 20px;''')

        # Создание меток и полей ввода
        self.label_username = QLabel("Логин")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Введите логин")
        self.input_username.setFixedSize(300, 40)
        self.input_username.setAlignment(Qt.AlignCenter)
        self.input_username.setStyleSheet('''font-family: Roboto Slab; 
                                               font-size: 17px;
                                               border: 2px solid black;
                                               border-radius: 10px;
                                               padding: 5px;
                                               ''')
        self.input_username.returnPressed.connect(self.focus_on_password)

        self.label_password = QLabel("Пароль")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setFixedSize(300, 40)
        self.input_password.setAlignment(Qt.AlignCenter)
        self.input_password.setStyleSheet('''font-family: Roboto Slab; 
                                               font-size: 17px;
                                               border: 2px solid black;
                                               border-radius: 10px;
                                               padding: 5px;
                                               ''')
        self.input_password.returnPressed.connect(self.handle_login)

        # Кнопка авторизации
        self.button_login = QPushButton("Авторизоваться")
        self.button_login.clicked.connect(self.handle_login)
        self.button_login.setFixedSize(200, 40)
        self.button_login.setStyleSheet('''font-family: Roboto Slab; 
                                             font-size: 17px; 
                                             color: white; 
                                             background-color: black; 
                                             border: 2px solid black; 
                                             border-radius: 10px; 
                                             padding: 5px; 
                                             ''')

        # Компоновка
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.label_title, alignment=Qt.AlignCenter)  # Добавляем заголовок
        layout.addWidget(self.input_username, alignment=Qt.AlignCenter)
        layout.addWidget(self.input_password, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.button_login, alignment=Qt.AlignCenter)

        self.central_widget.setLayout(layout)

    def focus_on_password(self):
        self.input_password.setFocus()

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        user_data = self.check_credentials(username, password)
        if user_data:
            self.user_data = user_data
            self.close()  # Закрываем окно авторизации
            self.open_main_window()  # Открываем главное окно
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин и/или пароль")
            self.input_username.clear()
            self.input_password.clear()

    def check_credentials(self, username, password):
        """
        Проверяет, существует ли пользователь с заданным логином и паролем в базе данных.
        Возвращает словарь с данными пользователя (id и role), если успех, иначе None.
        """
        DATABASE_URL = db_url

        try:
            # Подключение к базе данных
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()

            # Выполнение SQL-запроса
            query = """
                SELECT id, role FROM Users
                WHERE login = %s AND password = %s
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            # Закрытие соединения
            cursor.close()
            conn.close()

            if user:
                self.user_data = {"id": user[0], "role": user[1]}
                return {"id": user[0], "role": user[1]}
            return None

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось подключиться к базе данных:\n{e}")
            return None
    def open_main_window(self):
        self.main_window = MainWindow(self.user_data)
        self.main_window.show()