import flet as ft

def main(page: ft.Page):
    # Page configuration
    page.title = "Automated Test Manager"
    page.window_width = 500
    page.window_height = 600
    
    # ─────────────────────────────────────────────────────────
    # In-memory “state”
    # ─────────────────────────────────────────────────────────
    user_data = {
        "logged_in": False,
        "username": "",
    }

    # A simple list of tests we want to display
    tests = [
        {"id": "test1", "name": "Automated WLAN Test #1"},
        {"id": "test2", "name": "Automated WLAN Test #2"},
    ]

    # Per-test configuration data
    test_configs = {
        "test1": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",  # default
        },
        "test2": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
        },
    }

    eap_options = ["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"]

    # ─────────────────────────────────────────────────────────
    # ROUTE HANDLER
    # ─────────────────────────────────────────────────────────
    def route_change(event: ft.RouteChangeEvent):
        # event.route is the actual route string, e.g. "/main", "/test/test1"
        route = event.route
        page.views.clear()

        if route == "/":
            # Show login view
            page.views.append(build_login_view())
        elif route == "/main":
            # Show main "Tests" list after logging in
            if user_data["logged_in"]:
                page.views.append(build_tests_view())
            else:
                # If not logged in, redirect to "/"
                page.go("/")
        elif route.startswith("/test/"):
            # Something like "/test/test1" or "/test/test2"
            test_id = route.replace("/test/", "")
            if test_id in test_configs and user_data["logged_in"]:
                page.views.append(build_test_config_view(test_id))
            else:
                page.go("/main")
        else:
            # 404 / unknown route
            page.views.append(
                ft.View(
                    "/404",
                    [
                        ft.Text("Page not found!", size=24),
                        ft.ElevatedButton("Go to Login", on_click=lambda e: page.go("/"))
                    ]
                )
            )
        page.update()

    page.on_route_change = route_change

    # ─────────────────────────────────────────────────────────
    # 1. BUILD LOGIN VIEW
    # ─────────────────────────────────────────────────────────
    def build_login_view():
        username_tf = ft.TextField(label="Username", width=300)
        password_tf = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

        def login_click(e):
            if username_tf.value.strip() and password_tf.value.strip():
                user_data["username"] = username_tf.value.strip()
                user_data["logged_in"] = True
                page.go("/main")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Please enter username and password!"))
                page.snack_bar.open = True
                page.update()

        return ft.View(
            "/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Welcome! Please log in.", size=24, weight=ft.FontWeight.BOLD),
                username_tf,
                password_tf,
                ft.ElevatedButton("Login", on_click=login_click),
            ],
        )

    # ─────────────────────────────────────────────────────────
    # 2. BUILD MAIN "TESTS" VIEW
    # ─────────────────────────────────────────────────────────
    def build_tests_view():
        welcome_text = ft.Text(
            f"Hello, {user_data['username']}!",
            size=22,
            weight=ft.FontWeight.W_600
        )
        instructions = ft.Text("Select a test to configure and run.", size=16)

        test_buttons = []
        for t in tests:
            test_buttons.append(
                ft.ElevatedButton(
                    t["name"],
                    on_click=lambda e, tid=t["id"]: page.go(f"/test/{tid}"),
                    width=300
                )
            )

        def logout_click(e):
            user_data["logged_in"] = False
            user_data["username"] = ""
            page.go("/")
        
        return ft.View(
            "/main",
            [
                ft.Row(
                    [
                        welcome_text,
                        ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=logout_click),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                instructions,
                ft.Column(test_buttons, spacing=10),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ─────────────────────────────────────────────────────────
    # 3. BUILD TEST CONFIG VIEW
    # ─────────────────────────────────────────────────────────
    def build_test_config_view(test_id: str):
        config = test_configs[test_id]
        test_title = next((t["name"] for t in tests if t["id"] == test_id), "Unknown Test")

        test_username_tf = ft.TextField(label="Test Username", width=300, value=config["username"])
        test_password_tf = ft.TextField(label="Test Password", password=True, can_reveal_password=True, width=300, value=config["password"])
        eap_dropdown = ft.Dropdown(
            label="EAP Type",
            options=[ft.dropdown.Option(e) for e in eap_options],
            value=config["eap_type"],
            width=300,
        )

        def save_and_run_test(e):
            config["username"] = test_username_tf.value.strip()
            config["password"] = test_password_tf.value.strip()
            config["eap_type"] = eap_dropdown.value

            page.snack_bar = ft.SnackBar(
                ft.Text(f"Running {test_title} with EAP={config['eap_type']}...")
            )
            page.snack_bar.open = True
            page.update()
            # Here you could call a real function to run the test, etc.

        def go_back(e):
            page.go("/main")

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
                ft.ElevatedButton("Run Test", on_click=save_and_run_test),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

    # ─────────────────────────────────────────────────────────
    # Initialize by going to the login route
    # ─────────────────────────────────────────────────────────
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
