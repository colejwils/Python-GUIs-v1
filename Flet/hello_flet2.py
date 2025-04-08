# pip install flet
import flet as ft

def main(page: ft.Page):
    # Page configuration
    page.title = "Flet Multi-Screen Example"
    page.window_width = 400
    page.window_height = 550
    
    # In-memory “state”
    user_data = {
        "username": "",
        "items": []
    }

    # ─────────────────────────────────────────────────────────
    # ROUTE HANDLER
    # ─────────────────────────────────────────────────────────
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            # Show login view
            page.views.append(build_login_view())
        elif page.route == "/main":
            # Show main view (after successful login)
            page.views.append(build_main_view())
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

    # ─────────────────────────────────────────────────────────
    # BUILD LOGIN VIEW
    # ─────────────────────────────────────────────────────────
    def build_login_view():
        # We can define controls inside the function
        username_tf = ft.TextField(label="Username", width=300)
        password_tf = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

        def login_click(e):
            if username_tf.value.strip() and password_tf.value.strip():
                # Basic validation: just check they're not empty
                user_data["username"] = username_tf.value.strip()
                page.go("/main")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Please enter username and password!"))
                page.snack_bar.open = True
                page.update()
        
        view = ft.View(
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
        return view

    # ─────────────────────────────────────────────────────────
    # BUILD MAIN VIEW
    # ─────────────────────────────────────────────────────────
    def build_main_view():
        # Display the current username
        welcome_text = ft.Text(
            f"Hello, {user_data['username']}!",
            size=22,
            weight=ft.FontWeight.W_600  # Use W_600 instead of SEMI_BOLD
        )
        
        # Items list
        item_input = ft.TextField(label="Add an item", width=300)
        items_column = ft.Column()

        def refresh_items_column():
            items_column.controls.clear()
            if user_data["items"]:
                for idx, val in enumerate(user_data["items"]):
                    # Each item with a delete button
                    items_column.controls.append(
                        ft.Row(
                            [
                                ft.Text(f"{idx+1}. {val}"),
                                ft.IconButton(
                                    icon=ft.icons.DELETE, 
                                    on_click=lambda e, i=idx: remove_item(i)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    )
            else:
                items_column.controls.append(ft.Text("No items yet.", italic=True))
            page.update()

        def add_item(e):
            text = item_input.value.strip()
            if text:
                user_data["items"].append(text)
                item_input.value = ""
                refresh_items_column()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Please enter text before adding an item."))
                page.snack_bar.open = True
            page.update()

        def remove_item(index):
            user_data["items"].pop(index)
            refresh_items_column()

        def logout(e):
            # Clear out items if you want or keep them—your choice:
            # user_data["items"].clear()
            page.go("/")
        
        add_button = ft.ElevatedButton("Add", on_click=add_item)
        
        # Build the initial items list
        refresh_items_column()

        view = ft.View(
            "/main",
            [
                ft.Row(
                    [
                        welcome_text,
                        ft.IconButton(icon=ft.icons.LOGOUT, tooltip="Logout", on_click=logout),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Manage your items below:", size=18),
                ft.Row([item_input, add_button]),
                items_column,
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )

        return view

    # ─────────────────────────────────────────────────────────
    # Set up route change handlers and initialize
    # ─────────────────────────────────────────────────────────
    page.on_route_change = route_change
    page.go("/")  # Start at the login route

# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)
