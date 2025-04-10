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

    # Create SSH client
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
    page.window_width = 800
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    # In-memory list of configurations (host, user, password, keyfile)
    # Each entry = { "host": ..., "username": ..., "password": ..., "key_file": ... }
    ssh_configs = []

    # ----- UI Elements for Config Form -----
    txt_host = ft.TextField(label="Host", width=250)
    txt_user = ft.TextField(label="Username", width=200)
    txt_password = ft.TextField(label="Password", password=True, width=200)
    txt_keyfile = ft.TextField(label="Key File Path", width=250)
    
    def add_ssh_config(e):
        # Basic validation
        if not txt_host.value or not txt_user.value:
            lbl_status.value = "Host and username are required."
            page.update()
            return
        # Save the config
        config = {
            "host": txt_host.value.strip(),
            "username": txt_user.value.strip(),
            "password": txt_password.value,  # can be empty
            "key_file": txt_keyfile.value.strip()  # can be empty
        }
        ssh_configs.append(config)
        lbl_status.value = f"Added host config for {txt_host.value}."
        page.update()

        # Clear fields
        txt_host.value = ""
        txt_user.value = ""
        txt_password.value = ""
        txt_keyfile.value = ""
        page.update()

    btn_add_config = ft.ElevatedButton(
        text="Add SSH Config",
        on_click=add_ssh_config
    )

    lbl_status = ft.Text(value="", color="red")

    config_form = ft.Column(
        controls=[
            ft.Text("Add SSH Host Configuration", style="headlineSmall"),
            txt_host,
            txt_user,
            txt_password,
            txt_keyfile,
            btn_add_config,
            lbl_status
        ],
        spacing=10
    )

    # ----- UI Elements for Running Commands -----
    # Dropdown or other control to select which host config to use
    ddl_hosts = ft.Dropdown(label="Select SSH Host", width=300, options=[])

    # Output area
    txt_output = ft.Text(value="", selectable=True)

    def refresh_host_list():
        ddl_hosts.options = [
            ft.dropdown.Option(f"{cfg['host']} ({cfg['username']})") 
            for cfg in ssh_configs
        ]
        page.update()

    def run_command(e, command_str: str):
        if not ddl_hosts.value:
            txt_output.value = "Please select a host configuration."
            page.update()
            return

        # Find chosen config
        selected_label = ddl_hosts.value
        chosen_config = None
        for c in ssh_configs:
            # e.g. "192.168.1.5 (admin)"
            # We can match host+user to identify the correct config
            label = f"{c['host']} ({c['username']})"
            if label == selected_label:
                chosen_config = c
                break

        if not chosen_config:
            txt_output.value = "Configuration not found. Please re-add."
            page.update()
            return
        
        # Connect via SSH and run the command
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
        run_command(e, "cat /shared/fslog/plugin/connect_module/connect_module.log")

    def cat_connect_python_log(e):
        run_command(e, "cat /usr/local/forescout/plugin/connect_module/python_logs/python_server.log")

    btn_cat_connect_plugin_log = ft.ElevatedButton(
        text="Cat Connect Plugin Log",
        on_click=cat_connect_plugin_log
    )
    btn_cat_connect_python_log = ft.ElevatedButton(
        text="Cat Connect Python Log",
        on_click=cat_connect_python_log
    )

    # After adding a config, we can refresh the dropdown
    def on_config_added(e):
        refresh_host_list()

    btn_add_config.on_click = [add_ssh_config, on_config_added]

    command_controls = ft.Column(
        controls=[
            ft.Text("Run SSH Commands", style="headlineSmall"),
            ddl_hosts,
            ft.Row(controls=[btn_cat_connect_plugin_log, btn_cat_connect_python_log]),
            ft.Text("Output:"),
            txt_output
        ],
        spacing=10
    )

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

# Run the app
if __name__ == "__main__":
    ft.app(target=main)
