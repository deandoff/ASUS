from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QSpacerItem, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, QRect

from ui.main_window import MainAppWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ASUS Authorization")
        self.setFixedSize(500,300)

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создание меток и полей ввода
        self.label_username = QLabel()
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Введите логин")
        self.input_username.setLayout(QVBoxLayout())
        self.input_username.setFixedSize(480,40)
        self.input_username.setAlignment(Qt.AlignCenter)


        self.label_password = QLabel()
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setFixedSize(480,40)
        self.input_password.setAlignment(Qt.AlignCenter)


        # Кнопка авторизации
        self.button_login = QPushButton("Авторизоваться")
        self.button_login.clicked.connect(self.handle_login)
        self.button_login.setFixedSize(480,40)

        # Компоновка
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Центрирование всего содержимого
        layout.addStretch(1)
        layout.addWidget(self.input_username)
        layout.addWidget(self.input_password)
        layout.addStretch(1)
        layout.addWidget(self.button_login)

        self.central_widget.setLayout(layout)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username == "admin" and password == "password":
            self.close()  # Закрываем окно авторизации
            self.open_main_window()  # Открываем главное окно
        else:
            QMessageBox.information(self,"Ошибка авторизации", "Неверный логин и/или пароль")
            self.input_username.clear()
            self.input_password.clear()

    def open_main_window(self):
        self.main_window = MainAppWindow()
        self.main_window.show()

if __name__ == "__main__":
    app = QApplication([])

    window = LoginWindow()
    window.show()

    app.exec()
