import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty


class LoginScreen(Screen):
    """
    A simple login screen with text fields for username and password,
    and a button to proceed to the main screen.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.username_input = TextInput(
            hint_text="Username", multiline=False, font_size=18
        )
        self.password_input = TextInput(
            hint_text="Password", multiline=False, password=True, font_size=18
        )

        login_button = Button(text="Log In", font_size=18, size_hint=(1, 0.4))
        login_button.bind(on_press=self.validate_credentials)

        layout.add_widget(Label(text="Welcome! Please log in:", font_size=22))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def validate_credentials(self, instance):
        # For simplicity, let's accept any non-empty username/password
        if self.username_input.text and self.password_input.text:
            # Switch to main screen
            self.manager.current = "main"
        else:
            self.manager.get_screen("error").error_message = (
                "Username or password cannot be empty!"
            )
            self.manager.current = "error"


class ErrorScreen(Screen):
    """
    Displays an error message if login fails.
    """
    # Using a StringProperty lets us dynamically update the text on the label
    error_message = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.label = Label(text=self.error_message, font_size=18)
        go_back_button = Button(text="Go Back", font_size=18, size_hint=(1, 0.4))

        go_back_button.bind(on_press=self.go_back)

        layout.add_widget(self.label)
        layout.add_widget(go_back_button)

        self.add_widget(layout)

    def on_error_message(self, instance, value):
        # Update the label text whenever error_message changes
        self.label.text = value

    def go_back(self, instance):
        self.manager.current = "login"


class MainScreen(Screen):
    """
    The main screen shown after successful login.
    Allows the user to add items to a list.
    """
    # Keep a dynamic list of items
    items = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Root layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.info_label = Label(text="Add items below:", font_size=20)
        layout.add_widget(self.info_label)

        # Sub-layout for text input + 'Add' button
        input_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        self.item_input = TextInput(hint_text="Enter item", multiline=False, font_size=18)
        add_button = Button(text="Add", font_size=18, size_hint=(0.3, 1))

        add_button.bind(on_press=self.add_item)
        input_layout.add_widget(self.item_input)
        input_layout.add_widget(add_button)

        layout.add_widget(input_layout)

        # This label will display the list of items
        self.items_label = Label(text="", font_size=16)
        layout.add_widget(self.items_label)

        # Logout button
        logout_button = Button(text="Log Out", font_size=18, size_hint=(1, 0.3))
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def add_item(self, instance):
        text = self.item_input.text.strip()
        if text:
            self.items.append(text)
            self.item_input.text = ""
            self.update_items_label()

    def update_items_label(self):
        # Join all items in a single string for display
        self.items_label.text = "Items:\n" + "\n".join(self.items)

    def logout(self, instance):
        self.manager.current = "login"

    def on_pre_enter(self, *args):
        """
        Called every time the screen is about to be displayed.
        Reset or update anything here if needed.
        """
        self.update_items_label()


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen(name="login"))
        self.add_widget(ErrorScreen(name="error"))
        self.add_widget(MainScreen(name="main"))


class MultiScreenApp(App):
    def build(self):
        # Create the screen manager, which holds all screens
        self.title = "Kivy Multi-Screen Example"
        return MyScreenManager()


if __name__ == "__main__":
    MultiScreenApp().run()
