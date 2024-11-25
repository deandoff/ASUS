from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
)
from PySide6.QtCore import QSize


class EventListWidget(QWidget):
    def __init__(self, events, parent=None):
        super().__init__(parent)

        # Сохранение данных о мероприятиях
        self.events = events

        # Основной макет виджета
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Список мероприятий
        self.events_list = QListWidget()
        self.events_list.itemClicked.connect(self.show_event_details)
        self.events_list.setStyleSheet("""
                    QListWidget {
                        background-color: #f9f9f9; /* Фон списка */
                        border: 1px solid #ddd; /* Граница */
                        border-radius: 8px; /* Скругленные углы */
                        padding: 5px;
                    }
                    QListWidget::item {
                        background-color: #ffffff; /* Фон элемента */
                        border: 1px solid #e0e0e0; /* Граница элемента */
                        margin: 5px; /* Отступ между элементами */
                        padding: 10px; /* Отступы внутри элемента */
                        border-radius: 8px; /* Скругленные углы */
                    }
                    QListWidget::item:hover {
                        background-color: #f0f0f0; /* Фон при наведении */
                    }
                    QListWidget::item:selected {
                        background-color: #e0f7fa; /* Фон выбранного элемента */
                        border: 1px solid #4fc3f7; /* Граница выбранного элемента */
                    }
                """)

        self.populate_events()
        self.layout.addWidget(self.events_list)

        # Кнопка для открытия полного списка мероприятий
        self.btn_all_events = QPushButton("Все мероприятия")
        self.btn_all_events.clicked.connect(self.show_all_events)
        self.layout.addWidget(self.btn_all_events)

    def populate_events(self):
        """Создает элементы списка мероприятий."""
        self.events_list.clear()  # Очистка старых элементов
        for index, event in enumerate(self.events[:4]):
            # Создаем виджет для элемента
            item_widget = QWidget()
            item_layout = QVBoxLayout()
            item_layout.setContentsMargins(10, 10, 10, 10)

            # Верхняя строка: Дата мероприятия
            date_label = QLabel(f"<b>{event['Дата']}</b>")
            date_label.setStyleSheet("color: #6c757d; font-size: 14px;")
            item_layout.addWidget(date_label)

            # Средняя строка: Название мероприятия
            title_label = QLabel(event["Тема"])
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
            item_layout.addWidget(title_label)

            # Нижняя строка: Время мероприятия
            time_label = QLabel(event["Время"])
            time_label.setStyleSheet("color: #495057; font-size: 14px;")
            item_layout.addWidget(time_label)

            # Применение макета к виджету
            item_widget.setLayout(item_layout)

            # Упаковка виджета в QListWidgetItem
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint() + QSize(0, 35))

            self.events_list.addItem(list_item)
            self.events_list.setItemWidget(list_item, item_widget)

    def show_all_events(self):
        """Открывает окно с полным списком мероприятий."""
        print("Показать все мероприятия.")

    def show_event_details(self, item):
        """Показывает детали мероприятия при выборе элемента."""
        print("Детальная информация о мероприятии.")