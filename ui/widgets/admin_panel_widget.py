from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QStackedWidget, \
    QComboBox, QMessageBox
import psycopg2

db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"


class AdminPanelWidget(QWidget):
    def __init__(self, parent=None):
        super(AdminPanelWidget, self).__init__(parent)

        self.layout = QHBoxLayout()

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)

        self.add_participant_button = QPushButton("Добавить участника")
        self.add_participant_button.clicked.connect(self.add_participant)
        self.button_layout.addWidget(self.add_participant_button)
        self.add_participant_button.setStyleSheet(self.button_style())

        self.update_the_participant_button = QPushButton("Изменить участника")
        self.update_the_participant_button.clicked.connect(self.update_the_participant)
        self.button_layout.addWidget(self.update_the_participant_button)
        self.update_the_participant_button.setStyleSheet(self.button_style())

        self.layout.addLayout(self.button_layout, stretch=2)

        self.form_widget = QStackedWidget()
        self.add_participant_index = 0

        self.layout.addWidget(self.form_widget, stretch=5)

        self.setLayout(self.layout)

        self.setStyleSheet("""font-family: Roboto Slab; 
                              font-size: 14px;""")
        self.form_widget.setStyleSheet(self.input_style())

    def button_style(self):
        return '''font-family: Roboto Slab; 
                  font-size: 17px; 
                  color: white; 
                  background-color: black; 
                  border: 2px solid black; 
                  border-radius: 10px; 
                  padding: 5px;'''

    def input_style(self):
        return """QLineEdit {background-color: #E0FFFF;
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
                        border-radius: 4px;}"""

    def add_participant(self):
        self.sub_widget = QWidget()
        sub_layout = QFormLayout(self.sub_widget)

        self.name_input = QLineEdit()
        sub_layout.addRow("Логин", self.name_input)

        self.post_input = QLineEdit()
        sub_layout.addRow("Пароль", self.post_input)

        self.role_edit = QComboBox()
        self.role_edit.addItems(["ADMIN", "USER", "CREATOR", "GUEST", "SECRETARY"])
        sub_layout.addRow("Роль:", self.role_edit)

        self.save_info_button = QPushButton("Добавить")
        self.save_info_button.clicked.connect(self.save_info)
        self.save_info_button.setStyleSheet(self.button_style())
        sub_layout.addWidget(self.save_info_button)

        self.form_widget.addWidget(self.sub_widget)
        self.form_widget.setCurrentWidget(self.sub_widget)

    def update_the_participant(self):
        # Создаем виджет для изменения участника
        self.update_widget = QWidget()
        update_layout = QFormLayout(self.update_widget)

        # Выпадающий список для выбора участника
        self.participant_selector = QComboBox()
        self.load_participants()  # Загружаем участников из базы данных
        self.participant_selector.currentIndexChanged.connect(self.load_participant_data)
        update_layout.addRow("Выберите участника:", self.participant_selector)

        # Поля для редактирования данных участника
        self.name_edit = QLineEdit()
        update_layout.addRow("Логин", self.name_edit)

        self.post_edit = QLineEdit()
        update_layout.addRow("Пароль", self.post_edit)

        self.role_edit = QComboBox()
        self.role_edit.addItems(["ADMIN", "USER", "CREATOR", "GUEST", "SECRETARY"])
        update_layout.addRow("Роль:", self.role_edit)

        # К нопка для сохранения изменений
        self.save_changes_button = QPushButton("Сохранить изменения")
        self.save_changes_button.clicked.connect(self.save_changes)
        self.save_changes_button.setStyleSheet(self.button_style())
        update_layout.addWidget(self.save_changes_button)

        # Добавляем виджет в `QStackedWidget` и показываем
        self.form_widget.addWidget(self.update_widget)
        self.form_widget.setCurrentWidget(self.update_widget)

        # Загружаем данные для первого участника, если есть
        if self.participant_selector.count() > 0:
            self.load_participant_data()

    def load_participants(self):
        """Загружает участников из базы данных в выпадающий список."""
        try:
            connection = psycopg2.connect(db_url)
            cursor = connection.cursor()
            cursor.execute("SELECT login FROM Users")
            participants = cursor.fetchall()
            self.participant_selector.addItems([participant[0] for participant in participants])
        except Exception as e:
            print(f"Ошибка при загрузке участников: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def load_participant_data(self):
        """Загружает данные выбранного участника в поля редактирования."""
        selected_participant = self.participant_selector.currentText()
        if selected_participant:
            try:
                connection = psycopg2.connect(db_url)
                cursor = connection.cursor()
                cursor.execute("SELECT login, password, role FROM Users WHERE login = %s", (selected_participant,))
                data = cursor.fetchone()
                if data:
                    self.name_edit.setText(data[0])
                    self.post_edit.setText(data[1])
                    self.role_edit.setCurrentText(data[2])
            except Exception as e:
                print(f"Ошибка при загрузке данных участника: {e}")
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

    def save_changes(self):
        """Сохраняет изменения данных участника в базе данных."""
        login = self.name_edit.text().strip()
        password = self.post_edit.text().strip()
        role = self.role_edit.currentText()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми.")
            return

        if len(login) > 30 or len(password) > 30:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль должны быть не более 30 символов.")
            return

        try:
            connection = psycopg2.connect(db_url)
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Users
                SET password = %s, role = %s
                WHERE login = %s
            """, (password, role, login))
            connection.commit()
            QMessageBox.information(self, "Успех", "Данные участника успешно обновлены.")
              # Возвращаемся к добавлению участника
        except Exception as e:
            print(f"Ошибка при сохранении изменений: {e}")
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить изменения.")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def save_info(self):
        """Сохранение информации о новом участнике в базе данных."""
        login = self.name_input.text().strip()
        password = self.post_input.text().strip()
        role = self.role_edit.currentText()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми.")
            return

        if len(login) > 30 or len(password) > 30:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль должны быть не более 30 символов.")
            return

        try:
            connection = psycopg2.connect(db_url)
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Users (login, password, role)
                VALUES (%s, %s, %s)
            """, (login, password, role))
            connection.commit()
            QMessageBox.information(self, "Успех", "Участник успешно добавлен.")
            self.form_widget.setCurrentWidget(self.sub_widget)  # Возвращаемся к добавлению участника
        except Exception as e:
            print(f"Ошибка при добавлении участника: {e}")
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить участника.")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()