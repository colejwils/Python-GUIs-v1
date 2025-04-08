import sys
from PySide6.QtCore import Qt, Signal, Slot
# ACTION FIX: Import QAction from QtGui, not QtWidgets
from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QStatusBar,
    QDialogButtonBox,
    QHeaderView,
)


# ─────────────────────────────────────────────────────────────────
# 1. LoginDialog
# ─────────────────────────────────────────────────────────────────
class LoginDialog(QDialog):
    login_success = Signal(str)  # Emitted when login is successful, passes username

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")

        layout = QVBoxLayout()

        # Username
        user_layout = QHBoxLayout()
        user_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.username_edit)

        # Password
        pass_layout = QHBoxLayout()
        pass_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(pass_label)
        pass_layout.addWidget(self.password_edit)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.handle_login)
        button_box.rejected.connect(self.reject)

        layout.addLayout(user_layout)
        layout.addLayout(pass_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    @Slot()
    def handle_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        # For simplicity, let's accept any non-empty username/password
        if username and password:
            self.login_success.emit(username)
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Username/Password cannot be empty!"
            )


# ─────────────────────────────────────────────────────────────────
# 2. AddItemDialog
# ─────────────────────────────────────────────────────────────────
class AddItemDialog(QDialog):
    item_added = Signal(str)  # Emitted when a new item is added

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Item")

        layout = QVBoxLayout()

        # A simple field for item name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter item name...")

        layout.addWidget(QLabel("Item Name:"))
        layout.addWidget(self.name_edit)

        # OK / Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.ok_clicked)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    @Slot()
    def ok_clicked(self):
        name = self.name_edit.text().strip()
        if name:
            self.item_added.emit(name)
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Item name cannot be empty!"
            )


# ─────────────────────────────────────────────────────────────────
# 3. MainWindow
# ─────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    logout_requested = Signal()  # Emitted when user requests logout

    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"PySide6 Advanced Example - Logged in as {username}")
        self.resize(600, 400)

        # A simple in-memory list of items
        self.items = []
        self.item_id_counter = 0

        # Set up central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome!")

        # Create a toolbar with an “Add Item” action
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        add_item_action = QAction("Add Item", self)
        add_item_action.triggered.connect(self.open_add_item_dialog)
        self.toolbar.addAction(add_item_action)

        # Menu bar with “File -> Logout”
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.handle_logout)
        file_menu.addAction(logout_action)

        # Table to display items
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # ID, Name
        self.table.setHorizontalHeaderLabels(["ID", "Name"])
        # Make the columns stretch to fit the width
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.table)

    @Slot()
    def handle_logout(self):
        """Emit the logout signal so the main application can handle it."""
        self.logout_requested.emit()

    @Slot()
    def open_add_item_dialog(self):
        dialog = AddItemDialog(self)
        dialog.item_added.connect(self.add_item)
        dialog.exec()

    @Slot(str)
    def add_item(self, name):
        """Add an item to the list and refresh the table."""
        self.item_id_counter += 1
        self.items.append((self.item_id_counter, name))
        self.refresh_table()
        self.status_bar.showMessage(f"Item '{name}' added!", 3000)

    def refresh_table(self):
        """Repopulate the table with current items."""
        self.table.setRowCount(len(self.items))
        for row_index, (item_id, item_name) in enumerate(self.items):
            # ID
            id_item = QTableWidgetItem(str(item_id))
            # make ID read-only
            id_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row_index, 0, id_item)

            # Name
            name_item = QTableWidgetItem(item_name)
            self.table.setItem(row_index, 1, name_item)


# ─────────────────────────────────────────────────────────────────
# 4. Application “Flow”
# ─────────────────────────────────────────────────────────────────
class AdvancedPySideApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_dialog = LoginDialog()
        self.main_window = None

        # Connect signals
        self.login_dialog.login_success.connect(self.on_login_success)

    def run(self):
        # Start by showing the login dialog
        self.login_dialog.exec()

        # If login was successful, the main window will have been created
        # and shown in on_login_success(); if user canceled, the app ends.
        if self.main_window:
            sys.exit(self.app.exec())
        else:
            # User canceled or closed the login dialog without logging in
            sys.exit(0)

    @Slot(str)
    def on_login_success(self, username):
        # Create and show main window
        self.main_window = MainWindow(username)
        self.main_window.logout_requested.connect(self.on_logout_requested)
        self.login_dialog.close()
        self.main_window.show()

    @Slot()
    def on_logout_requested(self):
        # Close the main window and bring back the login dialog
        if self.main_window:
            self.main_window.close()
            self.main_window = None

        # Clear username/password fields
        self.login_dialog.username_edit.clear()
        self.login_dialog.password_edit.clear()

        # Show login dialog again
        self.login_dialog.exec()


# ─────────────────────────────────────────────────────────────────
# 5. Main Entry Point
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app_flow = AdvancedPySideApp()
    app_flow.run()
