import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

def create_login_window(app):
    """
    Creates and returns a Window for logging in.
    This window is not a subclass of Window but a plain toga.Window instance.
    """

    # UI elements
    username_input = toga.TextInput(placeholder="Username", style=Pack(width=200))
    password_input = toga.PasswordInput(placeholder="Password", style=Pack(width=200))
    message_label = toga.Label("", style=Pack(color="red", padding_bottom=5))
    
    def login_click(widget):
        username = username_input.value.strip()
        password = password_input.value.strip()
        if username and password:
            # Save user data in app state
            app.user_data["username"] = username
            app.user_data["logged_in"] = True
            # Close login window
            login_window.close()
            # Open the main window
            app.open_main_window()
        else:
            message_label.text = "Username/Password cannot be empty!"

    # Layout
    box = toga.Box(style=Pack(direction=COLUMN, padding=10, alignment="center"))
    box.add(toga.Label("Welcome! Please log in.", style=Pack(font_size=16, font_weight="bold", padding_bottom=10)))
    box.add(message_label)
    box.add(username_input)
    box.add(password_input)
    box.add(toga.Button("Login", on_press=login_click, style=Pack(padding_top=10)))

    # Create the login window
    login_window = toga.Window(title="Login", size=(320, 220))
    login_window.content = box

    return login_window


def create_main_window(app):
    """
    Creates and returns a Window that displays the test list and logout button.
    """
    welcome_label = toga.Label(
        text=f"Hello, {app.user_data['username']}!",
        style=Pack(font_size=14, font_weight="bold", padding_bottom=10)
    )
    instructions_label = toga.Label("Select a test to configure and run:", style=Pack(padding_bottom=5))

    tests_box = toga.Box(style=Pack(direction=COLUMN))
    # Build test buttons
    for t in app.tests:
        def on_test_click(widget, test_id=t["id"], test_name=t["name"]):
            # Create and show the test config window
            config_win = create_test_config_window(app, test_id, test_name)
            config_win.show()

        btn = toga.Button(t["name"], on_press=on_test_click, style=Pack(width=250, padding=(5, 0)))
        tests_box.add(btn)

    def logout_click(widget):
        # Close the main window
        main_window.close()
        app.user_data["logged_in"] = False
        app.user_data["username"] = ""
        # Re-open login window
        app.open_login_window()

    logout_btn = toga.Button("Logout", on_press=logout_click, style=Pack(padding_top=10, width=100))

    # Layout
    box = toga.Box(style=Pack(direction=COLUMN, padding=10))
    box.add(welcome_label)
    box.add(instructions_label)
    box.add(tests_box)
    box.add(logout_btn)

    # Create main window
    main_window = toga.Window(title="Automated Test Manager", size=(500, 400))
    main_window.content = box

    return main_window


def create_test_config_window(app, test_id, test_name):
    """
    Creates and returns a Window for configuring an individual test.
    """
    config = app.test_configs[test_id]

    username_input = toga.TextInput(value=config["username"], style=Pack(width=250))
    password_input = toga.PasswordInput(value=config["password"], style=Pack(width=250))
    eap_select = toga.Selection(items=["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"], style=Pack(width=150))
    eap_select.value = config["eap_type"]

    def run_test(widget):
        # Save the config
        config["username"] = username_input.value.strip()
        config["password"] = password_input.value.strip()
        config["eap_type"] = eap_select.value

        # Simulate test run
        toga.Dialog(
            title="Running Test",
            message=f"Running {test_name} with EAP={config['eap_type']}..."
        ).show(test_config_window)

    def close_window(widget):
        test_config_window.close()

    # Layout
    box = toga.Box(style=Pack(direction=COLUMN, padding=10))
    box.add(toga.Label(test_name, style=Pack(font_size=16, font_weight="bold", padding_bottom=10)))

    box.add(toga.Label("Test Username:"))
    box.add(username_input)
    box.add(toga.Label("Test Password:"))
    box.add(password_input)
    box.add(toga.Label("EAP Type:"))
    box.add(eap_select)

    button_box = toga.Box(style=Pack(direction=ROW, padding_top=10))
    button_box.add(toga.Button("Run Test", on_press=run_test, style=Pack(padding_right=10)))
    button_box.add(toga.Button("Close", on_press=close_window))
    box.add(button_box)

    # Create the test config window
    test_config_window = toga.Window(title=f"Configure {test_name}", size=(400, 320))
    test_config_window.content = box

    return test_config_window


class AutomatedTestManager(toga.App):
    def startup(self):
        # Called when the app starts. We decide if we show the login or main window.
        self.user_data = {
            "logged_in": False,
            "username": "",
        }
        self.tests = [
            {"id": "test1", "name": "Automated WLAN Test #1"},
            {"id": "test2", "name": "Automated WLAN Test #2"},
        ]
        self.test_configs = {
            "test1": {"username": "", "password": "", "eap_type": "PEAP"},
            "test2": {"username": "", "password": "", "eap_type": "PEAP"},
        }

        self.open_login_window()

    def open_login_window(self):
        # Create a login window and show it
        self.login_window = create_login_window(self)
        self.login_window.show()

    def open_main_window(self):
        # Create the main window and show it
        self.main_window = create_main_window(self)
        self.main_window.show()
        # Optionally close the login window if it's still open
        if hasattr(self, "login_window") and self.login_window is not None:
            self.login_window.close()


def main():
    return AutomatedTestManager("AutomatedTestManager", "org.beeware.automated-tests")


if __name__ == "__main__":
    main().main_loop()
