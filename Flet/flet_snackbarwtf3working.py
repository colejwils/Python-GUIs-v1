import flet as ft
import paramiko
import os

def connect_ssh_and_run_command(
    host: str,
    username: str,
    password: str = None,
    key_file: str = None,
    command: str = ""
) -> str:
    """
    Connect to an SSH host with either password or key file
    and run a command. Returns the command output or any errors.
    """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_file and os.path.exists(key_file):
            # Key-based authentication
            key = paramiko.RSAKey.from_private_key_file(key_file)
            ssh.connect(hostname=host, username=username, pkey=key, timeout=10)
        else:
            # Password-based authentication
            ssh.connect(hostname=host, username=username, password=password, timeout=10)

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode("utf-8", errors="ignore")
        errors = stderr.read().decode("utf-8", errors="ignore")

        if errors.strip():
            return f"ERROR:\n{errors.strip()}"
        return output.strip()

    except Exception as e:
        return f"Connection or command error: {str(e)}"
    finally:
        ssh.close()


def main(page: ft.Page):
    page.title = "Flet SSH Demo"
    page.window_width = 900
    page.window_height = 700
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # In-memory list of configurations (host, user, password, keyfile)
    # Each entry = { "host": ..., "username": ..., "password": ..., "key_file": ... }
    ssh_configs = []

    # We’ll track whether the latest SSH test was successful:
    test_ok = False

    # ---- UI Elements for Config Form ----
    txt_host = ft.TextField(label="Host", width=300)
    txt_user = ft.TextField(label="Username", width=250)
    txt_password = ft.TextField(label="Password", password=True, width=250)
    txt_keyfile = ft.TextField(label="Key File Path", width=300)

    lbl_test_result = ft.Text(value="", color="red")
    lbl_status = ft.Text(value="", color="red")

    # "Add SSH Config" starts disabled, only becomes enabled after a successful test.
    btn_add_config = ft.ElevatedButton(
        text="Add SSH Config",
        disabled=True,  
    )

    def test_ssh_config(e):
        nonlocal test_ok
        # Clear any previous test results
        lbl_test_result.value = ""
        btn_add_config.disabled = True
        page.update()

        # Basic validation
        if not txt_host.value.strip() or not txt_user.value.strip():
            lbl_test_result.value = "Error: Host and username are required."
            page.update()
            return

        # Attempt test connection
        result = connect_ssh_and_run_command(
            host=txt_host.value.strip(),
            username=txt_user.value.strip(),
            password=txt_password.value,
            key_file=txt_keyfile.value.strip(),
            command="echo SSH connection test successful!"
        )

        # If the result starts with "Connection or command error",
        # or if "ERROR" is in the returned text, we assume it failed.
        if "error" in result.lower() or "ERROR:" in result:
            lbl_test_result.value = f"Connection Test FAILED:\n{result}"
            test_ok = False
        else:
            lbl_test_result.value = f"Connection Test SUCCESS:\n{result}"
            test_ok = True
            btn_add_config.disabled = False

        page.update()

    def add_ssh_config(e):
        nonlocal test_ok
        # If test was never successful, do nothing
        if not test_ok:
            lbl_status.value = "Please test connection successfully before adding."
            page.update()
            return

        config = {
            "host": txt_host.value.strip(),
            "username": txt_user.value.strip(),
            "password": txt_password.value,
            "key_file": txt_keyfile.value.strip()
        }
        ssh_configs.append(config)
        lbl_status.value = f"Added host config for {txt_host.value}."
        page.update()

        # Clear fields and disable "Add" again until next test
        txt_host.value = ""
        txt_user.value = ""
        txt_password.value = ""
        txt_keyfile.value = ""
        lbl_test_result.value = ""
        test_ok = False
        btn_add_config.disabled = True
        page.update()
        refresh_host_list()

    # Assign the add_ssh_config function to the button
    btn_add_config.on_click = add_ssh_config

    btn_test_connection = ft.ElevatedButton(
        text="Test Connection",
        on_click=test_ssh_config
    )

    config_form = ft.Column(
        controls=[
            ft.Text("Add SSH Host Configuration", style="headlineSmall"),
            txt_host,
            txt_user,
            txt_password,
            txt_keyfile,
            ft.Row([btn_test_connection, btn_add_config], spacing=20),
            lbl_test_result,
            lbl_status
        ],
        spacing=10
    )

    # ---- UI Elements for Running Commands ----
    ddl_hosts = ft.Dropdown(label="Select SSH Host", width=400, options=[])
    txt_output = ft.Text(value="", selectable=True)

    def refresh_host_list():
        ddl_hosts.options = [
            ft.dropdown.Option(f"{cfg['host']} ({cfg['username']})") 
            for cfg in ssh_configs
        ]
        page.update()

    def run_command(command_str: str):
        selected_label = ddl_hosts.value
        if not selected_label:
            txt_output.value = "Please select a host configuration first."
            page.update()
            return

        # Find chosen config
        chosen_config = None
        for c in ssh_configs:
            label = f"{c['host']} ({c['username']})"
            if label == selected_label:
                chosen_config = c
                break

        if not chosen_config:
            txt_output.value = "Configuration not found. Please re-add."
            page.update()
            return

        # Connect via SSH and run command
        result = connect_ssh_and_run_command(
            host=chosen_config["host"],
            username=chosen_config["username"],
            password=chosen_config["password"],
            key_file=chosen_config["key_file"],
            command=command_str
        )
        txt_output.value = result
        page.update()

    def cat_connect_plugin_log(e):
        run_command("cat /shared/fslog/plugin/connect_module/connect_module.log")

    def cat_connect_python_log(e):
        run_command("cat /usr/local/forescout/plugin/connect_module/python_logs/python_server.log")

    btn_cat_connect_plugin_log = ft.ElevatedButton(
        text="Cat Connect Plugin Log",
        on_click=cat_connect_plugin_log
    )
    btn_cat_connect_python_log = ft.ElevatedButton(
        text="Cat Connect Python Log",
        on_click=cat_connect_python_log
    )

    command_controls = ft.Column(
        controls=[
            ft.Text("Run SSH Commands", style="headlineSmall"),
            ddl_hosts,
            ft.Row([btn_cat_connect_plugin_log, btn_cat_connect_python_log]),
            ft.Text("Output:"),
            txt_output
        ],
        spacing=10
    )

    # ---- Layout the page ----
    main_layout = ft.Column(
        controls=[
            config_form,
            ft.Divider(),
            command_controls
        ],
        spacing=20,
        expand=True
    )

    page.add(main_layout)

if __name__ == "__main__":
    ft.app(target=main)
