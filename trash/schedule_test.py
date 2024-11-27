from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from ui.widgets.event_list_widget import EventListWidget  # Импортируем наш виджет


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")

        # Данные мероприятий
        events = [
            {"Дата": "25 Ноября", "Тема": "Исповедь основного обучения :)", "Время": "18:00 - 19:00", "details": "Старшие волны поделятся, как проходило их обучение."},
            {"Дата": "26 Ноября", "Тема": "Мастер-класс (уровень 1) по 3D моделированию", "Время": "14:00 - 15:00", "details": "В лаборатории можно пройти серию практических занятий."},
            {"Дата": "27 Ноября", "Тема": "АНГЛИЙСКИЙ совместно с Лигой Студентов", "Время": "18:30 - 20:00", "details": "Занятия, которые проводят Лига студентов для всех желающих."},
            {"Дата": "27 Ноября", "Тема": "Meetup: Введение в Kubernetes", "Время": "19:00 - 20:00", "details": "На мероприятии участники знакомятся с основами Kubernetes."},
        ]

        # Главный виджет
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Добавляем EventListWidget
        event_list_widget = EventListWidget(events)
        main_layout.addWidget(event_list_widget)

        # Устанавливаем главный виджет
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
