import flet as ft

# EAP methods and inner functions for the actual tests
def run_peap_test(username, password, server_ip, port, timeout, inner_method):
    """
    A simple placeholder function that "runs" a PEAP test.
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
    return True  # For now, just say it's successful

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

    # INITIAL THEME MODE: DARK
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = light_theme
    page.dark_theme = dark_theme
    page.bgcolor = "black"  # Dark by default

    # IN-MEMORY STATE FOR USER
    user_data = {
        "logged_in": False,
        "username": "",
    }

    # A SIMPLE LIST OF TESTS
    tests = [
        {"id": "test1", "name": "Automated WLAN Test"},
        {"id": "test2", "name": "Automated Wired Test"},
        {"id": "test3", "name": "IPv4 Regression Testing"},
        {"id": "test4", "name": "IPv6 Regression Testing"},
    ]

    # PER-TEST CONFIG (EAP, EAP-TLS, etc.)
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

    # ------------------------------------------------------------------
    # CLIENTS DATA
    # ------------------------------------------------------------------
    clients = [
        {
            "client_name": "TestClient1",
            "mac_address": "AA:BB:CC:DD:EE:01",
            "ip_address": "192.168.10.101",
            "use_radsec": False,
            "certificate_file": None,
            "client_secret": "",
        },
        {
            "client_name": "TestClient2",
            "mac_address": "AA:BB:CC:DD:EE:02",
            "ip_address": "192.168.10.102",
            "use_radsec": True,
            "certificate_file": "/path/to/cert.pem",
            "client_secret": "supersecret",
        },
    ]

    # ------------------------------------------------------------------
    # NEW: REMOTE VMS DATA (For wpa_supplicant & eapol_test over SSH)
    # ------------------------------------------------------------------
    vms = [
        {
            "vm_name": "UbuntuTestVM",
            "host": "192.168.50.10",
            "port": 22,
            "ssh_user": "testuser",
            "ssh_password": "secret",
            "ssh_key_file": None,  # optional
        },
        {
            "vm_name": "CentOSVM",
            "host": "192.168.50.20",
            "port": 2222,
            "ssh_user": "root",
            "ssh_password": "",
            "ssh_key_file": "/home/user/.ssh/id_rsa",
        },
    ]

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
        elif route == "/clients":
            # CLIENTS VIEW
            if user_data["logged_in"]:
                page.views.append(build_clients_view())
            else:
                page.go("/")
        elif route == "/settings":
            # SETTINGS VIEW
            if user_data["logged_in"]:
                page.views.append(build_settings_view())
            else:
                page.go("/")
        elif route == "/vms":
            # VMS VIEW
            if user_data["logged_in"]:
                page.views.append(build_vms_view())
            else:
                page.go("/")
        else:
            # 404
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
        username_tf = ft.TextField(
            label="Username", 
            width=300,
            on_submit=lambda e: login_click(e)
        )
        password_tf = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            on_submit=lambda e: login_click(e)
        )

        def login_click(e):
            if username_tf.value.strip() and password_tf.value.strip():
                user_data["username"] = username_tf.value.strip()
                user_data["logged_in"] = True
                page.go("/main")
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please enter username and password!", color="white"),
                    bgcolor="#F36F21",
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
        instructions = ft.Text("Select a test to configure and run, or configure clients / VMs.", size=16)

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

        def clients_click(e):
            page.go("/clients")

        def vms_click(e):
            page.go("/vms")

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
                        ft.IconButton(icon=ft.Icons.DEVICE_HUB, tooltip="Configure VMs", on_click=vms_click),
                        ft.IconButton(icon=ft.Icons.COMPUTER, tooltip="Configure Clients", on_click=clients_click),
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
    # 3. TEST CONFIG VIEW (EAP & RADIUS)
    # ─────────────────────────────────────────────────────────
    def build_test_config_view(test_id: str):
        config = test_configs[test_id]
        test_title = next((t["name"] for t in tests if t["id"] == test_id), "Unknown Test")

        test_username_tf = ft.TextField(label="Test Username", width=300, value=config["username"])
        test_password_tf = ft.TextField(label="Test Password", password=True, can_reveal_password=True, width=300, value=config["password"])
        server_ip_tf = ft.TextField(label="Server IP/Hostname", width=300, value=config["server_ip"])
        port_tf = ft.TextField(label="Port", width=300, value=config["port"])
        timeout_tf = ft.TextField(label="Timeout (seconds)", width=300, value=config["timeout"])

        eap_dropdown = ft.Dropdown(
            label="EAP Type",
            options=[ft.dropdown.Option(e) for e in eap_options],
            value=config["eap_type"],
            width=300,
            on_change=lambda e: update_eap_ui_visibility()
        )

        inner_method_dropdown = ft.Dropdown(label="Inner Method", width=300, value=config["inner_method"])

        anonymous_identity_tf = ft.TextField(label="Anonymous Identity (TTLS)", width=300, value=config["anonymous_identity"])
        fast_provision_switch = ft.Switch(label="Allow FAST Provisioning", value=config["fast_provisioning"])

        certificate_picker = ft.FilePicker(on_result=lambda e: handle_cert_selected(e))
        page.overlay.append(certificate_picker)

        cert_label = ft.Text(
            value=(f"Selected cert: {config['certificate_file']}" if config["certificate_file"] else "No certificate selected"),
            size=14
        )

        def select_certificate(e):
            certificate_picker.pick_files(
                allow_multiple=False,
                dialog_title="Select Certificate File"
            )

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
                cert_label
            ],
            visible=(config["eap_type"] == "EAP-TLS")
        )

        def handle_cert_selected(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                chosen_file = e.files[0].path
                config["certificate_file"] = chosen_file
                cert_label.value = f"Selected cert: {chosen_file}"
            else:
                config["certificate_file"] = None
                cert_label.value = "No certificate selected"
            page.update()

        inner_method_container = ft.Column(controls=[], visible=False)

        def update_eap_ui_visibility():
            current_eap = eap_dropdown.value
            cert_container.visible = (current_eap == "EAP-TLS")

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

            print("===== TEST RUN =====")
            print(f"Test Title: {test_title}")
            print(f"Username: {config['username']}")
            print(f"Password: {config['password']}")
            print(f"EAP Type: {config['eap_type']}")
            print(f"Inner Method: {config['inner_method']}")
            print(f"Anonymous Identity: {config['anonymous_identity']}")
            print(f"FAST Provisioning? {config['fast_provisioning']}")
            print(f"Server IP: {config['server_ip']}")
            print(f"Port: {config['port']}")
            print(f"Timeout: {config['timeout']}")
            print(f"Cert File: {config['certificate_file']}")
            print("====================\n")
            if config.get('eap_type'):
                eap_type = config.get('eap_type')
                if eap_type == 'PEAP':
                    success = run_peap_test(
                        username=config["username"],
                        password=config["password"],
                        server_ip=config["server_ip"],
                        port=config["port"],
                        timeout=config["timeout"],
                        inner_method=config["inner_method"]
                    )
                    print(f"PEAP test success? {success}")
                else:
                    print(f"Running test with EAP type: {eap_type} (no stub function yet).")

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    f"Running {test_title} with EAP={config['eap_type']} "
                    f"(Inner={config['inner_method']}), Cert={config['certificate_file']}",
                    color="white"
                ),
                bgcolor="#00ADEF",
            )
            page.snack_bar.open = True
            page.update()

        def go_back(e):
            page.go("/main")

        view = ft.View(
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

                inner_method_container,
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

        update_eap_ui_visibility()
        return view

    # ─────────────────────────────────────────────────────────
    # 4. CLIENTS VIEW
    # ─────────────────────────────────────────────────────────
    def build_clients_view():
        def update_client_list():
            clients_col.controls.clear()
            for idx, c in enumerate(clients):
                row = build_client_section(idx, c)
                clients_col.controls.append(row)
            page.update()

        client_cert_picker = ft.FilePicker(on_result=lambda e: handle_client_cert(e))
        page.overlay.append(client_cert_picker)

        def open_client_cert_picker(index):
            client_cert_picker.data = index
            client_cert_picker.pick_files(
                allow_multiple=False,
                dialog_title="Select Client Certificate"
            )

        def handle_client_cert(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                chosen_file = e.files[0].path
                cl_idx = e.control.data
                clients[cl_idx]["certificate_file"] = chosen_file
            else:
                cl_idx = e.control.data
                clients[cl_idx]["certificate_file"] = None
            update_client_list()

        def build_client_section(idx, c):
            name_tf = ft.TextField(
                label="Client Name",
                width=200,
                value=c["client_name"],
                on_change=lambda e: save_changes(idx, "client_name", e.control.value)
            )
            mac_tf = ft.TextField(
                label="MAC Address",
                width=200,
                value=c["mac_address"],
                on_change=lambda e: save_changes(idx, "mac_address", e.control.value)
            )
            ip_tf = ft.TextField(
                label="IP Address",
                width=200,
                value=c["ip_address"],
                on_change=lambda e: save_changes(idx, "ip_address", e.control.value)
            )

            radsec_switch = ft.Switch(
                label="Use RadSec?",
                value=c["use_radsec"],
                on_change=lambda e: toggle_radsec(idx, e.control.value)
            )

            pick_cert_btn = ft.ElevatedButton(
                "Select RadSec Cert",
                color="white",
                bgcolor="#00ADEF",
                on_click=lambda e: open_client_cert_picker(idx),
                visible=c["use_radsec"]
            )

            cert_info_label = ft.Text(
                value=(f"Cert: {c['certificate_file']}" if c["certificate_file"] else "No cert selected"),
                size=14,
                visible=c["use_radsec"]
            )

            secret_tf = ft.TextField(
                label="Client Secret",
                width=200,
                value=c["client_secret"],
                password=True,
                can_reveal_password=True,
                visible=c["use_radsec"],
                on_change=lambda e: save_changes(idx, "client_secret", e.control.value)
            )

            remove_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Remove this client",
                on_click=lambda e: remove_client(idx)
            )

            return ft.Column(
                [
                    ft.Row([name_tf, mac_tf, ip_tf, remove_btn], wrap=True),
                    ft.Row([radsec_switch], wrap=True),
                    ft.Row([pick_cert_btn, cert_info_label], wrap=True),
                    secret_tf,
                    ft.Divider()
                ],
                spacing=10
            )

        def save_changes(index, field, new_value):
            clients[index][field] = new_value

        def toggle_radsec(index, new_value):
            clients[index]["use_radsec"] = new_value
            if not new_value:
                clients[index]["certificate_file"] = None
                clients[index]["client_secret"] = ""
            update_client_list()

        def remove_client(index):
            clients.pop(index)
            update_client_list()

        def add_client(e):
            clients.append({
                "client_name": "NewClient",
                "mac_address": "AA:BB:CC:DD:EE:FF",
                "ip_address": "192.168.10.200",
                "use_radsec": False,
                "certificate_file": None,
                "client_secret": "",
            })
            update_client_list()

        def save_client_config(e):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Clients configuration saved!", color="white"),
                bgcolor="#00ADEF",
            )
            page.snack_bar.open = True
            page.update()

        def go_back(e):
            page.go("/main")

        clients_col = ft.Column(spacing=10)
        update_client_list()

        return ft.View(
            "/clients",
            [
                ft.Row(
                    [
                        ft.Text("Configure Clients", size=24, weight=ft.FontWeight.W_600),
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back to Main", on_click=go_back),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text(
                    "Add, edit, or remove clients below. If 'Use RadSec' is enabled, configure a certificate and secret:",
                    size=16
                ),
                clients_col,
                ft.Row(
                    [
                        ft.ElevatedButton("Add Client", color="white", bgcolor="#00ADEF", on_click=add_client),
                        ft.ElevatedButton("Save", color="white", bgcolor="#00ADEF", on_click=save_client_config),
                    ],
                    spacing=20
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

    # ─────────────────────────────────────────────────────────
    # NEW: 5. VMS VIEW (SSH for wpa_supplicant & eapol_test)
    # ─────────────────────────────────────────────────────────
    def build_vms_view():
        def update_vms_list():
            vms_col.controls.clear()
            for idx, vm in enumerate(vms):
                row = build_vm_section(idx, vm)
                vms_col.controls.append(row)
            page.update()

        vm_key_picker = ft.FilePicker(on_result=lambda e: handle_vm_key(e))
        page.overlay.append(vm_key_picker)

        def open_vm_key_picker(index):
            vm_key_picker.data = index
            vm_key_picker.pick_files(
                allow_multiple=False,
                dialog_title="Select SSH Key File"
            )

        def handle_vm_key(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                chosen_file = e.files[0].path
                vm_idx = e.control.data
                vms[vm_idx]["ssh_key_file"] = chosen_file
            else:
                vm_idx = e.control.data
                vms[vm_idx]["ssh_key_file"] = None
            update_vms_list()

        # STUB FUNCTIONS TO “RUN” WPA_SUPPLICANT / EAPOL_TEST
        def run_wpa_supplicant(idx):
            vm = vms[idx]
            print("----- RUNNING WPA_SUPPLICANT -----")
            print(f"VM: {vm['vm_name']} @ {vm['host']}:{vm['port']}")
            print(f"SSH User: {vm['ssh_user']}")
            print(f"SSH Key: {vm['ssh_key_file']}")
            print("Simulating remote SSH call to start wpa_supplicant...")

        def run_eapol_test(idx):
            vm = vms[idx]
            print("----- RUNNING EAPOL_TEST -----")
            print(f"VM: {vm['vm_name']} @ {vm['host']}:{vm['port']}")
            print(f"SSH User: {vm['ssh_user']}")
            print(f"SSH Key: {vm['ssh_key_file']}")
            print("Simulating remote SSH call to run eapol_test...")

        def build_vm_section(idx, vm):
            vm_name_tf = ft.TextField(
                label="VM Name",
                width=200,
                value=vm["vm_name"],
                on_change=lambda e: save_vm_changes(idx, "vm_name", e.control.value)
            )
            host_tf = ft.TextField(
                label="Host/IP",
                width=200,
                value=vm["host"],
                on_change=lambda e: save_vm_changes(idx, "host", e.control.value)
            )
            port_tf = ft.TextField(
                label="SSH Port",
                width=100,
                value=str(vm["port"]),
                on_change=lambda e: save_vm_changes(idx, "port", e.control.value)
            )
            user_tf = ft.TextField(
                label="SSH Username",
                width=200,
                value=vm["ssh_user"],
                on_change=lambda e: save_vm_changes(idx, "ssh_user", e.control.value)
            )
            pass_tf = ft.TextField(
                label="SSH Password",
                width=200,
                value=vm["ssh_password"],
                password=True,
                can_reveal_password=True,
                on_change=lambda e: save_vm_changes(idx, "ssh_password", e.control.value)
            )

            pick_key_btn = ft.ElevatedButton(
                "Select SSH Key",
                color="white",
                bgcolor="#00ADEF",
                on_click=lambda e: open_vm_key_picker(idx)
            )
            key_label = ft.Text(
                value=(f"Key: {vm['ssh_key_file']}" if vm["ssh_key_file"] else "No key selected"),
                size=14
            )

            run_wpa_btn = ft.ElevatedButton("Test wpa_supplicant", on_click=lambda e: run_wpa_supplicant(idx))
            run_eapol_btn = ft.ElevatedButton("Test eapol_test", on_click=lambda e: run_eapol_test(idx))

            remove_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Remove this VM",
                on_click=lambda e: remove_vm(idx)
            )

            return ft.Column(
                [
                    ft.Row([vm_name_tf, remove_btn], wrap=True),
                    ft.Row([host_tf, port_tf], wrap=True),
                    ft.Row([user_tf, pass_tf], wrap=True),
                    ft.Row([pick_key_btn, key_label], wrap=True),
                    ft.Row([run_wpa_btn, run_eapol_btn]),
                    ft.Divider()
                ],
                spacing=10
            )

        def save_vm_changes(index, field, new_value):
            # Type conversion for port if needed
            if field == "port":
                try:
                    new_value = int(new_value)
                except ValueError:
                    new_value = 22
            vms[index][field] = new_value

        def remove_vm(index):
            vms.pop(index)
            update_vms_list()

        def add_vm(e):
            vms.append({
                "vm_name": "NewVM",
                "host": "192.168.50.100",
                "port": 22,
                "ssh_user": "user",
                "ssh_password": "",
                "ssh_key_file": None,
            })
            update_vms_list()

        def save_vm_config(e):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("VM configuration saved!", color="white"),
                bgcolor="#00ADEF",
            )
            page.snack_bar.open = True
            page.update()

        def go_back(e):
            page.go("/main")

        vms_col = ft.Column(spacing=10)
        update_vms_list()

        return ft.View(
            "/vms",
            [
                ft.Row(
                    [
                        ft.Text("Configure Remote VMs", size=24, weight=ft.FontWeight.W_600),
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back to Main", on_click=go_back),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Add, edit, or remove VMs below. Then run wpa_supplicant or eapol_test via SSH:", size=16),
                vms_col,
                ft.Row(
                    [
                        ft.ElevatedButton("Add VM", color="white", bgcolor="#00ADEF", on_click=add_vm),
                        ft.ElevatedButton("Save", color="white", bgcolor="#00ADEF", on_click=save_vm_config),
                    ],
                    spacing=20
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

    # ─────────────────────────────────────────────────────────
    # 6. SETTINGS VIEW (FOR THEME TOGGLE, ETC.)
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

    # THEME TOGGLE FUNCTION
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
