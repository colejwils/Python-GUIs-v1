import flet as ft
import paramiko
import os

def main(page: ft.Page):
    page.title = "Flet SSH Demo"
    
    # In-memory list of configurations
    ssh_configs = []

    txt_host = ft.TextField(label="Host", value='10.110.1.75')
    txt_user = ft.TextField(label="Username", value='root')
    txt_password = ft.TextField(label="Password", value='Vlabs123$$$', password=True)
    txt_keyfile = ft.TextField(label="Key File Path")
    lbl_status = ft.Text(value="", color="red")

    def add_ssh_config(e):
        if not txt_host.value or not txt_user.value:
            lbl_status.value = "Host and username are required."
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
        # Clear the fields
        txt_host.value = ""
        txt_user.value = ""
        txt_password.value = ""
        txt_keyfile.value = ""
        page.update()

    def on_config_added(e):
        # This could refresh a dropdown or do any other post-add logic
        # e.g., refresh_host_list()
        pass

    def handle_add_config(e):
        # A single event handler that calls both functions
        add_ssh_config(e)
        on_config_added(e)

    btn_add_config = ft.ElevatedButton(
        text="Add SSH Config",
        on_click=handle_add_config
    )

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

    page.add(config_form)

if __name__ == "__main__":
    ft.app(target=main)
