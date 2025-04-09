import flet as ft

def ssh_test_function(username, password, host_ip):
    """
    Simple placeholder function.
    - If username/password/host_ip are all non-empty, return success.
    - Otherwise, return failure.
    """
    print("=== SSH TEST FUNCTION CALLED ===")
    print(f"Username: {username}, Password: {password}, Host: {host_ip}\n")

    # If all fields are non-empty, simulate success
    if username and password and host_ip:
        return True, f"SSH connection to {host_ip} successful!"
    else:
        return False, "Missing username/password/host IP. SSH test failed."

def main(page: ft.Page):
    page.title = "SSH Test with SnackBar"
    page.window_width = 500
    page.window_height = 300
    page.theme_mode = ft.ThemeMode.LIGHT  # easier to see in some environments

    # A helper to close/hide the SnackBar.
    def close_snack(e):
        if page.snack_bar:
            page.snack_bar.open = False
            page.update()

    # Username, password, host_ip fields
    username_tf = ft.TextField(label="Username", width=250)
    password_tf = ft.TextField(label="Password", password=True, can_reveal_password=True, width=250)
    host_ip_tf  = ft.TextField(label="Host IP", width=250)

    # The 'Test' button logic
    def on_test_click(e):
        username = username_tf.value.strip()
        password = password_tf.value.strip()
        host_ip  = host_ip_tf.value.strip()

        success, msg = ssh_test_function(username, password, host_ip)

        # Make a SnackBar
        snack = ft.SnackBar(
            content=ft.Text(msg, color="white"),
            bgcolor="green" if success else "red",
            action="Close",
            on_action=close_snack
        )
        # Assign & open
        page.snack_bar = snack
        page.snack_bar.open = True
        page.update()

    # The button that triggers on_test_click
    test_button = ft.ElevatedButton("Test SSH", on_click=on_test_click)

    # Layout
    content = ft.Column(
        [
            ft.Text("Enter username, password, and host IP, then click 'Test SSH':", size=16),
            username_tf,
            password_tf,
            host_ip_tf,
            test_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(content)

if __name__ == "__main__":
    ft.app(target=main)
