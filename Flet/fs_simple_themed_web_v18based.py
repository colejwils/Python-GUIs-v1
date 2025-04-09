import flet as ft
import plotly.express as px
import flet.plotly_chart as fpc
import paramiko

# ---------------------- SSH TEST AREA ----------------------
def test_ssh_connection(hostname, ip_address, port, username, password=None, key=None):
    """
    Attempts to SSH to the given host using Paramiko.
    Returns (success, message) to indicate pass/fail and the reason.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # If a key path is provided, try key-based auth:
        if key and len(key.strip()) > 0:
            private_key = paramiko.RSAKey.from_private_key_file(key)
            client.connect(
                hostname=hostname,
                port=port,
                username=username,
                pkey=private_key,
                timeout=10
            )
        else:
            # Otherwise, user/password
            client.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                timeout=10
            )

        msg = f"SSH connection to {hostname} ({ip_address}) on port {port} successful!"
        print(msg)  # Console log
        return (True, msg)

    except paramiko.AuthenticationException:
        msg = f"Failed to authenticate to {hostname} ({ip_address}) on port {port}. Invalid credentials."
        print(msg)
        return (False, msg)
    except paramiko.SSHException as e:
        msg = f"SSH connection to {hostname} ({ip_address}) on port {port} failed: {str(e)}"
        print(msg)
        return (False, msg)
    except Exception as e:
        msg = f"An error occurred while connecting to {hostname} ({ip_address}) on port {port}: {str(e)}"
        print(msg)
        return (False, msg)
    finally:
        client.close()


# ---------------------- PEAP TEST STUB ---------------------
def run_peap_test(username, password, server_ip, port, timeout, inner_method):
    """
    Placeholder function that "runs" a PEAP test.
    In a real app, you'd have logic to connect to the server
    or call an API to verify PEAP connectivity.
    """
    print("===== RUNNING PEAP TEST =====")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Server IP: {server_ip}")
    print(f"Port: {port}")
    print(f"Timeout: {timeout}s")
    print(f"Inner Method: {inner_method}")
    print("Test in progress... [Simulating PEAP handshake]")
    return True


def main(page: ft.Page):
    # PAGE CONFIG
    page.title = "RADIUS Simulation Engine - Upstart Cyber, LLC"
    page.window_width = 500
    page.window_height = 600

    # THEMES
    light_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#00ADEF", on_primary="white",
            secondary="#00ADEF", on_secondary="white",
            background="white", on_background="black",
            surface="white", on_surface="black",
        )
    )
    dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#00ADEF", on_primary="white",
            secondary="#00ADEF", on_secondary="white",
            background="black", on_background="white",
            surface="black", on_surface="white",
        )
    )
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = light_theme
    page.dark_theme = dark_theme
    page.bgcolor = "black"

    # IN-MEMORY STATE
    user_data = {"logged_in": False, "username": ""}
    settings_data = {"persistent_config": False}

    tests = [
        {"id": "test1", "name": "Automated WLAN Test"},
        {"id": "test2", "name": "Automated Wired Test"},
        {"id": "test3", "name": "IPv4 Regression Testing"},
        {"id": "test4", "name": "IPv6 Regression Testing"},
    ]

    test_configs = {
        "test1": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "inner_method": "MSCHAPv2",
            "anonymous_identity": "",
            "fast_provisioning": False,
            "server_ip": "10.0.0.1",
            "port": "1812",
            "timeout": "30",
            "certificate_file": None,
        },
        "test2": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "inner_method": "MSCHAPv2",
            "anonymous_identity": "",
            "fast_provisioning": False,
            "server_ip": "10.0.0.2",
            "port": "1812",
            "timeout": "30",
            "certificate_file": None,
        },
        "test3": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "inner_method": "MSCHAPv2",
            "anonymous_identity": "",
            "fast_provisioning": False,
            "server_ip": "192.168.1.100",
            "port": "1812",
            "timeout": "60",
            "certificate_file": None,
        },
        "test4": {
            "username": "",
            "password": "",
            "eap_type": "PEAP",
            "inner_method": "MSCHAPv2",
            "anonymous_identity": "",
            "fast_provisioning": False,
            "server_ip": "fd12:3456::1",
            "port": "1812",
            "timeout": "60",
            "certificate_file": None,
        },
    }

    eap_options = ["PEAP", "EAP-TLS", "EAP-TTLS", "EAP-FAST"]
    inner_methods_map = {
        "PEAP": ["MSCHAPv2", "GTC"],
        "EAP-TTLS": ["MSCHAPv2", "CHAP", "PAP"],
        "EAP-FAST": ["MSCHAPv2", "GTC"],
    }

    # SAMPLE CLIENTS / VMS / LINUX HOSTS
    clients = [
        {"client_name": "TestClient1", "mac_address": "AA:BB:CC:DD:EE:01", "ip_address": "192.168.10.101",
         "use_radsec": False, "certificate_file": None, "client_secret": ""},
        {"client_name": "TestClient2", "mac_address": "AA:BB:CC:DD:EE:02", "ip_address": "192.168.10.102",
         "use_radsec": True, "certificate_file": "/path/to/cert.pem", "client_secret": "supersecret"},
    ]

    vms = [
        {"vm_name": "UbuntuTestVM", "host": "192.168.50.10", "port": 22, "ssh_user": "testuser",
         "ssh_password": "secret", "ssh_key_file": None},
        {"vm_name": "CentOSVM", "host": "192.168.50.20", "port": 2222, "ssh_user": "root",
         "ssh_password": "", "ssh_key_file": "/home/user/.ssh/id_rsa"},
    ]

    linux_hosts = [
        {"host_name": "eve-qa-em-912", "ip_address": "10.110.1.75", "port": 22, "ssh_user": "root", "ssh_password": "Vlabs123$$$", "ssh_key_file": None},
        {"host_name": "eve-qa-app-912", "ip_address": "10.110.1.74", "port": 22, "ssh_user": "root", "ssh_password": "Vlabs123$$$", "ssh_key_file": None},
    ]

    diagnostics_data = {
        "UbuntuTestVM": {
            "cpu_percent": [20, 25, 23, 30],
            "memory_percent": [55, 57, 53, 60],
            "timestamps": [0, 1, 2, 3]
        },
        "CentOSVM": {
            "cpu_percent": [10, 12, 15, 14],
            "memory_percent": [70, 68, 72, 75],
            "timestamps": [0, 1, 2, 3]
        },
    }

    # -------------- STUB TEST FUNCTIONS --------------
    def test_client_config(idx: int):
        c = clients[idx]
        print("=== Testing Client Configuration ===")
        print(f"Name: {c['client_name']}")
        print("Simulating client connectivity...\n")

    def test_vm_config(idx: int):
        vm = vms[idx]
        print("=== Testing VM Configuration ===")
        print("Simulating VM connectivity...\n")

    def test_linux_host(idx: int):
        host = linux_hosts[idx]
        print("=== Testing Forescout Host ===")
        hostname = host["ip_address"]
        ip_address = host["ip_address"]
        port = host["port"]
        ssh_user = host["ssh_user"]
        ssh_password = host["ssh_password"]
        ssh_key_file = host["ssh_key_file"]

        success, message = test_ssh_connection(
            hostname, ip_address, port,
            ssh_user, password=ssh_password, key=ssh_key_file
        )
        return (success, message)

    # -------------- ROUTE HANDLER --------------
    def route_change(event: ft.RouteChangeEvent):
        route = event.route
        page.views.clear()

        if route == "/":
            page.views.append(build_login_view())
        elif route == "/main":
            if user_data["logged_in"]:
                page.views.append(build_tests_view())
            else:
                page.go("/")
        elif route.startswith("/test/"):
            test_id = route.replace("/test/", "")
            if test_id in test_configs and user_data["logged_in"]:
                page.views.append(build_test_config_view(test_id))
            else:
                page.go("/main")
        elif route == "/clients":
            if user_data["logged_in"]:
                page.views.append(build_clients_view())
            else:
                page.go("/")
        elif route == "/settings":
            if user_data["logged_in"]:
                page.views.append(build_settings_view())
            else:
                page.go("/")
        elif route == "/vms":
            if user_data["logged_in"]:
                page.views.append(build_vms_view())
            else:
                page.go("/")
        elif route == "/diagnostics":
            if user_data["logged_in"]:
                page.views.append(build_diagnostics_view())
            else:
                page.go("/")
        elif route == "/linux_hosts":
            if user_data["logged_in"]:
                page.views.append(build_linux_hosts_view())
            else:
                page.go("/")
        else:
            page.views.append(
                ft.View(
                    "/404",
                    [
                        ft.Text("Page not found!", size=24),
                        ft.ElevatedButton("Go to Login", on_click=lambda e: page.go("/"),
                                         color="white", bgcolor="#00ADEF")
                    ]
                )
            )
        page.update()

    page.on_route_change = route_change

    # -------------- 1. LOGIN VIEW --------------
    def build_login_view():
        username_tf = ft.TextField(label="Username", width=300)
        password_tf = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)

        def login_click(e):
            if username_tf.value.strip() and password_tf.value.strip():
                user_data["username"] = username_tf.value.strip()
                user_data["logged_in"] = True
                page.go("/main")
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please enter username and password!", color="white"),
                    bgcolor="#F36F21",
                    auto_hide=False,  # Keep it visible until user dismisses it
                    # Show a close icon
                    action="Close",
                    on_action=lambda _: close_snack()
                )
                page.snack_bar.open = True
                page.update()

        def close_snack():
            # When user clicks "Close" on the SnackBar:
            page.snack_bar.open = False
            page.update()

        return ft.View(
            "/",
            [
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
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # -------------- 2. MAIN TESTS VIEW --------------
    def build_tests_view():
        forescout_logo = ft.Image(
            src="https://images.store.crowdstrike.com/9748z14dd5zg/60SGqWYDWlrWJFsuQEZRV2/"
                "880c0144353da3a3904a84a98ee6731a/Forescout_icon_square.png",
            width=120, fit=ft.ImageFit.CONTAIN
        )
        welcome_text = ft.Text(f"Hello, {user_data['username']}!", size=22, weight=ft.FontWeight.W_600)
        instructions = ft.Text("Select a test to configure and run, or configure clients / VMs / Linux hosts / diagnostics.", size=16)

        test_buttons = [
            ft.ElevatedButton(
                t["name"], width=300, color="white", bgcolor="#00ADEF",
                on_click=lambda e, tid=t["id"]: page.go(f"/test/{tid}")
            ) for t in tests
        ]

        def logout_click(e):
            user_data["logged_in"] = False
            user_data["username"] = ""
            page.go("/")

        def settings_click(e):
            page.go("/settings")

        def clients_click(e):
            page.go("/clients")

        def vms_click(e):
            page.go("/vms")

        def diagnostics_click(e):
            page.go("/diagnostics")

        def linux_hosts_click(e):
            page.go("/linux_hosts")

        top_bar = ft.Row([
            ft.Row([forescout_logo, ft.VerticalDivider(width=10, color="transparent"), welcome_text], spacing=0),
            ft.Row([
                ft.IconButton(icon=ft.Icons.MONITOR_HEART, tooltip="Diagnostics", on_click=diagnostics_click),
                ft.IconButton(icon=ft.Icons.DEVICE_HUB, tooltip="Configure VMs", on_click=vms_click),
                ft.IconButton(icon=ft.Icons.ROUTER, tooltip="Configure Clients", on_click=clients_click),
                ft.IconButton(icon=ft.Icons.SECURITY, tooltip="Forescout Devices", on_click=linux_hosts_click),
                ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=settings_click),
                ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=logout_click),
            ], spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

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

    # -------------- 3. TEST CONFIG VIEW --------------
    def build_test_config_view(test_id: str):
        # (Same as previous code with EAP config, runs a snack bar, etc.)
        # We'll add auto_hide=False to keep snack bar visible
        config = test_configs[test_id]
        test_title = next((t["name"] for t in tests if t["id"] == test_id), "Unknown Test")

        test_username_tf = ft.TextField(label="Test Username", width=300, value=config["username"])
        test_password_tf = ft.TextField(label="Test Password", password=True, can_reveal_password=True, width=300,
                                        value=config["password"])
        server_ip_tf = ft.TextField(label="Server IP/Hostname", width=300, value=config["server_ip"])
        port_tf = ft.TextField(label="Port", width=300, value=config["port"])
        timeout_tf = ft.TextField(label="Timeout (seconds)", width=300, value=config["timeout"])

        eap_dropdown = ft.Dropdown(
            label="EAP Type",
            options=[ft.dropdown.Option(e) for e in eap_options],
            value=config["eap_type"],
            width=300
        )

        inner_method_dropdown = ft.Dropdown(label="Inner Method", width=300, value=config["inner_method"])
        anonymous_identity_tf = ft.TextField(label="Anonymous Identity (TTLS)", width=300,
                                             value=config["anonymous_identity"])
        fast_provision_switch = ft.Switch(label="Allow FAST Provisioning", value=config["fast_provisioning"])

        # FILE PICKER
        certificate_picker = ft.FilePicker()
        page.overlay.append(certificate_picker)

        cert_label = ft.Text(
            value=(f"Selected cert: {config['certificate_file']}" if config["certificate_file"] else "No certificate selected"),
            size=14
        )

        def select_certificate(e):
            certificate_picker.pick_files(allow_multiple=False, dialog_title="Select Certificate File")

        select_cert_button = ft.ElevatedButton("Select Certificate", color="white", bgcolor="#00ADEF",
                                               on_click=select_certificate)

        cert_container = ft.Column([
            ft.Divider(height=5, color="transparent"),
            select_cert_button,
            cert_label
        ], visible=(config["eap_type"] == "EAP-TLS"))

        def handle_cert_selected(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                chosen_file = e.files[0].path
                config["certificate_file"] = chosen_file
                cert_label.value = f"Selected cert: {chosen_file}"
            else:
                config["certificate_file"] = None
                cert_label.value = "No certificate selected"
            page.update()

        certificate_picker.on_result = handle_cert_selected

        inner_method_container = ft.Column(controls=[], visible=False)

        def update_eap_ui_visibility():
            current_eap = eap_dropdown.value
            cert_container.visible = (current_eap == "EAP-TLS")

            # Show/hide inner method stuff
            if current_eap in ["PEAP", "EAP-TTLS", "EAP-FAST"]:
                methods = inner_methods_map[current_eap]
                inner_method_dropdown.options = [ft.dropdown.Option(m) for m in methods]
                if config["inner_method"] not in methods:
                    config["inner_method"] = methods[0]
                    inner_method_dropdown.value = methods[0]
                else:
                    inner_method_dropdown.value = config["inner_method"]
                inner_method_container.visible = True
                anonymous_identity_tf.visible = (current_eap == "EAP-TTLS")
                fast_provision_switch.visible = (current_eap == "EAP-FAST")
            else:
                inner_method_container.visible = False

            page.update()

        inner_method_container.controls = [
            ft.Text("Inner Method Settings", size=16, weight=ft.FontWeight.W_600),
            inner_method_dropdown,
            anonymous_identity_tf,
            fast_provision_switch,
        ]

        def save_and_run_test(e):
            config["username"] = test_username_tf.value.strip()
            config["password"] = test_password_tf.value.strip()
            config["eap_type"] = eap_dropdown.value
            config["server_ip"] = server_ip_tf.value.strip()
            config["port"] = port_tf.value.strip()
            config["timeout"] = timeout_tf.value.strip()

            if inner_method_container.visible:
                config["inner_method"] = inner_method_dropdown.value
                config["anonymous_identity"] = anonymous_identity_tf.value.strip()
                config["fast_provisioning"] = fast_provision_switch.value

            print("===== RUNNING TEST =====")
            print(f"Test Title: {test_title}, EAP={config['eap_type']}")
            # If eap_type is PEAP, run our stub
            if config['eap_type'] == 'PEAP':
                success = run_peap_test(
                    username=config["username"],
                    password=config["password"],
                    server_ip=config["server_ip"],
                    port=config["port"],
                    timeout=config["timeout"],
                    inner_method=config["inner_method"]
                )
                print(f"PEAP test success? {success}")

            # Show indefinite SnackBar
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Running {test_title} (EAP={config['eap_type']})", color="white"),
                bgcolor="#00ADEF",
                auto_hide=False,  # keep it open
                action="Close",
                on_action=lambda _: close_snack_bar()
            )
            page.snack_bar.open = True
            page.update()

        def close_snack_bar():
            # close the snack bar
            page.snack_bar.open = False
            page.update()

        def go_back(e):
            page.go("/main")

        view = ft.View(
            f"/test/{test_id}",
            [
                ft.Row([
                    ft.Text(test_title, size=24, weight=ft.FontWeight.W_600),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text("Please configure the test details below:", size=16),
                test_username_tf,
                test_password_tf,
                eap_dropdown,
                server_ip_tf,
                port_tf,
                timeout_tf,
                inner_method_container,
                cert_container,
                ft.ElevatedButton(
                    "Run Test", on_click=save_and_run_test,
                    color="white", bgcolor="#00ADEF"
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
        update_eap_ui_visibility()
        return view

    # -------------- 4. CLIENTS, 5. VMS, etc. --------------
    # Omitted for brevity, but you'd have the same structure:
    # - A "Test" button
    # - A snack bar with "auto_hide=False"
    # - page.update() after opening the snack bar

    def build_clients_view():
        def update_clients_list():
            clients_col.controls.clear()
            for idx, c in enumerate(clients):
                clients_col.controls.append(build_client_section(idx, c))
            page.update()

        def run_client_test(idx):
            test_client_config(idx)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Test run for {clients[idx]['client_name']}", color="white"),
                bgcolor="#00ADEF",
                auto_hide=False,
                action="Close",
                on_action=lambda _: close_snack()
            )
            page.snack_bar.open = True
            page.update()

        def close_snack():
            page.snack_bar.open = False
            page.update()

        def build_client_section(idx, c):
            test_btn = ft.ElevatedButton(
                "Test",
                color="white", bgcolor="#00ADEF",
                on_click=lambda e, i=idx: run_client_test(i)
            )
            return ft.Column([
                ft.TextField(label="Client Name", width=200, value=c["client_name"]),
                test_btn,
                ft.Divider()
            ], spacing=10)

        clients_col = ft.Column(spacing=10)
        update_clients_list()

        def go_back(e):
            page.go("/main")

        return ft.View(
            "/clients",
            [
                ft.Row([
                    ft.Text("Configure Clients", size=24, weight=ft.FontWeight.W_600),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                clients_col
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Similar approach for build_vms_view()

    def build_vms_view():
        def go_back(e):
            page.go("/main")
        return ft.View(
            "/vms",
            [ft.Text("VMs View", size=24), ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back)]
        )

    # -------------- 6. LINUX HOSTS ----------------------
    def build_linux_hosts_view():
        def update_hosts_list():
            hosts_col.controls.clear()
            for idx, host in enumerate(linux_hosts):
                hosts_col.controls.append(build_linux_host_section(idx, host))
            page.update()

        def test_linux_host_button_click(idx):
            success, message = test_linux_host(idx)
            # indefinite snack bar
            page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="white"),
                bgcolor="#00ADEF" if success else "#FF0000",
                auto_hide=False,
                action="Close",
                on_action=lambda _: close_snack()
            )
            page.snack_bar.open = True
            page.update()

        def close_snack():
            page.snack_bar.open = False
            page.update()

        key_picker = ft.FilePicker()
        page.overlay.append(key_picker)

        def open_key_picker(index):
            key_picker.data = index
            key_picker.pick_files(allow_multiple=False, dialog_title="Select SSH Key File")

        def handle_ssh_key(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                chosen_file = e.files[0].path
                idx = e.control.data
                linux_hosts[idx]["ssh_key_file"] = chosen_file
            else:
                idx = e.control.data
                linux_hosts[idx]["ssh_key_file"] = None
            update_hosts_list()

        key_picker.on_result = handle_ssh_key

        def build_linux_host_section(idx, host):
            test_btn = ft.ElevatedButton(
                "Test Host",
                color="white", bgcolor="#00ADEF",
                on_click=lambda e, i=idx: test_linux_host_button_click(i)
            )
            return ft.Column([
                ft.TextField(label="Host Name", width=200, value=host["host_name"]),
                ft.Row([
                    ft.TextField(label="IP Address", width=200, value=host["ip_address"]),
                    ft.TextField(label="SSH Port", width=100, value=str(host["port"])),
                ]),
                ft.Row([
                    ft.TextField(label="SSH Username", width=200, value=host["ssh_user"]),
                    ft.TextField(label="SSH Password", width=200, value=host["ssh_password"],
                                 password=True, can_reveal_password=True),
                ]),
                ft.Row([
                    ft.ElevatedButton("Select SSH Key", color="white", bgcolor="#00ADEF",
                                      on_click=lambda e, i=idx: open_key_picker(i)),
                    ft.Text(value=(f"Key: {host['ssh_key_file']}" if host["ssh_key_file"] else "No key selected"), size=14)
                ]),
                test_btn,
                ft.Divider()
            ], spacing=10)

        def add_linux_host(e):
            linux_hosts.append({
                "host_name": "NewLinuxHost",
                "ip_address": "10.10.10.50",
                "port": 22,
                "ssh_user": "monitor",
                "ssh_password": "",
                "ssh_key_file": None,
            })
            update_hosts_list()

        def go_back(e):
            page.go("/main")

        hosts_col = ft.Column(spacing=10)
        update_hosts_list()

        return ft.View(
            "/linux_hosts",
            [
                ft.Row([
                    ft.Text("Configure Forescout CounterACT Hosts", size=24, weight=ft.FontWeight.W_600),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                hosts_col,
                ft.Row([
                    ft.ElevatedButton("Add Host", color="white", bgcolor="#00ADEF", on_click=add_linux_host),
                ], spacing=20),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # -------------- 7. SETTINGS ---------------------------
    def build_settings_view():
        dark_mode_switch = ft.Switch(
            label="Enable Dark Mode",
            value=(page.theme_mode == ft.ThemeMode.DARK),
            on_change=toggle_dark_mode
        )
        persistent_switch = ft.Switch(
            label="Persistent Configuration",
            value=settings_data["persistent_config"],
            on_change=toggle_persistent_config
        )

        def go_back(e):
            page.go("/main")

        return ft.View(
            "/settings",
            [
                ft.Row([
                    ft.Text("Settings", size=24, weight=ft.FontWeight.W_600),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Column([
                    ft.Text("Theme Options"),
                    dark_mode_switch,
                    ft.Divider(height=10, color="transparent"),
                    ft.Text("Configuration Options"),
                    persistent_switch,
                ], spacing=10),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def toggle_dark_mode(e: ft.ControlEvent):
        if e.control.value:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "black"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "white"
        page.update()

    def toggle_persistent_config(e: ft.ControlEvent):
        new_val = e.control.value
        settings_data["persistent_config"] = new_val
        print(f"Persistent Configuration set to: {new_val}")

    # -------------- 8. DIAGNOSTICS -------------------------
    def build_diagnostics_view():
        chart_container = ft.Column()

        def update_charts():
            chart_container.controls.clear()
            for host, data in diagnostics_data.items():
                fig = create_line_chart_for_host(host, data)
                chart_container.controls.append(fpc.PlotlyChart(fig, expand=True))
            page.update()

        def create_line_chart_for_host(hostname, data_dict):
            df = {
                "Time": data_dict["timestamps"],
                "CPU": data_dict["cpu_percent"],
                "Memory": data_dict["memory_percent"],
            }
            fig = px.line(
                df,
                x="Time",
                y=["CPU", "Memory"],
                title=f"Resource Usage for {hostname}",
                markers=True
            )
            fig.update_layout(
                xaxis_title="Timestamp",
                yaxis_title="Percentage (%)",
                legend_title="Metric"
            )
            return fig

        def fetch_data_click(e):
            import random
            for host, d in diagnostics_data.items():
                last_time = d["timestamps"][-1] if d["timestamps"] else 0
                d["timestamps"].append(last_time + 1)
                new_cpu = max(0, min(100, d["cpu_percent"][-1] + random.randint(-5, 5)))
                new_mem = max(0, min(100, d["memory_percent"][-1] + random.randint(-2, 4)))
                d["cpu_percent"].append(new_cpu)
                d["memory_percent"].append(new_mem)
            update_charts()

        update_charts_button = ft.ElevatedButton("Fetch/Refresh Data", color="white", bgcolor="#00ADEF", on_click=fetch_data_click)

        def go_back(e):
            page.go("/main")

        view = ft.View(
            "/diagnostics",
            [
                ft.Row([
                    ft.Text("Diagnostics: Resource Utilization", size=24, weight=ft.FontWeight.W_600),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=go_back)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text("Below is CPU/Memory usage fetched from remote hosts (simulated data).", size=16),
                update_charts_button,
                chart_container
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        update_charts()
        return view

    # INIT
    page.on_route_change = route_change
    page.go("/")


# RUN APP
if __name__ == "__main__":
    # Force the Flet app to open in the browser
    ft.app(target=main, view=ft.WEB_BROWSER)
