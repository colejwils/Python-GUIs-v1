import dearpygui.dearpygui as dpg

# Global application state
app_data = {
    "logged_in": False,
    "username": "",
    "tests": [
        {"id": "test1", "name": "Automated WLAN Test #1"},
        {"id": "test2", "name": "Automated WLAN Test #2"},
    ],
    # Per-test configs
    "test_configs": {
        "test1": {"username": "", "password": "", "eap_type": "PEAP"},
        "test2": {"username": "", "password": "", "eap_type": "PEAP"},
    },
    # Track the currently open test
    "selected_test_id": None,
}

# Unique DearPyGui item tags
TAG_LOGIN_WINDOW = "LoginWindow"
TAG_MAIN_WINDOW = "MainWindow"
TAG_CONFIG_WINDOW = "ConfigWindow"

# Input tags for login fields
TAG_LOGIN_USERNAME = "LoginUsername"
TAG_LOGIN_PASSWORD = "LoginPassword"

# Input tags for test config fields
TAG_CONFIG_USERNAME = "ConfigUsername"
TAG_CONFIG_PASSWORD = "ConfigPassword"
TAG_CONFIG_EAP = "ConfigEAP"

###############################################################################
# Callbacks
###############################################################################
def login_callback(sender, app_data_callback):
    username = dpg.get_value(TAG_LOGIN_USERNAME).strip()
    password = dpg.get_value(TAG_LOGIN_PASSWORD).strip()

    if username and password:
        app_data["username"] = username
        app_data["logged_in"] = True
        # Hide the login window, show the main window
        dpg.configure_item(TAG_LOGIN_WINDOW, show=False)
        dpg.configure_item(TAG_MAIN_WINDOW, show=True)
    else:
        print("Login failed: username/password cannot be empty.")


def logout_callback(sender, app_data_callback):
    """Log out and return to the login window."""
    app_data["logged_in"] = False
    app_data["username"] = ""
    # Clear the login fields
    dpg.set_value(TAG_LOGIN_USERNAME, "")
    dpg.set_value(TAG_LOGIN_PASSWORD, "")
    # Hide main window, show login window
    dpg.configure_item(TAG_MAIN_WINDOW, show=False)
    dpg.configure_item(TAG_LOGIN_WINDOW, show=True)


def open_test_config_callback(sender, test_id):
    """Open the test config window for a specific test."""
    app_data["selected_test_id"] = test_id
    if test_id not in app_data["test_configs"]:
        print(f"Error: test_configs does not contain key '{test_id}'!")
        return

    config = app_data["test_configs"][test_id]
    # Populate fields
    dpg.set_value(TAG_CONFIG_USERNAME, config["username"])
    dpg.set_value(TAG_CONFIG_PASSWORD, config["password"])
    dpg.set_value(TAG_CONFIG_EAP, config["eap_type"])

    # Update window label with the test name
    test_name = next((t["name"] for t in app_data["tests"] if t["id"] == test_id), "Unknown Test")
    dpg.configure_item(TAG_CONFIG_WINDOW, label=f"Configure: {test_name}")

    # Show config window
    dpg.configure_item(TAG_CONFIG_WINDOW, show=True)


def run_test_callback(sender, app_data_callback):
    """Save config fields and 'run' the test."""
    test_id = app_data["selected_test_id"]
    if not test_id:
        return

    config = app_data["test_configs"][test_id]
    config["username"] = dpg.get_value(TAG_CONFIG_USERNAME).strip()
    config["password"] = dpg.get_value(TAG_CONFIG_PASSWORD).strip()
    config["eap_type"] = dpg.get_value(TAG_CONFIG_EAP)

    # Simulate running the test
    print(f"Running {test_id} with EAP={config['eap_type']}...")

def close_test_config_callback(sender, app_data_callback):
    """Close the test config window."""
    dpg.configure_item(TAG_CONFIG_WINDOW, show=False)


###############################################################################
# Build the UI
###############################################################################
def build_ui():
    # 1. Login Window
    with dpg.window(label="Login", tag=TAG_LOGIN_WINDOW, width=300, height=200, pos=(100, 100), show=True):
        dpg.add_text("Welcome! Please log in.")
        dpg.add_input_text(label="Username", tag=TAG_LOGIN_USERNAME)
        dpg.add_input_text(label="Password", tag=TAG_LOGIN_PASSWORD, password=True)
        dpg.add_button(label="Login", callback=login_callback)

    # 2. Main Window (initially hidden)
    with dpg.window(label="Automated Test Manager", tag=TAG_MAIN_WINDOW, width=400, height=300, pos=(150, 150), show=False):
        dpg.add_text(lambda: f"Hello, {app_data['username']}!", bullet=False)
        dpg.add_separator()
        dpg.add_text("Select a test to configure and run:")

        # Create a button for each test
        for t in app_data["tests"]:
            dpg.add_button(
                label=t["name"],
                callback=lambda s,a,u=t["id"]: open_test_config_callback(s,u)
            )

        dpg.add_separator()
        dpg.add_button(label="Logout", callback=logout_callback)

    # 3. Test Config Window (hidden by default)
    with dpg.window(label="Configure Test", tag=TAG_CONFIG_WINDOW, width=350, height=250, pos=(200, 200), show=False):
        dpg.add_text("Test Username:")
        dpg.add_input_text(tag=TAG_CONFIG_USERNAME)

        dpg.add_text("Test Password:")
        dpg.add_input_text(tag=TAG_CONFIG_PASSWORD, password=True)

        dpg.add_text("EAP Type:")
        dpg.add_combo(["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"], tag=TAG_CONFIG_EAP, default_value="PEAP")

        dpg.add_separator()
        # Instead of add_same_line(), use a horizontal group:
        with dpg.group(horizontal=True):
            dpg.add_button(label="Run Test", callback=run_test_callback)
            dpg.add_button(label="Close", callback=close_test_config_callback)


def main():
    dpg.create_context()
    dpg.create_viewport(title="Dear PyGui - Automated Tests", width=600, height=400)
    build_ui()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
