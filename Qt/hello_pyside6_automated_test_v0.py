import sys
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QToolBar,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QStatusBar,
    QWidget,
    QTableWidgetSelectionRange,
    QDialogButtonBox,
    QMenuBar,
)

# ─────────────────────────────────────────────────────────────────
# 1. LoginDialog
# ─────────────────────────────────────────────────────────────────
class LoginDialog(QDialog):
    login_success = Signal(str)

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
        if username and password:
            # For simplicity, accept any non-empty credentials.
            self.login_success.emit(username)
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Username/Password cannot be empty!")

# ─────────────────────────────────────────────────────────────────
# 2. TestConfigDialog
# ─────────────────────────────────────────────────────────────────
class TestConfigDialog(QDialog):
    """
    Dialog for configuring and running a specific test.
    """
    def __init__(self, test_id: str, test_name: str, config_data: dict, parent=None):
        super().__init__(parent)
        self.test_id = test_id
        self.test_name = test_name
        self.config_data = config_data  # e.g. {"username": "", "password": "", "eap_type": "PEAP"}

        self.setWindowTitle(f"Configure {test_name}")
        self.resize(400, 200)

        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel(test_name)
        title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        main_layout.addWidget(title_label)

        # Username
        user_layout = QHBoxLayout()
        user_label = QLabel("Test Username:")
        self.username_edit = QLineEdit(self.config_data["username"])
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.username_edit)
        main_layout.addLayout(user_layout)

        # Password
        pass_layout = QHBoxLayout()
        pass_label = QLabel("Test Password:")
        self.password_edit = QLineEdit(self.config_data["password"])
        self.password_edit.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(pass_label)
        pass_layout.addWidget(self.password_edit)
        main_layout.addLayout(pass_layout)

        # EAP Type
        eap_layout = QHBoxLayout()
        eap_label = QLabel("EAP Type:")
        self.eap_combo = QComboBox()
        # example EAP options
        eap_options = ["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"]
        self.eap_combo.addItems(eap_options)
        self.eap_combo.setCurrentText(self.config_data["eap_type"])
        eap_layout.addWidget(eap_label)
        eap_layout.addWidget(self.eap_combo)
        main_layout.addLayout(eap_layout)

        # OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.run_test)
        button_box.rejected.connect(self.reject)

        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    @Slot()
    def run_test(self):
        # Update our config data from the form
        self.config_data["username"] = self.username_edit.text().strip()
        self.config_data["password"] = self.password_edit.text().strip()
        self.config_data["eap_type"] = self.eap_combo.currentText()

        QMessageBox.information(
            self,
            "Running Test",
            f"Running {self.test_name} with EAP={self.config_data['eap_type']}..."
        )
        # Real test logic goes here...
        self.accept()

# ─────────────────────────────────────────────────────────────────
# 3. MainWindow
# ─────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    logout_requested = Signal()

    def __init__(self, username: str, parent=None):
        super().__init__(parent)
        self.username = username
        self.setWindowTitle(f"Automated Test Manager - Logged in as {username}")
        self.resize(600, 400)

        # A simple table of tests
        self.tests = [
            {"id": "test1", "name": "Automated WLAN Test #1"},
            {"id": "test2", "name": "Automated WLAN Test #2"},
        ]
        # Per-test configuration data
        self.test_configs = {
            "test1": {"username": "", "password": "", "eap_type": "PEAP"},
            "test2": {"username": "", "password": "", "eap_type": "PEAP"},
        }

        # Central widget with table
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to the Automated Test Manager!")

        # Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        add_action = QAction("Add test (demo)", self)
        add_action.triggered.connect(self.add_new_test_demo)
        self.toolbar.addAction(add_action)

        # Menu bar with “File -> Logout”
        menubar = QMenuBar()
        self.setMenuBar(menubar)
        file_menu = menubar.addMenu("File")

        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.handle_logout)
        file_menu.addAction(logout_action)

        # Build test table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Test ID", "Test Name"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.cellDoubleClicked.connect(self.on_table_double_click)

        layout.addWidget(QLabel(f"Hello, {self.username}! Select a test below:", parent=central_widget))
        layout.addWidget(self.table)
        self.refresh_table()

    @Slot()
    def handle_logout(self):
        self.logout_requested.emit()

    def refresh_table(self):
        self.table.setRowCount(len(self.tests))
        for i, t in enumerate(self.tests):
            # Test ID
            item_id = QTableWidgetItem(t["id"])
            self.table.setItem(i, 0, item_id)
            # Test Name
            item_name = QTableWidgetItem(t["name"])
            self.table.setItem(i, 1, item_name)

    @Slot(int, int)
    def on_table_double_click(self, row, column):
        if row < len(self.tests):
            test_id = self.tests[row]["id"]
            test_name = self.tests[row]["name"]
            self.open_test_config_dialog(test_id, test_name)

    def open_test_config_dialog(self, test_id, test_name):
        # Retrieve existing config
        config_data = self.test_configs[test_id]
        dialog = TestConfigDialog(test_id, test_name, config_data, parent=self)
        dialog.exec()
        self.status_bar.showMessage(f"Config updated for {test_name}", 4000)

    @Slot()
    def add_new_test_demo(self):
        # This is just a placeholder to show how you might dynamically add tests
        new_test = {"id": f"test{len(self.tests)+1}", "name": f"Automated WLAN Test #{len(self.tests)+1}"}
        self.tests.append(new_test)
        self.test_configs[new_test["id"]] = {"username": "", "password": "", "eap_type": "PEAP"}
        self.refresh_table()
        self.status_bar.showMessage(f"New test added: {new_test['name']}", 3000)

# ─────────────────────────────────────────────────────────────────
# 4. Application Flow
# ─────────────────────────────────────────────────────────────────
class AutomatedTestManagerApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_dialog = LoginDialog()
        self.main_window = None

        # Connect signals
        self.login_dialog.login_success.connect(self.on_login_success)

    def run(self):
        self.login_dialog.exec()

        # If login was successful -> main window is created
        if self.main_window:
            sys.exit(self.app.exec())
        else:
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
        if self.main_window:
            self.main_window.close()
            self.main_window = None

        # Reset login fields
        self.login_dialog.username_edit.clear()
        self.login_dialog.password_edit.clear()
        # Show login dialog again
        self.login_dialog.exec()

# ─────────────────────────────────────────────────────────────────
# 5. Main Entry Point
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app_flow = AutomatedTestManagerApp()
    app_flow.run()
