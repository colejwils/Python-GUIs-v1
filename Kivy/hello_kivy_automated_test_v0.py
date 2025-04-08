import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

kivy.require('2.1.0')  # Adjust if needed

# ─────────────────────────────────────────────────────────
# 1. LoginScreen
# ─────────────────────────────────────────────────────────
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Welcome! Please log in.", font_size=24))

        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True)
        login_button = Button(text="Login", size_hint=(1, 0.4))
        login_button.bind(on_press=self.login)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        if username and password:
            # Save user data in the App
            app = App.get_running_app()
            app.user_data["username"] = username
            app.user_data["logged_in"] = True
            self.manager.current = "main"
        else:
            popup = Popup(title="Login Failed",
                          content=Label(text="Username/Password cannot be empty!"),
                          size_hint=(0.6, 0.4))
            popup.open()


# ─────────────────────────────────────────────────────────
# 2. MainScreen
# ─────────────────────────────────────────────────────────
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.welcome_label = Label(text="", font_size=20)
        layout.add_widget(self.welcome_label)

        layout.add_widget(Label(text="Select a test to configure and run:"))

        # A layout to list test buttons
        self.test_buttons_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, None))
        layout.add_widget(self.test_buttons_layout)

        logout_button = Button(text="Logout", size_hint=(1, 0.3))
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        """
        Called before the screen is displayed.
        Update the welcome label and build the test buttons if needed.
        """
        app = App.get_running_app()
        username = app.user_data["username"]
        self.welcome_label.text = f"Hello, {username}!"

        # Clear previous buttons if any, then create new ones
        self.test_buttons_layout.clear_widgets()

        for t in App.get_running_app().tests:
            btn = Button(text=t["name"], size_hint=(1, None), height=40)
            # We store the test_id in a closure
            btn.bind(on_press=lambda instance, test_id=t["id"]: self.open_test_config(test_id))
            self.test_buttons_layout.add_widget(btn)

        # Adjust container height to fit all buttons (simple approach)
        self.test_buttons_layout.height = 45 * len(App.get_running_app().tests)

    def open_test_config(self, test_id):
        """
        Switch to TestConfigScreen, telling it which test we selected.
        """
        app = App.get_running_app()
        app.selected_test_id = test_id  # store it in app state
        self.manager.current = "test_config"

    def logout(self, instance):
        app = App.get_running_app()
        app.user_data["logged_in"] = False
        app.user_data["username"] = ""
        self.manager.current = "login"


# ─────────────────────────────────────────────────────────
# 3. TestConfigScreen
# ─────────────────────────────────────────────────────────
class TestConfigScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title_label = Label(text="Configure Test", font_size=20)
        layout.add_widget(self.title_label)

        # Test username
        self.username_input = TextInput(hint_text="Test Username", multiline=False)
        layout.add_widget(self.username_input)

        # Test password
        self.password_input = TextInput(hint_text="Test Password", multiline=False, password=True)
        layout.add_widget(self.password_input)

        # EAP Type (Spinner for selection)
        self.eap_spinner = Spinner(text="PEAP", values=["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"])
        layout.add_widget(self.eap_spinner)

        # Button to run test
        run_button = Button(text="Run Test", size_hint=(1, 0.3))
        run_button.bind(on_press=self.run_test)
        layout.add_widget(run_button)

        # Back button
        back_button = Button(text="Back to Main", size_hint=(1, 0.3))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        """
        Called when we navigate to this screen.
        Load the test config data from the app state.
        """
        app = App.get_running_app()
        test_id = app.selected_test_id
        # Find the test name
        test_name = next((t["name"] for t in app.tests if t["id"] == test_id), "Unknown Test")
        self.title_label.text = f"Configure {test_name}"

        # Load existing config
        config = app.test_configs[test_id]
        self.username_input.text = config["username"]
        self.password_input.text = config["password"]
        self.eap_spinner.text = config["eap_type"]

    def run_test(self, instance):
        """
        Save the config, then show a popup indicating test is running.
        """
        app = App.get_running_app()
        test_id = app.selected_test_id
        config = app.test_configs[test_id]

        config["username"] = self.username_input.text.strip()
        config["password"] = self.password_input.text.strip()
        config["eap_type"] = self.eap_spinner.text

        popup = Popup(title="Running Test",
                      content=Label(text=f"Running test: {test_id}\nEAP={config['eap_type']}..."),
                      size_hint=(0.7, 0.5))
        popup.open()
        # Real test logic goes here...

    def go_back(self, instance):
        self.manager.current = "main"


# ─────────────────────────────────────────────────────────
# 4. ScreenManager
# ─────────────────────────────────────────────────────────
class MyScreenManager(ScreenManager):
    pass


# ─────────────────────────────────────────────────────────
# 5. The Kivy App
# ─────────────────────────────────────────────────────────
class AutomatedTestApp(App):
    def build(self):
        # Global app state
        self.user_data = {
            "logged_in": False,
            "username": "",
        }

        # Example tests
        self.tests = [
            {"id": "test1", "name": "Automated WLAN Test #1"},
            {"id": "test2", "name": "Automated WLAN Test #2"},
        ]

        # Per-test config data
        self.test_configs = {
            "test1": {"username": "", "password": "", "eap_type": "PEAP"},
            "test2": {"username": "", "password": "", "eap_type": "PEAP"},
        }

        # We’ll store the currently selected test ID here
        self.selected_test_id = None

        sm = MyScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(TestConfigScreen(name="test_config"))

        # Start at login screen
        sm.current = "login"
        return sm


if __name__ == "__main__":
    AutomatedTestApp().run()
