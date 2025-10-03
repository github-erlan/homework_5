import sys, os
import PyQt6.QtCore

# --- Фикс для macOS: Qt иногда не находит плагины (cocoa) ---
plugin_path = os.path.join(os.path.dirname(PyQt6.QtCore.__file__), "Qt6", "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QSpinBox, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt


class ShoppingListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список покупок")
        self.resize(400, 400)

        layout = QVBoxLayout(self)

        # Поля ввода
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название товара")
        self.amount_input = QSpinBox()
        self.amount_input.setRange(1, 99)
        self.amount_input.setValue(1)
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.amount_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        self.toggle_btn = QPushButton("Отметить купленным")
        self.clear_btn = QPushButton("Очистить купленные")

        for b in [self.add_btn, self.edit_btn, self.delete_btn, self.toggle_btn, self.clear_btn]:
            button_layout.addWidget(b)

        # Список покупок
        self.list_widget = QListWidget()

        # Статус-бар
        self.status_bar = QStatusBar()
        self.update_status()

        # Сборка интерфейса
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.status_bar)

        # Сигналы
        self.add_btn.clicked.connect(self.add_item)
        self.edit_btn.clicked.connect(self.edit_item)
        self.delete_btn.clicked.connect(self.delete_item)
        self.toggle_btn.clicked.connect(self.toggle_item)
        self.clear_btn.clicked.connect(self.clear_purchased)
        self.list_widget.itemDoubleClicked.connect(self.fill_inputs)

    def add_item(self):
        name = self.name_input.text().strip()
        amount = self.amount_input.value()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название товара не может быть пустым!")
            return
        item = QListWidgetItem(f"{name} × {amount}")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.list_widget.addItem(item)
        self.update_status()

    def edit_item(self):
        item = self.list_widget.currentItem()
        if item:
            name = self.name_input.text().strip()
            amount = self.amount_input.value()
            if not name:
                QMessageBox.warning(self, "Ошибка", "Название товара не может быть пустым!")
                return
            item.setText(f"{name} × {amount}")
            self.update_status()

    def delete_item(self):
        item = self.list_widget.currentItem()
        if item:
            reply = QMessageBox.question(
                self, "Подтверждение", "Удалить выбранный элемент?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                row = self.list_widget.row(item)
                self.list_widget.takeItem(row)
                self.update_status()

    def toggle_item(self):
        item = self.list_widget.currentItem()
        if item:
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)
            self.update_status()

    def clear_purchased(self):
        reply = QMessageBox.question(
            self, "Подтверждение", "Удалить все купленные товары?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            for i in reversed(range(self.list_widget.count())):
                item = self.list_widget.item(i)
                if item.checkState() == Qt.CheckState.Checked:
                    self.list_widget.takeItem(i)
            self.update_status()

    def fill_inputs(self, item):
        text = item.text()
        if "×" in text:
            name, amount = text.split("×")
            self.name_input.setText(name.strip())
            self.amount_input.setValue(int(amount.strip()))

    def update_status(self):
        total = self.list_widget.count()
        purchased = sum(1 for i in range(total) if self.list_widget.item(i).checkState() == Qt.CheckState.Checked)
        self.status_bar.showMessage(f"Всего: {total} | Куплено: {purchased}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoppingListApp()
    window.show()
    sys.exit(app.exec())
