from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QStackedWidget, \
    QListWidget, QAbstractItemView, QComboBox


class AdminPanelWidget(QWidget):
    def __init__(self, parent=None):
        super(AdminPanelWidget, self).__init__(parent)

        self.layout = QHBoxLayout()

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)

        self.add_participant_button = QPushButton("Добавить участника")
        self.add_participant_button.clicked.connect(self.add_participant)
        self.button_layout.addWidget(self.add_participant_button)
        self.add_participant_button.setStyleSheet('''font-family: Roboto Slab; 
                                                     font-size: 17px; 
                                                     color: white; 
                                                     background-color: black; 
                                                     border: 2px solid black; 
                                                     border-radius: 10px; 
                                                     padding: 5px; 
                                                     ''')

        self.update_the_participant_button = QPushButton("Изменить участника")
        self.update_the_participant_button.clicked.connect(self.update_the_participant)
        self.button_layout.addWidget(self.update_the_participant_button)
        self.update_the_participant_button.setStyleSheet('''font-family: Roboto Slab; 
                                                     font-size: 17px; 
                                                     color: white; 
                                                     background-color: black; 
                                                     border: 2px solid black; 
                                                     border-radius: 10px; 
                                                     padding: 5px; 
                                                     ''')

        self.layout.addLayout(self.button_layout, stretch=2)

        self.form_widget = QStackedWidget()
        self.add_participant_index = 0

        self.layout.addWidget(self.form_widget, stretch=5)

        self.setLayout(self.layout)

        self.setStyleSheet("""font-family: Roboto Slab; 
                              font-size: 14px;""")
        self.form_widget.setStyleSheet("""QLineEdit {background-color: #E0FFFF;
                border-style: solid; /* Устанавливает стиль границы */
                border-width: 2px; /* Толщина границы */
                border-color: #808080; /* Цвет границы */
                padding: 8px;
                margin: 5px;
                border-radius: 4px;}""")

    def add_participant(self):
        self.sub_widget = QWidget()
        sub_layout = QFormLayout(self.sub_widget)

        self.name_input = QLineEdit()
        sub_layout.addRow("Фамилия И.О.", self.name_input)

        self.post_input = QLineEdit()
        sub_layout.addRow("Должность", self.post_input)

        self.email_input = QLineEdit()
        sub_layout.addRow("Почта", self.email_input)

        self.number_input = QLineEdit()
        sub_layout.addRow("Номер", self.number_input)

        self.role_input = QComboBox()
        self.role_input.addItems(["Организатор", "Участник", "Гость"])
        sub_layout.addRow("Роль:", self.role_input)

        self.save_info_button = QPushButton("Добавить")
        self.save_info_button.clicked.connect(self.save_info)
        self.save_info_button.setStyleSheet('''font-family: Roboto Slab; 
                                                     font-size: 17px; 
                                                     color: white; 
                                                     background-color: black; 
                                                     border: 2px solid black; 
                                                     border-radius: 10px; 
                                                     padding: 5px; 
                                                     ''')
        sub_layout.addWidget(self.save_info_button)

        self.form_widget.addWidget(self.sub_widget)
        self.form_widget.setCurrentWidget(self.sub_widget)

    def update_the_participant(self):
        # Создаем виджет для изменения участника
        self.update_widget = QWidget()
        update_layout = QFormLayout(self.update_widget)

        # Выпадающий список для выбора участника
        self.participant_selector = QComboBox()
        self.participant_selector.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])  # Список участников
        self.participant_selector.currentIndexChanged.connect(self.load_participant_data)
        update_layout.addRow("Выберите участника:", self.participant_selector)

        # Поля для редактирования данных участника
        self.name_edit = QLineEdit()
        update_layout.addRow("Фамилия И.О.", self.name_edit)

        self.post_edit = QLineEdit()
        update_layout.addRow("Должность", self.post_edit)

        self.email_edit = QLineEdit()
        update_layout.addRow("Почта", self.email_edit)

        self.number_edit = QLineEdit()
        update_layout.addRow("Номер", self.number_edit)

        self.role_edit = QComboBox()
        self.role_edit.addItems(["Организатор", "Участник", "Гость"])
        update_layout.addRow("Роль:", self.role_edit)

        # Кнопка для сохранения изменений
        self.save_changes_button = QPushButton("Сохранить изменения")
        self.save_changes_button.clicked.connect(self.save_changes)
        self.save_changes_button.setStyleSheet('''font-family: Roboto Slab; 
                                                     font-size: 17px; 
                                                     color: white; 
                                                     background-color: black; 
                                                     border: 2px solid black; 
                                                     border-radius: 10px; 
                                                     padding: 5px; 
                                                     ''')
        update_layout.addWidget(self.save_changes_button)

        # Добавляем виджет в `QStackedWidget` и показываем
        self.form_widget.addWidget(self.update_widget)
        self.form_widget.setCurrentWidget(self.update_widget)

        # Загружаем данные для первого участника, если есть
        if self.participant_selector.count() > 0:
            self.load_participant_data()

    def load_participant_data(self):
        """
        Загружает данные выбранного участника в поля редактирования.
        Здесь вы можете подгружать данные из базы данных или словаря.
        """
        # Пример данных для участников (можно заменить на реальные)
        participants_data = {
            "Иванов И.И.": {"name": "Иванов И.И.", "post": "Директор", "email": "ivanov@example.com",
                            "number": "1234567890", "role": "Организатор"},
            "Петров П.П.": {"name": "Петров П.П.", "post": "Менеджер", "email": "petrov@example.com",
                            "number": "9876543210", "role": "Участник"},
            "Сидоров С.С.": {"name": "Сидоров С.С.", "post": "Аналитик", "email": "sidorov@example.com",
                             "number": "1122334455", "role": "Гость"},
        }

        # Получаем текущего участника
        selected_participant = self.participant_selector.currentText()
        if selected_participant in participants_data:
            data = participants_data[selected_participant]

            # Загружаем данные в поля редактирования
            self.name_edit.setText(data["name"])
            self.post_edit.setText(data["post"])
            self.email_edit.setText(data["email"])
            self.number_edit.setText(data["number"])
            self.role_edit.setCurrentText(data["role"])

    def save_changes(self):
        """
        Сохраняет изменения данных участника.
        Здесь можно отправить данные в базу данных или обновить локальный список.
        """
        updated_data = {
            "name": self.name_edit.text(),
            "post": self.post_edit.text(),
            "email": self.email_edit.text(),
            "number": self.number_edit.text(),
            "role": self.role_edit.currentText(),
        }
        print(f"Данные участника обновлены: {updated_data}")
        self.form_widget.setCurrentWidget(self.sub_widget)

    def save_info(self):
        '''Сохранение инфы в базу'''
        pass

