from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QCheckBox


class SearchableMultiSelect(QWidget):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 200)

        self.items = items or []

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Search box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Поиск...")
        self.search_box.textChanged.connect(self.filter_items)
        layout.addWidget(self.search_box)

        # List widget with checkboxes
        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        self.populate_list()

        self.setLayout(layout)

    def populate_list(self):
        """Добавляет элементы с чекбоксами."""
        self.list_widget.clear()
        for item in self.items:
            list_item = QListWidgetItem(self.list_widget)
            checkbox = QCheckBox(item)
            checkbox.stateChanged.connect(self.on_state_changed)  # Update state on check
            self.list_widget.setItemWidget(list_item, checkbox)
            list_item.setSizeHint(checkbox.sizeHint())

    def filter_items(self, text):
        """Фильтрует элементы на основе ввода в поиске."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            item.setHidden(text.lower() not in widget.text().lower())

    def get_selected_items(self):
        """Возвращает список выбранных элементов."""
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if widget.isChecked():
                selected.append(widget.text())
        return selected

    def set_selected_items(self, selected_items):
        """Устанавливает элементы как выбранные."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            widget.setChecked(widget.text() in selected_items)

    def on_state_changed(self, state):
        """Дополнительная логика при изменении состояния."""
        pass