import flet as ft

def main(page: ft.Page):
    page.title = "Minimal SnackBar Demo"
    page.window_width = 400
    page.window_height = 200

    # A function to close/hide the snack bar:
    def close_snack(e):
        if page.snack_bar:
            page.snack_bar.open = False
            page.update()

    # On-click handler: just show a snack bar
    def show_snackbar(e):
        # Make a snack bar:
        snack = ft.SnackBar(
            content=ft.Text("Hello from the minimal SnackBar!", color="white"),
            bgcolor="blue",
            action="Close",
            on_action=close_snack
        )
        # Assign & show
        page.snack_bar = snack
        page.snack_bar.open = True
        page.update()

    # A single button that triggers the snack bar
    btn = ft.ElevatedButton("Click me for snack bar", on_click=show_snackbar)

    # Add the button to the page
    page.add(btn)

if __name__ == "__main__":
    ft.app(target=main)
