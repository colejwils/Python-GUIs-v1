import flet as ft

def main(page: ft.Page):
    # PAGE CONFIG
    page.title = "Automated Test Manager"
    page.window_width = 500
    page.window_height = 600

    # DEFINE LIGHT THEME
    light_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#00ADEF",    # Forescout teal
            on_primary="white",
            secondary="#00ADEF",  # Also teal
            on_secondary="white",
            background="white",
            on_background="black",
            surface="white",
            on_surface="black",
        )
    )

    # DEFINE DARK THEME
    dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#00ADEF",
            on_primary="white",
            secondary="#00ADEF",
            on_secondary="white",
            background="black",
            on_background="white",
            surface="black",
            on_surface="white",
        )
    )

    # INITIAL THEME MODE AND THEMES
    page.theme_mode = ft.ThemeMode.LIGHT   # Default to light
    page.theme = light_theme
    page.dark_theme = dark_theme
    page.bgcolor = "white"  # Overridden in dark mode if user toggles

    # IN-MEMORY STATE
    user_data = {
        "logged_in": False,
        "username": "",
    }

    # A SIMPLE LIST OF TESTS
    tests = [
        {"id": "test1", "name": "Automated WLAN Test #1"},
        {"id": "test2", "name": "Automated WLAN Test #2"},
        {"id": "test3", "name": "IPv4 Regression Testing"},
        {"id": "test4", "name": "IPv6 Regression Testing"},
    ]

    # PER-TEST CONFIG (INITIAL DEFAULTS)
    test_configs = {
        "test1": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "server_ip": "10.0.0.1",
            "port": "1812",
            "timeout": "30",
            "certificate_file": None,  # will store path to cert if EAP-TLS
        },
        "test2": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "server_ip": "10.0.0.2",
            "port": "1812",
            "timeout": "30",
            "certificate_file": None,
        },
        "test3": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "server_ip": "192.168.1.100",
            "port": "1812",
            "timeout": "60",
            "certificate_file": None,
        },
        "test4": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "server_ip": "fd12:3456::1",
            "port": "1812",
            "timeout": "60",
            "certificate_file": None,
        },
    }

    eap_options = ["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"]

    # ─────────────────────────────────────────────────────────
    # ROUTE HANDLER
    # ─────────────────────────────────────────────────────────
    def route_change(event: ft.RouteChangeEvent):
        route = event.route
        page.views.clear()

        if route == "/":
            # LOGIN
            page.views.append(build_login_view())
        elif route == "/main":
            # MAIN TESTS VIEW
            if user_data["logged_in"]:
                page.views.append(build_tests_view())
            else:
                page.go("/")
        elif route.startswith("/test/"):
            # TEST CONFIG VIEW
            test_id = route.replace("/test/", "")
            if test_id in test_configs and user_data["logged_in"]:
                page.views.append(build_test_config_view(test_id))
            else:
                page.go("/main")
        elif route == "/settings":
            # SETTINGS VIEW
            if user_data["logged_in"]:
                page.views.append(build_settings_view())
            else:
                page.go("/")
        else:
            # 404 / unknown route
            page.views.append(
                ft.View(
                    "/404",
                    [
                        ft.Text("Page not found!", size=24),
                        ft.ElevatedButton(
                            "Go to Login",
                            on_click=lambda e: page.go("/"),
                            color="white",
                            bgcolor="#00ADEF"
                        )
                    ]
                )
            )
        page.update()

    page.on_route_change = route_change

    # ─────────────────────────────────────────────────────────
    # 1. LOGIN VIEW
    # ─────────────────────────────────────────────────────────
    def build_login_view():
        username_tf = ft.TextField(label="Username", width=300)
        password_tf = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300
        )

        def login_click(e):
            if username_tf.value.strip() and password_tf.value.strip():
                user_data["username"] = username_tf.value.strip()
                user_data["logged_in"] = True
                page.go("/main")
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please enter username and password!", color="white"),
                    bgcolor="#F36F21",  # Orange for error
                )
                page.snack_bar.open = True
                page.update()

        return ft.View(
            "/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Welcome! Please log in.", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, color="transparent"),
                username_tf,
                password_tf,
                ft.Divider(height=10, color="transparent"),
                ft.ElevatedButton(
                    "Login",
                    width=300,
                    on_click=login_click,
                    color="white",
                    bgcolor="#00ADEF",
                ),
            ],
        )

    # ─────────────────────────────────────────────────────────
    # 2. MAIN TESTS VIEW
    # ─────────────────────────────────────────────────────────
    def build_tests_view():
        # Insert the Forescout logo from their public site
        forescout_logo = ft.Image(
            src='https://images.store.crowdstrike.com/9748z14dd5zg/60SGqWYDWlrWJFsuQEZRV2/880c0144353da3a3904a84a98ee6731a/Forescout_icon_square.png',
            width=120,
            fit=ft.ImageFit.CONTAIN
        )

        welcome_text = ft.Text(
            f"Hello, {user_data['username']}!",
            size=22,
            weight=ft.FontWeight.W_600,
        )
        instructions = ft.Text("Select a test to configure and run.", size=16)

        test_buttons = []
        for t in tests:
            test_buttons.append(
                ft.ElevatedButton(
                    t["name"],
                    width=300,
                    on_click=lambda e, tid=t["id"]: page.go(f"/test/{tid}"),
                    color="white",
                    bgcolor="#00ADEF",
                )
            )

        def logout_click(e):
            user_data["logged_in"] = False
            user_data["username"] = ""
            page.go("/")

        def settings_click(e):
            page.go("/settings")

        # Create a Row at the top with the logo + welcome text on the left,
        # and "Settings" & "Logout" on the right
        top_bar = ft.Row(
            [
                ft.Row(
                    [
                        forescout_logo,
                        ft.VerticalDivider(width=10, color="transparent"),
                        welcome_text
                    ],
                    spacing=0,
                ),
                ft.Row(
                    [
                        ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=settings_click),
                        ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=logout_click),
                    ],
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ft.View(
            "/main",
            [
                top_bar,
                ft.Divider(),
                instructions,
                ft.Column(test_buttons, spacing=10),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ─────────────────────────────────────────────────────────
    # 3. TEST CONFIG VIEW
    # ─────────────────────────────────────────────────────────

    def build_test_config_view(test_id: str):
        """Displays test-specific configuration fields, including EAP settings
        and additional parameters such as server IP, port, and timeout. Shows
        a file-chooser button if EAP-TLS is selected."""
        config = test_configs[test_id]
        test_title = next((t["name"] for t in tests if t["id"] == test_id), "Unknown Test")

        # TEXT FIELDS
        test_username_tf = ft.TextField(
            label="Test Username",
            width=300,
            value=config["username"]
        )
        test_password_tf = ft.TextField(
            label="Test Password",
            password=True,
            can_reveal_password=True,
            width=300,
            value=config["password"],
        )
        server_ip_tf = ft.TextField(
            label="Server IP/Hostname",
            width=300,
            value=config["server_ip"],
        )
        port_tf = ft.TextField(
            label="Port",
            width=300,
            value=config["port"],
        )
        timeout_tf = ft.TextField(
            label="Timeout (seconds)",
            width=300,
            value=config["timeout"],
        )

        # EAP TYPE DROPDOWN
        eap_dropdown = ft.Dropdown(
            label="EAP Type",
            options=[ft.dropdown.Option(e) for e in eap_options],
            value=config["eap_type"],
            width=300,
            on_change=lambda e: update_cert_ui_visibility()
        )

        # FILE PICKER + UI elements to handle EAP-TLS
        certificate_picker = ft.FilePicker(
            on_result=lambda e: handle_cert_selected(e)
        )
        page.overlay.append(certificate_picker)  # Make sure it's in the page overlay

        cert_label = ft.Text(
            value=("Selected cert: " + config["certificate_file"]) if config["certificate_file"] else "No certificate selected",
            size=14,
        )

        def select_certificate(e):
            # Open the file picker
            # (If you only want to allow certain extensions, you can specify e.g. `file_picker.accept=[".pem",".p12"]`)
            certificate_picker.pick_files(
                allow_multiple=False,
                dialog_title="Select Certificate File"
            )

        def handle_cert_selected(e: ft.FilePickerResultEvent):
            """Called after user picks a file."""
            if e.files and len(e.files) > 0:
                chosen_file = e.files[0].path
                config["certificate_file"] = chosen_file
                cert_label.value = f"Selected cert: {chosen_file}"
            else:
                config["certificate_file"] = None
                cert_label.value = "No certificate selected"
            page.update()

        # Container for certificate selection UI
        select_cert_button = ft.ElevatedButton(
            "Select Certificate",
            color="white",
            bgcolor="#00ADEF",
            on_click=select_certificate
        )

        cert_container = ft.Column(
            [
                ft.Divider(height=5, color="transparent"),
                select_cert_button,
                cert_label,
            ],
            visible=(config["eap_type"] == "EAP-TLS")  # Visible if EAP-TLS
        )

        def update_cert_ui_visibility():
            """Show/hide certificate UI if eap_dropdown changes to EAP-TLS or not."""
            if eap_dropdown.value == "EAP-TLS":
                cert_container.visible = True
            else:
                cert_container.visible = False
            page.update()

        def save_and_run_test(e):
            # Update config from text fields
            config["username"] = test_username_tf.value.strip()
            config["password"] = test_password_tf.value.strip()
            config["eap_type"] = eap_dropdown.value
            config["server_ip"] = server_ip_tf.value.strip()
            config["port"] = port_tf.value.strip()
            config["timeout"] = timeout_tf.value.strip()

            # Show a snack bar to confirm
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    f"Running {test_title} with EAP={config['eap_type']}... (Cert: {config['certificate_file']})",
                    color="white"
                ),
                bgcolor="#00ADEF",
            )
            page.snack_bar.open = True
            page.update()

        def go_back(e):
            page.go("/main")

        # Build the test config view
        return ft.View(
            f"/test/{test_id}",
            [
                ft.Row(
                    [
                        ft.Text(test_title, size=24, weight=ft.FontWeight.W_600),
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Please configure the test details below:", size=16),

                test_username_tf,
                test_password_tf,
                eap_dropdown,
                server_ip_tf,
                port_tf,
                timeout_tf,

                # Certificate UI (conditionally shown if EAP-TLS)
                cert_container,

                ft.ElevatedButton(
                    "Run Test",
                    on_click=save_and_run_test,
                    color="white",
                    bgcolor="#00ADEF",
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

    # ─────────────────────────────────────────────────────────
    # 4. SETTINGS VIEW (FOR LIGHT/DARK TOGGLE)
    # ─────────────────────────────────────────────────────────
    def build_settings_view():
        dark_mode_switch = ft.Switch(
            label="Enable Dark Mode",
            value=(page.theme_mode == ft.ThemeMode.DARK),
            on_change=toggle_dark_mode
        )

        def go_back(e):
            page.go("/main")

        return ft.View(
            "/settings",
            [
                ft.Row(
                    [
                        ft.Text("Settings", size=24, weight=ft.FontWeight.W_600),
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text("Theme Options"),
                        dark_mode_switch,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def toggle_dark_mode(e: ft.ControlEvent):
        if e.control.value:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "black"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "white"
        page.update()

    # INITIALIZE
    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
